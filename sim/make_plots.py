from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt

from norm_diffusion import run_scenarios


def plot_metric(ax, series_by_name, title, ylabel):
    for name, series in series_by_name.items():
        ax.plot(series, label=name)
    ax.set_title(title)
    ax.set_xlabel("timestep")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25)


def main():
    out = run_scenarios()

    metrics = [
        ("adoption_rate", "Adoption", "fraction of population"),
        ("compliance_rate", "Compliance among adopters", "fraction"),
        ("valid_provenance_rate", "Valid provenance among adopters", "fraction"),
        ("incident_rate", "Incident rate among adopters", "fraction per timestep"),
    ]

    figs_dir = Path(__file__).resolve().parents[1] / "docs" / "img"
    figs_dir.mkdir(parents=True, exist_ok=True)

    for key, title, ylabel in metrics:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        series_by_name = {name: data[key] for name, data in out.items()}
        plot_metric(ax, series_by_name, title, ylabel)
        ax.legend(loc="best", fontsize=9)
        fig.tight_layout()
        out_path = figs_dir / f"norm-diffusion-{key}.png"
        fig.savefig(out_path, dpi=160)
        plt.close(fig)
        print("wrote", out_path)


if __name__ == "__main__":
    main()
