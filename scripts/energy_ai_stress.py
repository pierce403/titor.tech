"""Energy + AI compute demand stress test (2030–2045).

First-pass Monte Carlo model intended for blog-quality scenario exploration.

Outputs:
- draws_wide.csv: per-draw headline values for selected years
- summary_by_year.csv: percentiles by year
- plots/*.png: key figures

GPU acceleration:
- Uses CuPy if available (CUDA). Falls back to NumPy.

This is not a forecast; it is a stress test with explicit assumptions.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np


def get_xp():
    """Return array module: cupy if available, else numpy."""
    try:
        import cupy as cp  # type: ignore

        # Minimal sanity check that CUDA is reachable.
        _ = cp.cuda.runtime.getDeviceCount()
        return cp
    except Exception:
        return np


def _triangular(xp, left, mode, right, size, rng):
    # xp.random.triangular doesn't exist for cupy in some versions; implement manually.
    u = rng.random(size=size)
    c = (mode - left) / (right - left)
    return xp.where(
        u < c,
        left + xp.sqrt(u * (right - left) * (mode - left)),
        right - xp.sqrt((1 - u) * (right - left) * (right - mode)),
    )


def _clip01(xp, x):
    return xp.clip(x, 0.0, 1.0)


@dataclass
class ModelConfig:
    start_year: int = 2030
    end_year: int = 2045
    n_draws: int = 50_000
    seed: int = 7

    # Electricity demand units: TWh/year.
    # Baseline global electricity demand in 2030.
    global_elec_2030_twh: Tuple[float, float, float] = (28_000.0, 32_000.0, 38_000.0)  # low/mode/high

    # Baseline AI+DC electricity in 2030 (includes training+inference+cooling overhead).
    ai_elec_2030_twh: Tuple[float, float, float] = (200.0, 700.0, 2_000.0)

    # Non-AI electricity growth (CAGR), 2030–2045.
    non_ai_cagr: Tuple[float, float, float] = (0.008, 0.018, 0.030)

    # AI compute usage growth (CAGR). Very uncertain.
    ai_compute_cagr: Tuple[float, float, float] = (0.15, 0.30, 0.55)

    # AI energy efficiency improvement (J per unit compute) (CAGR reduction).
    ai_eff_improve_cagr: Tuple[float, float, float] = (0.10, 0.20, 0.32)

    # PUE (power usage effectiveness) in 2030 and 2045.
    pue_2030: Tuple[float, float, float] = (1.15, 1.25, 1.40)
    pue_2045: Tuple[float, float, float] = (1.08, 1.15, 1.30)

    # Additional "rebound" multiplier capturing new applications / higher QoS,
    # applied to AI energy in 2045 relative to baseline trajectory.
    rebound_2045: Tuple[float, float, float] = (0.9, 1.1, 1.6)

    # Optional supply-side stress: plausible maximum annual electricity generation additions (TWh/year).
    # This is deliberately coarse.
    max_additions_twh_per_year: Tuple[float, float, float] = (600.0, 1_200.0, 2_000.0)


def simulate(cfg: ModelConfig):
    xp = get_xp()

    # RNG: cupy has its own Generator; if we fall back, use numpy.
    if xp is np:
        rng = np.random.default_rng(cfg.seed)
    else:
        rng = xp.random.default_rng(cfg.seed)

    years = xp.arange(cfg.start_year, cfg.end_year + 1)
    t = years - cfg.start_year
    n_years = int(years.shape[0])

    # Sample parameters.
    global_2030 = _triangular(xp, *cfg.global_elec_2030_twh, size=cfg.n_draws, rng=rng)
    ai_2030 = _triangular(xp, *cfg.ai_elec_2030_twh, size=cfg.n_draws, rng=rng)

    # Ensure AI is a subset of global.
    ai_2030 = xp.minimum(ai_2030, 0.20 * global_2030)
    non_ai_2030 = xp.maximum(global_2030 - ai_2030, 1.0)

    non_ai_cagr = _triangular(xp, *cfg.non_ai_cagr, size=cfg.n_draws, rng=rng)
    ai_compute_cagr = _triangular(xp, *cfg.ai_compute_cagr, size=cfg.n_draws, rng=rng)
    ai_eff_improve = _triangular(xp, *cfg.ai_eff_improve_cagr, size=cfg.n_draws, rng=rng)

    pue0 = _triangular(xp, *cfg.pue_2030, size=cfg.n_draws, rng=rng)
    pue1 = _triangular(xp, *cfg.pue_2045, size=cfg.n_draws, rng=rng)

    rebound_2045 = _triangular(xp, *cfg.rebound_2045, size=cfg.n_draws, rng=rng)

    # Supply-side additions capacity.
    max_additions = _triangular(xp, *cfg.max_additions_twh_per_year, size=cfg.n_draws, rng=rng)

    # Build PUE trajectory as linear in time between 2030 and 2045.
    pue_t = pue0[:, None] + (pue1 - pue0)[:, None] * (t[None, :] / float(cfg.end_year - cfg.start_year))
    pue_t = xp.clip(pue_t, 1.02, 2.5)

    # Non-AI electricity.
    non_ai = non_ai_2030[:, None] * (1.0 + non_ai_cagr)[:, None] ** t[None, :]

    # AI electricity: baseline * compute growth * efficiency improvement * PUE ratio.
    net_ai_growth = ((1.0 + ai_compute_cagr) / (1.0 + ai_eff_improve))
    ai = ai_2030[:, None] * (net_ai_growth[:, None] ** t[None, :]) * (pue_t / pue0[:, None])

    # Apply rebound smoothly towards 2045.
    rebound_path = 1.0 + (rebound_2045 - 1.0)[:, None] * (t[None, :] / float(cfg.end_year - cfg.start_year))
    ai = ai * rebound_path

    total = non_ai + ai

    ai_share = ai / total

    # Convert to average power (GW): TWh/year / 8.76.
    ai_gw = ai / 8.76

    # Supply stress: year-over-year additions needed (TWh/year).
    additions_needed = xp.zeros_like(total)
    additions_needed[:, 1:] = total[:, 1:] - total[:, :-1]

    supply_stress = additions_needed > max_additions[:, None]

    return {
        "xp": xp,
        "years": years,
        "ai_twh": ai,
        "non_ai_twh": non_ai,
        "total_twh": total,
        "ai_share": ai_share,
        "ai_gw": ai_gw,
        "additions_needed_twh": additions_needed,
        "max_additions_twh": max_additions,
        "supply_stress": supply_stress,
    }


def percentiles(x: np.ndarray, ps=(5, 10, 25, 50, 75, 90, 95)):
    return {f"p{p}": np.percentile(x, p, axis=0) for p in ps}


def to_numpy(xp, arr):
    if xp is np:
        return arr
    return arr.get()


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def run_and_save(out_dir: str, cfg: ModelConfig):
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_theme(style="whitegrid")

    sim = simulate(cfg)
    xp = sim["xp"]
    years = to_numpy(xp, sim["years"]).astype(int)

    ai = to_numpy(xp, sim["ai_twh"])
    total = to_numpy(xp, sim["total_twh"])
    share = to_numpy(xp, sim["ai_share"])
    ai_gw = to_numpy(xp, sim["ai_gw"])
    additions_needed = to_numpy(xp, sim["additions_needed_twh"])
    max_additions = to_numpy(xp, sim["max_additions_twh"])
    supply_stress = to_numpy(xp, sim["supply_stress"]).astype(bool)

    ensure_dir(out_dir)
    plots_dir = os.path.join(out_dir, "plots")
    ensure_dir(plots_dir)

    # Summary by year.
    rows = []
    for j, y in enumerate(years):
        rows.append(
            {
                "year": int(y),
                **{k: v[j] for k, v in percentiles(ai, ps=(5, 50, 95)).items()},
            }
        )
    ai_summary = pd.DataFrame(rows).rename(columns={"p5": "ai_twh_p5", "p50": "ai_twh_p50", "p95": "ai_twh_p95"})

    rows = []
    for j, y in enumerate(years):
        rows.append(
            {
                "year": int(y),
                **{k: v[j] for k, v in percentiles(share, ps=(5, 50, 95)).items()},
            }
        )
    share_summary = pd.DataFrame(rows).rename(
        columns={"p5": "ai_share_p5", "p50": "ai_share_p50", "p95": "ai_share_p95"}
    )

    summary = ai_summary.merge(share_summary, on="year")

    # Supply stress probability by year.
    stress_prob = supply_stress.mean(axis=0)
    summary["p_supply_stress"] = stress_prob

    summary_path = os.path.join(out_dir, "summary_by_year.csv")
    summary.to_csv(summary_path, index=False)

    # Headline draws for selected years.
    pick_years = [2030, 2035, 2040, 2045]
    pick_idx = [int(np.where(years == y)[0][0]) for y in pick_years]

    draws = pd.DataFrame(
        {
            "draw": np.arange(ai.shape[0]),
            **{f"ai_twh_{y}": ai[:, idx] for y, idx in zip(pick_years, pick_idx)},
            **{f"ai_share_{y}": share[:, idx] for y, idx in zip(pick_years, pick_idx)},
            **{f"ai_gw_{y}": ai_gw[:, idx] for y, idx in zip(pick_years, pick_idx)},
            "max_additions_twh_per_year": max_additions,
        }
    )
    draws_path = os.path.join(out_dir, "draws_wide.csv")
    draws.to_csv(draws_path, index=False)

    # --- Plots ---
    # 1) AI electricity (TWh) percentile band.
    plt.figure(figsize=(8.5, 4.8))
    plt.fill_between(years, summary["ai_twh_p5"], summary["ai_twh_p95"], alpha=0.25, label="P5–P95")
    plt.plot(years, summary["ai_twh_p50"], linewidth=2.2, label="Median")
    plt.title("AI electricity demand (TWh/year), 2030–2045")
    plt.ylabel("TWh/year")
    plt.xlabel("Year")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "ai_twh_band.png"), dpi=200)
    plt.close()

    # 2) AI share of global electricity.
    plt.figure(figsize=(8.5, 4.8))
    plt.fill_between(years, 100 * summary["ai_share_p5"], 100 * summary["ai_share_p95"], alpha=0.25, label="P5–P95")
    plt.plot(years, 100 * summary["ai_share_p50"], linewidth=2.2, label="Median")
    plt.title("AI share of global electricity, 2030–2045")
    plt.ylabel("Percent of global electricity")
    plt.xlabel("Year")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "ai_share_band.png"), dpi=200)
    plt.close()

    # 3) Distribution of AI demand in 2045.
    plt.figure(figsize=(8.5, 4.8))
    sns.histplot(draws["ai_twh_2045"], bins=60, kde=False)
    plt.title("Distribution of AI electricity demand in 2045")
    plt.xlabel("AI electricity (TWh/year) in 2045")
    plt.ylabel("Draw count")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "ai_twh_2045_hist.png"), dpi=200)
    plt.close()

    # 4) Supply stress probability.
    plt.figure(figsize=(8.5, 4.8))
    plt.plot(years, 100 * summary["p_supply_stress"], linewidth=2.2)
    plt.title("Probability annual additions exceed sampled build rate")
    plt.ylabel("Probability (%)")
    plt.xlabel("Year")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "supply_stress_prob.png"), dpi=200)
    plt.close()

    # Headline stats for blog.
    def p(x, q):
        return float(np.percentile(x, q))

    headline = {
        "n_draws": int(cfg.n_draws),
        "ai_twh_2045_p50": p(draws["ai_twh_2045"], 50),
        "ai_twh_2045_p90": p(draws["ai_twh_2045"], 90),
        "ai_share_2045_p50": p(draws["ai_share_2045"], 50),
        "ai_share_2045_p90": p(draws["ai_share_2045"], 90),
        "p_ai_share_2045_gt_10pct": float((draws["ai_share_2045"] > 0.10).mean()),
        "p_ai_share_2045_gt_20pct": float((draws["ai_share_2045"] > 0.20).mean()),
        "p_ai_twh_2045_gt_5000": float((draws["ai_twh_2045"] > 5_000).mean()),
        "p_supply_stress_any_year": float(supply_stress.any(axis=1).mean()),
    }

    headline_path = os.path.join(out_dir, "headline.json")
    import json

    with open(headline_path, "w", encoding="utf-8") as f:
        json.dump(headline, f, indent=2)

    return {
        "out_dir": out_dir,
        "summary_path": summary_path,
        "draws_path": draws_path,
        "headline_path": headline_path,
        "plots_dir": plots_dir,
        "headline": headline,
    }
