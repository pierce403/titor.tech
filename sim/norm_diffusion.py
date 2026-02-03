"""Agent adoption + safety norm diffusion ABM.

Focus: permission manifests + provenance practices under adversarial pressure.

This is a *first-pass* model intended for qualitative insight and parameter sweeps.

State per agent i:
- adopted[i]      bool: uses agentic automation
- s[i]            float in [0,1]: internalized safety norm strength
- compliant[i]    bool: uses permission manifests + provenance tagging when adopted
- exposed[i]      float in [0,1]: current adversarial exposure level (decays)

Dynamics (discrete timesteps):
- Adoption is a utility choice with social influence and friction.
- Norm strength diffuses on the graph and responds to incidents/audits.
- Adversary can seed unsafe tooling or messaging, increasing exposure; exposure
  reduces norm strength and increases likelihood of non-compliance and acceptance
  of forged provenance.

Outputs:
- adoption_rate(t)
- compliance_rate_among_adopters(t)
- valid_provenance_rate_among_actions(t)
- incident_rate(t)

Dependencies: numpy, networkx
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import math
import random

import numpy as np
import networkx as nx


@dataclass
class Params:
    # population / graph
    n: int = 800
    graph: str = "small_world"  # small_world|scale_free|erdos_renyi
    seed: int = 7

    # adoption
    base_benefit: float = 1.0
    social_weight: float = 1.6
    risk_weight: float = 1.1
    adopt_noise: float = 0.35
    adopt_threshold: float = 0.6

    # safety norm + compliance
    init_norm_mean: float = 0.35
    init_norm_sd: float = 0.15
    norm_diffusion: float = 0.22  # pull toward neighbor mean
    norm_decay: float = 0.02
    compliance_threshold: float = 0.55
    manifest_friction: float = 0.20
    default_on_manifest_bonus: float = 0.12  # offsets perceived friction

    # incidents + feedback
    base_incident_prob: float = 0.010  # per-timestep per adopter
    unsafe_multiplier: float = 6.0
    incident_norm_boost: float = 0.10
    audit_rate: float = 0.00  # fraction of adopters audited per step
    audit_norm_boost: float = 0.07
    audit_compliance_boost: float = 0.12

    # adversary
    adversary: bool = False
    adv_seed_frac: float = 0.03
    adv_target: str = "hubs"  # hubs|random
    exposure_decay: float = 0.50
    exposure_increase: float = 0.85
    exposure_norm_penalty: float = 0.20
    forge_accept_bias: float = 0.45  # higher => more likely accept forged provenance

    # simulation
    T: int = 120


def make_graph(p: Params) -> nx.Graph:
    rng = np.random.default_rng(p.seed)
    if p.graph == "small_world":
        # Watts–Strogatz: clustered + short path lengths
        k = max(4, int(round(math.log(p.n) * 2)))
        g = nx.watts_strogatz_graph(p.n, k, 0.08, seed=p.seed)
    elif p.graph == "scale_free":
        g = nx.barabasi_albert_graph(p.n, 3, seed=p.seed)
    elif p.graph == "erdos_renyi":
        g = nx.erdos_renyi_graph(p.n, 0.015, seed=p.seed)
    else:
        raise ValueError(f"unknown graph: {p.graph}")

    # ensure connected for neighbor-mean logic
    if not nx.is_connected(g):
        largest = max(nx.connected_components(g), key=len)
        g = g.subgraph(largest).copy()
    return g


def _sigmoid(x):
    """Sigmoid that works on scalars or numpy arrays."""
    return 1.0 / (1.0 + np.exp(-x))


def simulate(p: Params) -> Dict[str, np.ndarray]:
    random.seed(p.seed)
    np.random.seed(p.seed)

    g = make_graph(p)
    n = g.number_of_nodes()

    # state
    s = np.clip(np.random.normal(p.init_norm_mean, p.init_norm_sd, size=n), 0.0, 1.0)
    adopted = np.zeros(n, dtype=bool)
    compliant = np.zeros(n, dtype=bool)
    exposure = np.zeros(n, dtype=float)

    # choose adversary seeds (unsafe tooling + messaging)
    adv_seeds: List[int] = []
    if p.adversary:
        m = max(1, int(round(p.adv_seed_frac * n)))
        if p.adv_target == "hubs":
            deg = np.array([g.degree(i) for i in range(n)])
            adv_seeds = list(np.argsort(-deg)[:m])
        else:
            adv_seeds = random.sample(range(n), m)
        exposure[adv_seeds] = 1.0

    # metrics
    adoption_rate = np.zeros(p.T)
    compliance_rate = np.zeros(p.T)
    valid_prov_rate = np.zeros(p.T)
    incident_rate = np.zeros(p.T)

    neighbors = [list(g.neighbors(i)) for i in range(n)]

    for t in range(p.T):
        # --- norm diffusion (neighbor averaging) + decay
        neigh_mean = np.array([
            s[i] if len(neighbors[i]) == 0 else float(np.mean(s[neighbors[i]]))
            for i in range(n)
        ])
        s = s + p.norm_diffusion * (neigh_mean - s) - p.norm_decay * (s - 0.0)

        # --- adversary exposure spreads via edges
        if p.adversary:
            # exposure propagates from exposed nodes to neighbors
            new_exposure = exposure.copy() * (1.0 - p.exposure_decay)
            for i in range(n):
                if exposure[i] <= 1e-9:
                    continue
                for j in neighbors[i]:
                    if random.random() < 0.12:
                        new_exposure[j] = max(new_exposure[j], min(1.0, exposure[i] * p.exposure_increase))
            exposure = np.clip(new_exposure, 0.0, 1.0)
            # exposure reduces norm strength
            s = np.clip(s - p.exposure_norm_penalty * exposure, 0.0, 1.0)

        # --- compliance decision (if adopted)
        # default-on manifests: effective friction is reduced for higher-norm agents
        effective_friction = max(0.0, p.manifest_friction - p.default_on_manifest_bonus)
        compliant = adopted & (s >= p.compliance_threshold)

        # --- adoption decision (non-adopters evaluate utility)
        frac_adopted_neigh = np.array([
            0.0 if len(neighbors[i]) == 0 else float(np.mean(adopted[neighbors[i]]))
            for i in range(n)
        ])

        # expected incident risk depends on compliance (if they adopted) and adversary exposure
        # (non-adopters estimate risk from neighborhood incident climate via neighbor adoption)
        est_risk = p.base_incident_prob * (1.0 + 2.0 * frac_adopted_neigh)

        utility = (
            p.base_benefit
            + p.social_weight * frac_adopted_neigh
            - p.risk_weight * est_risk
            - effective_friction * (s >= p.compliance_threshold)  # high-norm agents anticipate overhead
        )
        utility = utility + np.random.normal(0.0, p.adopt_noise, size=n)

        adopt_prob = _sigmoid((utility - p.adopt_threshold) * 2.2)
        will_adopt = (np.random.random(size=n) < adopt_prob)
        adopted = adopted | will_adopt

        # --- incidents happen among adopters
        inc = np.zeros(n, dtype=bool)
        for i in range(n):
            if not adopted[i]:
                continue
            pr = p.base_incident_prob
            if not compliant[i]:
                pr *= p.unsafe_multiplier
                # adversarial exposure increases incident likelihood when unsafe
                pr *= (1.0 + 0.9 * exposure[i])
            if random.random() < pr:
                inc[i] = True

        # --- feedback: incidents + audits strengthen norms
        if inc.any():
            s[inc] = np.clip(s[inc] + p.incident_norm_boost, 0.0, 1.0)
            # local learning from incidents: neighbors update too
            for i in np.where(inc)[0].tolist():
                for j in neighbors[i]:
                    if random.random() < 0.35:
                        s[j] = min(1.0, s[j] + 0.35 * p.incident_norm_boost)

        if p.audit_rate > 0:
            adopters = np.where(adopted)[0]
            k = int(round(p.audit_rate * len(adopters)))
            if k > 0:
                audited = np.random.choice(adopters, size=k, replace=False)
                s[audited] = np.clip(s[audited] + p.audit_norm_boost, 0.0, 1.0)
                # audits also nudge compliance by raising perceived threshold margin
                s[audited] = np.clip(s[audited] + p.audit_compliance_boost, 0.0, 1.0)

        # --- provenance validity for actions this timestep
        # assume each adopter performs one action.
        # valid provenance if compliant and not accepting a forged chain.
        valid = np.zeros(n, dtype=bool)
        for i in range(n):
            if not adopted[i]:
                continue
            if compliant[i]:
                # still may accept a forged upstream provenance when exposed and low-norm
                forge_prob = 0.0
                if p.adversary:
                    forge_prob = exposure[i] * (p.forge_accept_bias * (1.0 - s[i]))
                valid[i] = (random.random() > forge_prob)
            else:
                valid[i] = False

        # --- record metrics
        adoption_rate[t] = float(np.mean(adopted))
        compliance_rate[t] = float(np.mean(compliant[adopted])) if adopted.any() else 0.0
        valid_prov_rate[t] = float(np.mean(valid[adopted])) if adopted.any() else 0.0
        incident_rate[t] = float(np.mean(inc[adopted])) if adopted.any() else 0.0

    return {
        "adoption_rate": adoption_rate,
        "compliance_rate": compliance_rate,
        "valid_provenance_rate": valid_prov_rate,
        "incident_rate": incident_rate,
    }


def run_scenarios() -> Dict[str, Dict[str, np.ndarray]]:
    """A small battery of scenarios used in the accompanying blog post."""
    base = Params()

    scenarios: Dict[str, Params] = {
        "baseline_default_on": base,
        "high_friction": Params(manifest_friction=0.55, default_on_manifest_bonus=0.05),
        "adversary_hub_seed": Params(adversary=True, adv_target="hubs"),
        "adversary_plus_audits": Params(adversary=True, adv_target="hubs", audit_rate=0.08),
    }

    out: Dict[str, Dict[str, np.ndarray]] = {}
    for name, p in scenarios.items():
        out[name] = simulate(p)
    return out
