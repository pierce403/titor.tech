---
title: "Agent adoption & safety norms as a contagion: permission manifests, provenance, and adversaries"
date: 2026-02-02
categories:
  - Research
tags:
  - agents
  - safety
  - provenance
  - permissioning
  - simulation
---

As we ship more *agentic* automation into real networks—teams, orgs, open-source ecosystems—two things diffuse at once:

1. **Adoption**: who starts using agents to do work.
2. **Norms**: whether people use agents *safely*, e.g. with **permission manifests** and **provenance**.

Those two diffusions are coupled. Safety practices can ride on the back of adoption… or get outcompeted by convenience, especially under targeted adversarial pressure.

This post shares a first-pass agent-based model (ABM) that makes that coupling explicit.

<!-- more -->

## The model (first pass)

We simulate a population of agents on a social graph (small-world by default). Each node represents a person/team adopting agentic automation.

Each simulated actor has:

- **adopted** ∈ {0,1}: are they using agents?
- **safety norm strength** *s* ∈ [0,1]: how strongly they internalize “do it safely”.
- **compliance** ∈ {0,1}: when adopted, do they use a **permission manifest + provenance tagging**?
- **adversarial exposure** *e* ∈ [0,1]: how much “unsafe shortcut” pressure they’re under (decays, spreads).

**Permission manifests** are modeled as a friction term: they impose workflow overhead unless they’re close to “default-on” (good tooling, good UI, good automation).

**Provenance** is modeled as a per-action property: compliant adopters usually emit valid provenance, but under exposure and low norms they can accept *forged* provenance chains.

**Incidents** are more likely when actors are adopted-but-noncompliant (unsafe multiplier). Incidents (and audits) increase norm strength locally and via neighbors.

Code: `sim/norm_diffusion.py` (plus `sim/make_plots.py` to regenerate figures).

## Scenarios

We ran four scenarios with identical starting conditions:

1. **baseline_default_on**: low friction + “default-on” bonus
2. **high_friction**: manifests are meaningfully annoying
3. **adversary_hub_seed**: attacker seeds high-degree hubs with unsafe tooling/messaging
4. **adversary_plus_audits**: same attacker, but with light ongoing audits

Figures below show time series for adoption, compliance, provenance validity, and incidents.

### Adoption

![](/img/norm-diffusion-adoption_rate.png)

### Compliance among adopters (permission manifests + provenance enabled)

![](/img/norm-diffusion-compliance_rate.png)

### Valid provenance among actions

![](/img/norm-diffusion-valid_provenance_rate.png)

### Incidents

![](/img/norm-diffusion-incident_rate.png)

## Key findings (qualitative)

### 1) Adoption can saturate while safety collapses
Even when adoption grows smoothly, **compliance can drop** if permission manifests feel like “optional overhead”. In the model, a moderate increase in manifest friction causes a large decrease in sustained compliance.

Interpretation: if manifests/provenance are not *boring by default*, they become a tax that people route around—especially when their neighbors normalize skipping them.

### 2) Targeted attacks on hubs are disproportionately effective
When the adversary seeds **high-degree nodes**, exposure spreads faster and reaches more of the network early. That shifts local equilibria toward noncompliance (and raises the rate of “valid-looking but forged provenance”).

Interpretation: in real ecosystems, “influencers” are not only people; they are:

- popular repos
- widely copied agent templates
- default configs in agent frameworks
- LLM prompt packs

If those hubs omit manifests/provenance, they don’t just add risk—they *set the norm*.

### 3) Lightweight audits are a strong stabilizer
Adding a small audit rate (random checks of adopters) meaningfully increases norm strength and compliance, even under adversarial pressure, reducing incident rates.

Interpretation: you don’t need perfect enforcement. You need *credible detection* plus feedback loops that increase the local cost of noncompliance.

### 4) Provenance fails “silently” without strong norms
In the model, provenance validity is not only about emitting signatures; it is about **refusing forged chains**.

If safety norms are weak, actors accept forged provenance at high rates when exposed.

Interpretation: provenance is a socio-technical system. Cryptography helps, but if users routinely click through warnings, provenance becomes theater.

## What this suggests for real systems

1. **Make manifests/provenance default-on and low-friction**.
   - Aim for “safe by construction” pipelines where manifest generation is automatic.
   - Treat “turning off provenance” like disabling seatbelts: possible, but costly and visible.

2. **Defend the hubs**.
   - Curate and harden the top templates/repos.
   - Add provenance checks to package managers, agent registries, and framework defaults.

3. **Add small-but-real enforcement**.
   - Periodic audits, automated policy checks, and incident postmortems that update norms.

4. **Measure what matters**.
   - Adoption rate alone is the wrong KPI.
   - Track compliance, provenance validity, and incident rates (plus leading indicators like bypass attempts).

## Limitations / next steps

This is intentionally simple. A better model would:

- separate *individual* vs *institutional* norms
- include heterogeneous roles (operators, security teams, vendors)
- model multiple competing toolchains (safe vs unsafe) with explicit switching costs
- include “shadow usage” (unreported agents)
- represent provenance as a graph of artifacts with verification policies

If you want to play with it, start with `Params` in `sim/norm_diffusion.py` and sweep:

- `manifest_friction`, `default_on_manifest_bonus`
- `adv_seed_frac`, `adv_target`
- `audit_rate`

## Reproducing the figures

From the repo root:

```bash
./venv/bin/pip install numpy matplotlib networkx
./venv/bin/python sim/make_plots.py
```

---

If you’re building agent systems and want to pressure-test your permissioning and provenance design against “realistic laziness + realistic attackers”, this is the kind of model worth keeping in your toolbox.
