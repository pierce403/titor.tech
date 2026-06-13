---
title: "Software wants a frontier"
date: 2026-06-13
categories:
  - Thesis
  - AI
  - Infrastructure
tags:
  - autoresearch
  - agents
  - open-source
  - rust
  - ffmpeg
  - rmpeg
  - security
---

A few weeks ago, autoresearch sounded like a clever trick: give an agent a goal, a metric, and a loop, then let it iterate.

Then [ECDSA.fail](https://ecdsa.fail/) made the idea feel less like a trick and more like a new institution.

The site is almost brutally simple. There is a hard technical problem, a public benchmark, a leaderboard, and a verification path. Humans and agents submit improvements. Bad attempts fall away. Good attempts become the new frontier.

The system does not care who wrote the better paragraph about their approach. It cares which circuit scores better.

That is the part worth paying attention to.

<!-- more -->

## Reality gets a vote

ECDSA.fail is an Eigen Labs benchmark arena for optimizing a reversible circuit used in elliptic curve point addition. The score is the qubit-Toffoli product. Lower is better.

As of this morning, the main challenge had moved from a baseline score of 10,758,874,395 to a current best score of 1,681,025,595. That is roughly a 6.4x improvement, or an 84.4% reduction. The public API showed 538 submissions, 321 accepted attempts, 319 promoted attempts, and 85 solvers.

Those numbers matter because they describe a process, not a press release.

The frontier moved because the problem had a shape:

- a narrow editable surface
- a reproducible setup command
- a benchmark command
- a score file
- a promotion rule
- a public history of attempts

That is enough structure for agents to do real work. They can try a change, measure it, keep it, revert it, combine it with another branch, and try again. Humans still matter. A lot. The interesting submissions read like strange little expedition logs: Codex ported one line of work, Claude found another compression route, Opus handled nonce hunting, humans named the branches and decided what was worth pursuing.

That is the future hiding inside the benchmark.

Autoresearch works when reality gets a vote.

## Open source has been missing this layer

Open source already has source control, issue trackers, package registries, CI, fuzzers, and review. What it lacks is a general frontier layer.

Most projects have vague goals:

- make it faster
- improve compatibility
- reduce memory bugs
- clean up the API
- modernize the codebase
- replace the unsafe parts

Everyone agrees with the goals. The work still stalls, because the goals are too large for a single pull request and too fuzzy for a swarm.

A frontier layer changes that. It turns ambition into thousands of measurable climbs.

For a compiler, the frontier might be test suite coverage, compile time, generated code quality, and accepted programs.

For a database, it might be query correctness, benchmark throughput, crash consistency, and replication behavior.

For a cryptography implementation, it might be formal verification coverage, constant time behavior, known answer tests, and circuit cost.

For media software, it might be corpus compatibility, decode hashes, probe accuracy, fuzz findings, and speed.

Once the frontier exists, agents can attack it. Not vaguely. Not through vibes. Through attempts.

Knowledge advances when attempts become legible.

## Why rmpeg exists

This morning we started [rmpeg](https://rmpeg.org/), an experiment to rewrite FFmpeg in Rust.

FFmpeg is invisible civilizational infrastructure. It touches video, audio, streaming, cameras, phones, browsers, podcasts, archives, creative tools, surveillance systems, medical workflows, and a depressing number of forgotten shell scripts. It is also a huge C attack surface that has accumulated decades of complexity.

The security dump yesterday made the problem hard to ignore. FFmpeg's own security page lists a long tail of CVEs, including recent 2025 entries and BIGSLEEP-reported issues. That does not make FFmpeg bad. It makes FFmpeg important. Important software gets attacked. Old unsafe code gives attackers plenty of room to work.

The April Fools version of the future was "rewrite it in Rust."

Fine. Let's take the joke seriously.

One agent will not rewrite FFmpeg. One startup probably will not either. FFmpeg is too broad, too weird, too full of edge cases, and too deeply embedded in the world.

A swarm might.

But only if the swarm has a frontier.

## A rewrite as a scoreboard

rmpeg does not begin by claiming to replace FFmpeg. It begins by measuring itself against FFmpeg.

The current Phase 1 metric is simple: how many FFmpeg-accepted sample media files in the upstream FATE corpus can rmpeg inspect correctly?

This morning, rmpeg reported:

- 617 media matches out of 2,154 FFmpeg-accepted sample files
- 28.6% Phase 1 sample media progress
- 2,511 files checked
- 965 total corpus passes
- metadata support for WAV, MP3, FLAC, Ogg audio, MP4/MOV, H.264/AAC, IVF video, and a growing list of image formats
- early probe benchmarks around 56x to 60x faster than FFmpeg on small metadata cases

The decode layer is still early. Many compressed formats are recognized but not decoded. Filters, seeking, resampling, remuxing, and most codec behavior are still ahead.

Good. That is the point.

A measurable frontier gives the swarm somewhere to stand.

The work breaks down into small climbs:

- one container
- one codec
- one probe field
- one decode hash
- one weird file from FATE
- one fuzz crash
- one benchmark regression
- one security class

Each improvement is small. The frontier moves anyway.

## Autoresearch curates attempts

Wikis curate what we know. Autoresearch curates what works.

That distinction is worth sitting with.

A wiki stores claims, sources, links, contradictions, and concepts. It helps a community remember what it believes and why.

An autoresearch system stores attempts. It remembers which patches improved the score, which failed, which were reverted, which merged cleanly, which broke a hidden invariant, and which became the parent of the next frontier branch.

That is a different kind of knowledge. It is practical, empirical, and often lost.

Most failed attempts vanish into private chats, abandoned branches, local notebooks, and the heads of tired maintainers. That loss is expensive. It means the next person repeats the same mistake. It means a clever near miss dies before another agent can combine it with a different near miss.

Autoresearch makes attempts durable.

A good frontier system should remember:

- the patch
- the score
- the logs
- the failure mode
- the parent attempt
- the machine environment
- the human reviewer
- the agent model
- the reason it was promoted or rejected

That history becomes a substrate for future search.

## The software ecosystem after heroism

Open source has relied on heroism for too long.

A few maintainers absorb the complexity of systems used by billions of people. They triage bugs, review patches, fight spam, respond to security reports, and carry undocumented context in their heads. Then the world acts surprised when critical infrastructure is underfunded, under-reviewed, and full of ancient traps.

Agent swarms do not remove the need for maintainers. They make maintainers more powerful.

The maintainer's role shifts toward frontier design:

- What counts as progress?
- Which tests define compatibility?
- Which benchmarks matter?
- Which areas are safe for agents to edit?
- Which security properties are mandatory?
- Which promoted attempts deserve human review?
- Which project values should the swarm preserve?

That is a better use of scarce human judgment.

Humans set direction. Machines explore the search space. Reality vetoes bad ideas. Maintainers decide what enters the commons.

That is the happy path.

## From projects to civilization

This pattern does not stop at software.

Science needs replication frontiers. Medicine needs outcome frontiers. Education needs learning frontiers. Policy needs measurable civic frontiers. Security needs exploit and proof frontiers. Knowledge bases need provenance and contradiction frontiers.

The shared pattern is simple:

1. Define the domain.
2. Define the tests reality is allowed to run.
3. Let many minds and machines attempt improvements.
4. Preserve the full attempt history.
5. Promote what survives verification.
6. Fold the result back into the knowledge base.

That is how human knowledge gets built when the rate of attempts explodes.

The old internet organized pages. The next internet can organize attempts.

ECDSA.fail shows the shape in cryptography. rmpeg applies it to one of the most important media stacks on Earth. The same pattern can rebuild other brittle systems if we give agents measurable terrain, strong safety boundaries, and honest scoreboards.

Software wants a frontier.

Give it one, and the swarm starts climbing.
