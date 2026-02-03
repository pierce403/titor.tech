# Norm diffusion simulation (first pass)

This folder contains a small agent-based model (ABM) exploring coupled diffusion of:

- **agent adoption** (who starts using agentic automation)
- **safety norms** (permission manifests + provenance practices)

It is designed to be *qualitative* and easy to modify.

## Files

- `norm_diffusion.py` — model + a few reference scenarios
- `make_plots.py` — generates the PNGs used in the blog post

## Run

```bash
./venv/bin/pip install numpy matplotlib networkx
./venv/bin/python sim/make_plots.py
```

Outputs are written into `docs/img/`.
