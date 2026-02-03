"""Input–output (IO) network shock propagation (first-pass).

This script builds a multi-region, multi-sector IO network and simulates
cascading shortages under capacity constraints.

Core idea
---------
Let A be the technical coefficients matrix where A[i,j] is the amount of input i
required per unit of gross output of j.

Baseline (no constraints): x solves x = A @ x + y => x = (I - A)^-1 @ y.

With a supply shock, each node j has a capacity cap[j] <= x0[j]. We iterate

  req = A @ x + y
  x_next = min(cap, req)

Until convergence. This is a simple rationing / feasibility fixed-point that
captures cascading constraints (upstream shortages reduce downstream output,
which in turn reduces demand for upstream).

Notes
-----
- This is *not* a full equilibrium model (no price response, no substitution).
- Good for first-pass intuition + fast stress tests.
- Uses PyTorch and runs on CUDA if available; otherwise CPU.

Usage
-----
python scripts/io_shock_propagation.py --demo

"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from typing import Iterable, List, Tuple


def _try_import_torch():
    """Optional torch backend (CUDA when available).

    We keep the model runnable even without torch installed (falls back to numpy).
    """
    try:
        import torch  # type: ignore

        return torch
    except Exception:
        return None


def _import_numpy():
    import numpy as np  # type: ignore

    return np


@dataclass
class IOSimResult:
    x0: "Tensor"
    xT: "Tensor"
    unmet_final: "Tensor"
    cap: "Tensor"
    iters: int
    converged: bool
    history_gap: List[float]


def make_synthetic_mrio(
    torch,
    n_countries: int,
    n_sectors: int,
    density: float = 0.15,
    seed: int = 0,
    stability_margin: float = 0.25,
    device: str = "cpu",
    dtype=None,
):
    """Create a random-ish, stable IO system (A, y) for demos.

    We generate a sparse-ish nonnegative A and then scale it so that spectral
    radius(A) < 1 - stability_margin.
    """

    if dtype is None:
        dtype = torch.float32

    g = torch.Generator(device="cpu").manual_seed(seed)

    n = n_countries * n_sectors

    # Sparse random weights
    mask = (torch.rand((n, n), generator=g) < density).to(dtype)

    # Encourage block structure (more within-country than cross)
    country_ids = torch.arange(n) // n_sectors
    same_country = (country_ids[:, None] == country_ids[None, :]).to(dtype)

    w_in = 0.75
    w_out = 0.25

    base = torch.rand((n, n), generator=g).to(dtype)
    A = mask * base * (w_in * same_country + w_out * (1.0 - same_country))

    # Normalize columns to represent input shares, then scale down.
    col_sum = A.sum(dim=0, keepdim=True) + 1e-8
    A = A / col_sum

    # Each sector uses some fraction of intermediate inputs (rest value-added).
    # Draw intermediate share between 0.2 and 0.8.
    interm_share = 0.2 + 0.6 * torch.rand((1, n), generator=g).to(dtype)
    A = A * interm_share

    # Scale by spectral radius estimate via power iteration.
    def power_iter(mat, steps=50):
        v = torch.rand((n, 1), generator=g).to(dtype)
        v = v / (v.norm() + 1e-12)
        for _ in range(steps):
            v = mat @ v
            v = v / (v.norm() + 1e-12)
        # Rayleigh quotient
        num = (v.T @ (mat @ v)).squeeze()
        den = (v.T @ v).squeeze() + 1e-12
        return (num / den).item()

    rho = power_iter(A)
    target = max(1e-6, 1.0 - stability_margin)
    if rho >= target:
        A = A * (target / (rho + 1e-12))

    # Final demand, positive
    y = torch.rand((n,), generator=g).to(dtype)
    y = y * (10.0 / (y.mean() + 1e-12))

    return A.to(device=device), y.to(device=device)


def solve_leontief(torch, A, y, device: str = "cpu"):
    """Solve x = (I - A)^-1 y."""
    n = A.shape[0]
    I = torch.eye(n, device=device, dtype=A.dtype)
    M = I - A
    # torch.linalg.solve is stable and GPU-friendly.
    x = torch.linalg.solve(M, y)
    return x


def simulate_capacity_cascade(
    torch,
    A,
    y,
    cap,
    x_init=None,
    max_iters: int = 200,
    tol: float = 1e-6,
):
    """Iterate x_{t+1} = min(cap, A @ x_t + y)."""

    if x_init is None:
        # start from capacity (pessimistic) to avoid overshooting
        x = cap.clone()
    else:
        x = x_init.clone()

    history_gap: List[float] = []
    converged = False

    for it in range(1, max_iters + 1):
        req = A @ x + y
        x_next = torch.minimum(cap, req)
        gap = (x_next - x).abs().max().item()
        history_gap.append(gap)
        x = x_next
        if gap < tol:
            converged = True
            break

    # unmet final demand (simple accounting): if intermediate takes priority,
    # unmet final approximated as max(0, y - (x - A@x)). Here x - A@x is value
    # available to satisfy final demand.
    avail_to_final = torch.clamp(x - (A @ x), min=0.0)
    unmet_final = torch.clamp(y - avail_to_final, min=0.0)

    return x, unmet_final, it, converged, history_gap


def idx(country: int, sector: int, n_sectors: int) -> int:
    return country * n_sectors + sector


def pretty_topk(torch, v, names: List[str], k: int = 10) -> List[Tuple[str, float]]:
    k = min(k, v.numel())
    vals, inds = torch.topk(v, k)
    out = []
    for val, ind in zip(vals.tolist(), inds.tolist()):
        out.append((names[ind], float(val)))
    return out


def run_demo(args):
    """Run a synthetic demo.

    Prefers PyTorch (CUDA if available). Falls back to NumPy-only CPU so the
    repo stays lightweight.
    """

    torch = _try_import_torch()

    # Name nodes
    names = [f"C{c}:S{s}" for c in range(args.countries) for s in range(args.sectors)]

    if torch is None:
        np = _import_numpy()
        rng = np.random.default_rng(args.seed)

        n = args.countries * args.sectors

        # --- Build A (similar logic to make_synthetic_mrio) ---
        mask = (rng.random((n, n)) < args.density).astype(np.float32)
        country_ids = (np.arange(n) // args.sectors).astype(int)
        same_country = (country_ids[:, None] == country_ids[None, :]).astype(np.float32)

        base = rng.random((n, n), dtype=np.float32)
        A = mask * base * (0.75 * same_country + 0.25 * (1.0 - same_country))

        col_sum = A.sum(axis=0, keepdims=True) + 1e-8
        A = A / col_sum
        interm_share = 0.2 + 0.6 * rng.random((1, n), dtype=np.float32)
        A = A * interm_share

        # Roughly scale down to ensure stability; use a conservative factor.
        A = 0.7 * A

        y = rng.random(n, dtype=np.float32)
        y = y * (10.0 / (y.mean() + 1e-12))

        I = np.eye(n, dtype=np.float32)
        x0 = np.linalg.solve(I - A, y)

        cap = x0.copy()
        for (c, s, r) in args.shock:
            j = idx(c, s, args.sectors)
            cap[j] = cap[j] * (1.0 - r)

        x = x0.copy()
        history_gap: List[float] = []
        converged = False
        for it in range(1, args.max_iters + 1):
            req = A @ x + y
            x_next = np.minimum(cap, req)
            gap = float(np.max(np.abs(x_next - x)))
            history_gap.append(gap)
            x = x_next
            if gap < args.tol:
                converged = True
                break

        xT = x
        avail_to_final = np.maximum(xT - (A @ xT), 0.0)
        unmet_final = np.maximum(y - avail_to_final, 0.0)

        output_loss = np.maximum(x0 - xT, 0.0)
        rel_loss = output_loss / (x0 + 1e-12)

        def topk(arr, k=10):
            k = min(k, arr.size)
            inds = np.argsort(-arr)[:k]
            return [(names[i], float(arr[i])) for i in inds]

        total_baseline = float(x0.sum())
        total_realized = float(xT.sum())

        report = {
            "device": "numpy-cpu",
            "n": int(n),
            "countries": args.countries,
            "sectors": args.sectors,
            "iters": it,
            "converged": converged,
            "total_baseline_output": total_baseline,
            "total_realized_output": total_realized,
            "total_output_loss": total_baseline - total_realized,
            "total_unmet_final": float(unmet_final.sum()),
            "top_output_loss": topk(output_loss),
            "top_rel_loss": topk(rel_loss),
            "top_unmet_final": topk(unmet_final),
            "top_upstream_strength": topk(A.sum(axis=1)),
            "history_gap_tail": history_gap[-10:],
            "shocks": args.shock,
            "note": "Install torch for GPU/precision: pip install torch",
        }
        return report

    # --- Torch path (CUDA if available) ---
    device = "cuda" if (args.cuda and torch.cuda.is_available()) else "cpu"

    A, y = make_synthetic_mrio(
        torch,
        n_countries=args.countries,
        n_sectors=args.sectors,
        density=args.density,
        seed=args.seed,
        stability_margin=0.25,
        device=device,
    )

    x0 = solve_leontief(torch, A, y, device=device)

    cap = x0.clone()
    for (c, s, r) in args.shock:
        j = idx(c, s, args.sectors)
        cap[j] = cap[j] * (1.0 - r)

    xT, unmet_final, iters, converged, history_gap = simulate_capacity_cascade(
        torch, A, y, cap, x_init=x0, max_iters=args.max_iters, tol=args.tol
    )

    output_loss = torch.clamp(x0 - xT, min=0.0)
    rel_loss = output_loss / (x0 + 1e-12)

    report = {
        "device": device,
        "n": int(A.shape[0]),
        "countries": args.countries,
        "sectors": args.sectors,
        "iters": iters,
        "converged": converged,
        "total_baseline_output": x0.sum().item(),
        "total_realized_output": xT.sum().item(),
        "total_output_loss": (x0.sum() - xT.sum()).item(),
        "total_unmet_final": unmet_final.sum().item(),
        "top_output_loss": pretty_topk(torch, output_loss, names, k=10),
        "top_rel_loss": pretty_topk(torch, rel_loss, names, k=10),
        "top_unmet_final": pretty_topk(torch, unmet_final, names, k=10),
        "top_upstream_strength": pretty_topk(torch, A.sum(dim=1), names, k=10),
        "history_gap_tail": history_gap[-10:],
        "shocks": args.shock,
    }

    return report


def _parse_shocks(raw: Iterable[str]) -> List[Tuple[int, int, float]]:
    out = []
    for s in raw:
        # Format: country,sector,reduction
        c_str, sec_str, r_str = s.split(",")
        out.append((int(c_str), int(sec_str), float(r_str)))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true", help="run a synthetic demo")
    p.add_argument("--countries", type=int, default=8)
    p.add_argument("--sectors", type=int, default=12)
    p.add_argument("--density", type=float, default=0.12)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--cuda", action="store_true", help="use CUDA if available")
    p.add_argument("--max-iters", type=int, default=200)
    p.add_argument("--tol", type=float, default=1e-6)
    p.add_argument(
        "--shock",
        action="append",
        default=[],
        help="shock as 'country,sector,reduction' (e.g. 2,3,0.5 means -50%)",
    )

    args = p.parse_args()

    if args.demo:
        args.shock = _parse_shocks(args.shock) if args.shock else [(1, 2, 0.6), (4, 7, 0.3)]
        report = run_demo(args)

        import json

        print(json.dumps(report, indent=2))
        return

    p.error("Only --demo is implemented in this first-pass script")


if __name__ == "__main__":
    main()
