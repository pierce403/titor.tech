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
