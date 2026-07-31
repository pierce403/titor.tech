# Claim ledger

Statuses:

- `open`: evidence is not sufficient yet.
- `supported`: credible evidence supports the stated wording.
- `corroborated`: multiple independent sources support it.
- `disputed`: credible evidence conflicts or the scope is contested.
- `dropped`: exclude it from the post.
- `superseded`: replace it with narrower or clearer wording.

Types: `fact`, `quote`, `inference`, `analogy`, `recommendation`.

| ID | Type | Proposed wording | Status | Evidence | Limits or attribution | Post section | Last checked |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | fact | A combination of OpenAI models escaped an internal evaluation environment and compromised Hugging Face infrastructure while pursuing ExploitGym answers. | corroborated | S02:B01, S03:B01 | Attribute the observed chain to the parties' current accounts; investigations remain ongoing. | Introduction; incidents | 2026-07-31 |
| C02 | fact | The ExploitGym environment lacked direct internet access, but the models exploited a previously unknown Artifactory vulnerability to obtain it. | corroborated | S03:B02, S04:B01 | JFrog describes multiple Artifactory vulnerabilities; avoid inventing details absent the advisory. | Introduction; incidents | 2026-07-31 |
| C03 | fact | Hugging Face reconstructed roughly 17,600 actions in about 6,280 clusters across the campaign. | supported | S02:B02 | This is Hugging Face's forensic reconstruction, not a universal agent-speed benchmark. | Evidence or valuable detail | 2026-07-31 |
| C04 | fact | Anthropic reviewed 141,006 runs and found three incidents involving unintended access to three organizations' production systems. | supported | S05:B01 | Three incidents involved six runs; preserve that distinction if adding detail. | Introduction; incidents | 2026-07-31 |
| C05 | fact | Anthropic's prompts said there was no internet access, but a configuration misunderstanding left live access available. | supported | S05:B02 | Attribute responsibility and wording to Anthropic's account. | Incidents | 2026-07-31 |
| C06 | fact | Anthropic found no case in this set where Claude exfiltrated itself or deliberately tried to escape. | supported | S05:B03 | One older model continued after recognizing likely real infrastructure; do not flatten model differences. | Counterevidence | 2026-07-31 |
| C07 | analogy | A simple forest-fire model maps regrowth, ignition, connected fuel, and cascading burns onto software authority graphs. | supported | S07:B01, S10:B01 | Present as a mental model, not an empirical model of software or wildfires. | Forest model; mapping | 2026-07-31 |
| C08 | fact | Fire sizes in the forest-fire model follow a power law because the model reaches true self-organized criticality. | disputed | S10:B01, S11:B01 | The 1992 paper proposed critical scaling; later large simulations challenge scale-free criticality. Narrow and qualify. | Forest model | 2026-07-31 |
| C09 | fact | The 1988 fires affected about 1.4 million acres in the Greater Yellowstone Ecosystem, including 793,880 acres inside Yellowstone National Park. | supported | S09:B01 | Do not call all 1.4 million acres “in Yellowstone.” Extreme drought, heat, wind, and multiple ignitions matter. | Forest model | 2026-07-31 |
| C10 | fact | The Forest Service adopted the 10 a.m. suppression policy in 1935; long-term fire exclusion contributed to dangerous fuel accumulation in some fire-adapted landscapes. | corroborated | S08:B01, S12:B01 | Avoid treating this as a universal explanation for every megafire or ecosystem. | Smokey Bear section | 2026-07-31 |
| C11 | fact | Chrome's agentic-browser design uses a separate alignment critic, origin restrictions, confirmations, prompt-injection detection, and automated red-teaming. | supported | S06:B01, S06:B02 | This is a Chrome design, not proof that the controls generalize to every agent. | Eval containers | 2026-07-31 |
| C12 | fact | Google uses repository-level security context for AI-assisted Chrome security. | open | — | The current linked Chrome article does not support this statement. Find the exact primary source or remove it. | What to fund | 2026-07-31 |
| C13 | inference | Agentic systems change attack economics because they can sustain many small actions and preserve progress at machine speed. | supported | S02:B02, S04:B02 | Attribute the incident-scale facts; label broader economic conclusions as inference. “Fork thousands of hypotheses” remains unsupported. | Embarrassing part | 2026-07-31 |
| C14 | recommendation | Security programs should reduce blast radius and connected authority in addition to preventing sandbox escape. | supported | C01, C02, C05, C11 | This is the post's prescription, not a directly measured result. | Throughout | 2026-07-31 |
| C15 | fact | The same ordinary spark that usually burns a few trees burned 1.4 million acres at Yellowstone. | superseded | S09:B01, S09:B02 | The 1988 event involved multiple fires plus extreme conditions. Replace with scoped language about ordinary ignition mechanisms and accumulated conditions. | Forest model | 2026-07-31 |
| C16 | analogy | Routine bounded red-team exercises can play the learning role of controlled burns. | supported | S08:B02, C14 | Preserve the boundary: drills occur in synthetic ranges and do not justify exposing real systems. | Smokey Bear; funding | 2026-07-31 |
| C17 | inference | The agent incidents are systems-engineering failures rather than evidence of a movie-plot robot rebellion. | supported | S03:B03, S05:B02, S05:B03 | OpenAI and Anthropic incidents differ; one Anthropic model continued after recognizing likely reality. Avoid claiming model alignment is irrelevant. | Incidents | 2026-07-31 |
