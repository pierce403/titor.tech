#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os

import sys

# Allow running from repo root without installing as a package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from energy_ai_stress import ModelConfig, run_and_save


def main():
    ap = argparse.ArgumentParser(description="Monte Carlo stress test: global energy + AI compute demand (2030–2045)")
    ap.add_argument("--out", default="docs/analysis/energy-ai-stress", help="Output directory")
    ap.add_argument("--n", type=int, default=50_000, help="Number of Monte Carlo draws")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    cfg = ModelConfig(n_draws=args.n, seed=args.seed)
    out_dir = os.path.abspath(args.out)

    res = run_and_save(out_dir=out_dir, cfg=cfg)
    print("Wrote:")
    print("-", res["summary_path"])
    print("-", res["draws_path"])
    print("-", res["headline_path"])
    print("- plots in", res["plots_dir"])
    print("Headline:")
    for k, v in res["headline"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
