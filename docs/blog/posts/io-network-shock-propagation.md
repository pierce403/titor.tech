---
title: Cascading supply shocks with a GPU-friendly input–output network model
date: 2026-02-02
categories:
  - Analysis
tags:
  - economics
  - input-output
  - supply-chain
  - commodities
  - networks
  - simulation
  - pytorch
---

Modern economies aren’t just “a bunch of industries.” They’re *networks of dependencies*.

A shock in one upstream node (energy, fertilizer, chips, shipping, critical metals) doesn’t stay local — it propagates through intermediate inputs, forcing downstream sectors to reduce output, which then feeds back upstream as reduced demand.

This post is a first-pass, **matrix-first** model of that cascade, designed to be fast (and GPU-friendly when PyTorch+CUDA is available).

<!-- more -->

## The model (first pass)

We represent the world as a multi-region, multi-sector input–output (IO) system.

- Each node is a *(country, sector)* pair.
- `A[i, j]` is the technical coefficient: units of input *i* required per unit of output *j*.
- `y[j]` is final demand for node *j* (households, government, investment, etc.).

In the classic Leontief model (no constraints), gross output `x` satisfies:

\[
  x = A x + y \quad \Rightarrow \quad x = (I - A)^{-1} y
\]

### Capacity shocks → cascading constraints

A supply shock reduces the maximum feasible output of one or more nodes.

Let `cap[j]` be the post-shock capacity (e.g. baseline output times `(1 - shock)`).

We then iterate a simple feasibility fixed-point:

\[
  req = A x + y \\
  x_{t+1} = \min(cap, req)
\]

Interpretation:

- `req` is “what the economy would like to produce” given the current level of activity.
- `min(cap, req)` enforces capacity constraints.
- Shortages upstream reduce feasible downstream production; the reduced downstream activity reduces input demand upstream; the system settles to a constrained fixed point.

This is **not** a full equilibrium model:

- no prices
- no substitution across inputs
- no inventory dynamics

…but it’s a useful *stress-test lens* and it runs in a few milliseconds for moderate problem sizes.

## Implementation (matrix ops; GPU when available)

I put a small reference implementation in the repo:

- `scripts/io_shock_propagation.py`

It prefers **PyTorch** (and will use CUDA if available) but falls back to NumPy CPU.

### Run the demo

```bash
# Use the repo venv python (has numpy)
./venv/bin/python scripts/io_shock_propagation.py --demo

# If you have torch installed and a CUDA GPU:
./venv/bin/python scripts/io_shock_propagation.py --demo --cuda

# Override shock list: country,sector,reduction
./venv/bin/python scripts/io_shock_propagation.py --demo \
  --shock 1,2,0.6 \
  --shock 4,7,0.3
```

### Output

The demo prints a JSON report: total output loss, unmet final demand, and the most impacted nodes.

Here’s an example run (synthetic MRIO, 8 countries × 12 sectors, two shocks):

```json
{
  "device": "numpy-cpu",
  "n": 96,
  "iters": 15,
  "converged": true,
  "total_baseline_output": 1468.6268,
  "total_realized_output": 1453.2307,
  "total_output_loss": 15.3961,
  "total_unmet_final": 8.3062,
  "top_output_loss": [["C1:S2", 6.9492], ["C4:S7", 1.4850], ...],
  "top_unmet_final": [["C1:S2", 6.8944], ["C4:S7", 1.4119], ...]
}
```

Even in this toy network, the first-order shocks create **second-order losses** in other nodes — the “blast radius” isn’t just the directly shocked sectors.

## Key takeaways (from this first pass)

1. **The cascade is a fixed point, not a single hop.**
   You don’t just look at immediate customers of a shocked sector; you iterate until constraints settle.

2. **Most of the pain is concentrated.**
   Output loss and unmet final demand often concentrate in a small set of nodes, especially when the shock hits a node that is (a) highly central as an input supplier, or (b) has few substitutes.

3. **There’s a distinction between “output loss” and “unmet final demand.”**
   Some reductions are simply reduced intermediate activity (less stuff being produced because the network contracts); unmet final demand is the part consumers/“the outside world” actually feels.

4. **GPU matters when you scale.**
   Once you move from a toy MRIO (hundreds of nodes) to real MRIO tables (thousands to tens of thousands), the core operations are matrix multiplies and linear solves — perfect for GPU acceleration.

## Next steps (to make it real)

This is deliberately minimal. Next iterations that would make it more decision-useful:

- **Use real MRIO data** (OECD ICIO, WIOD, Eora) for `A` and `y`.
- **Commodity layer**: add explicit commodity nodes (oil, gas, fertilizer, copper, etc.) and map them into sectors.
- **Rationing rules**: decide who gets scarce inputs first (final demand vs intermediate, strategic sectors, domestic bias).
- **Inventories / time**: add stock buffers and multi-period dynamics.
- **Scenario library**: structured shocks (shipping lane closure, energy embargo, drought, sanctions) with reusable parameter sets.

If you want this model to answer “what happens if X breaks?”, those additions are where the value is.
