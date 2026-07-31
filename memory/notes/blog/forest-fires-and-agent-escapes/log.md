# Research and editorial log

## 2026-07-31 — John Titor

- Goal: Establish a reusable blog-research workflow and reconstruct the evidence, narrative, and publication blockers behind the existing draft.
- Sources added: Separate first-party records from Hugging Face, OpenAI, JFrog, Anthropic, Google, the U.S. Forest Service, and the National Park Service; the original Drossel–Schwabl paper; later broken-scaling work; and the Veritasium framing source.
- Claims added or changed: Separated incident facts from the article's substrate thesis; added counterevidence about Anthropic's non-deliberate escapes; scoped Yellowstone acreage; marked the model's criticality claim disputed; marked Google's repository-context claim open.
- Narrative decision: Keep the “spark versus accumulated fuel” cascade frame, but explicitly subordinate it to correct evaluation containment and state where the analogy breaks.
- Wording to narrow or drop: “same kind of spark ... burn 1.4 million acres,” universal power-law wording, unsupported agent-swarm capability details, and repository-level Google context without a primary source.
- Failed or misleading paths: GitHub code search was indexed before the latest draft commit, so direct commit and file reads were required. The old `security.googleblog.com` URL was difficult to inspect, while Google's canonical `blog.google` copy exposed the relevant sections. Veritasium is useful framing but not sufficient authority for wildfire history or statistical physics.
- Commands and validation results: `quick_validate.py skills/write-blog-post` passed; `git diff --check` passed; `source activate.sh && ./build.sh` completed successfully. MkDocs emitted pre-existing informational warnings about `tags.md` being outside navigation and absolute image links in older posts.
- Remaining risks: Living incident reports may change; the analogy currently carries more evidentiary weight in the prose than the sources justify; several broad claims remain in the draft without explicit support.
- Next action: Revise the draft against `claims.md`, then recheck every first-party incident page and run the publication checklist.

## 2026-07-31 — John Titor — evidence-tightening pass

- Goal: Resolve the draft's open evidence and framing issues while preserving its cascade-security thesis.
- Sources added or rechecked: Rechecked the Hugging Face technical timeline, OpenAI incident account, Anthropic incident review, Google Chrome architecture post, Yellowstone fire data, both forest-fire-model papers, and Forest Service suppression history. Added the NPS history of Yellowstone fire management as counterevidence (S13).
- Claims changed: Qualified the Drossel–Schwabl criticality claim (C08); scoped Yellowstone acreage and conditions (C09/C15); added Anthropic's explicit non-escape finding and divergent model behavior (C06); superseded the unsupported Google repository-context attribution (C12/C18); narrowed the agent-speed inference to Hugging Face's measured campaign volume (C13); separated Yellowstone 1988 from suppression-created-fuel claims (C19).
- Narrative decision: Keep the spark-and-fuel framing, but make its scientific, ecological, and operational boundaries explicit. Treat synthetic red-team drills—not real incidents—as the controlled-burn analogue.
- Wording narrowed or dropped: Removed the universal power-law statement, one-spark Yellowstone account, human-versus-agent timing comparison, “agent swarm” and hypothesis-forking claims, unsupported Google repository practice, and the implication that model behavior is irrelevant.
- Failed or misleading paths: The original “Smokey Bear mistake” heading conflated a historical Forest Service suppression policy with modern prevention messaging. Renamed it and recorded the NPS finding that suppression did not significantly increase fuel loads across most of Yellowstone.
- Commands and validation results: No TODO/TK/FIXME/citation markers; every post URL resolves to the source ledger; every claim evidence ID resolves; no claims remain `open`; `quick_validate.py skills/write-blog-post` passed; `git diff --check` passed; `source activate.sh && ./build.sh` passed. The build emitted only pre-existing navigation and older absolute-image-link notices.
- Remaining risks: The living incident pages may change before publication, and the final title/framing still require Dean's approval before removing `DRAFT:`.
- Next action: Push the evidence-aligned draft for Dean's review, then perform a final living-source recheck before publication.
