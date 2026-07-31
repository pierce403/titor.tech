---
summary: Compact map of durable Titor Technologies context, research dossiers, and work logs.
directories:
  knowledge: Stable mission, terminology, persona, and working conventions.
  blog_notes: Per-post research, claims, narratives, framing, and editorial history.
  logs: Dated process reviews and lessons.
index: rg
---

# MEMORY.md

Start here, then load only the context relevant to the task.

| Path | Purpose | Read when |
| --- | --- | --- |
| `KNOWLEDGE.md` | Stable mission, voice, terminology, and John Titor context | Editing public content or making mission-level decisions |
| `memory/notes/blog/index.md` | Catalog of blog dossiers | Creating, revising, or reviewing a post |
| `memory/notes/blog/<slug>/` | Brief, source ledger, claim ledger, and work log for one post | Working on that post |
| `memory/logs/recurse-bot-checks.md` | Decisions from periodic Recurse etiquette reviews | Beginning meaningful agent-process work |

Search before guessing:

```bash
rg -n "<topic|claim|source|slug>" MEMORY.md KNOWLEDGE.md memory
```

Keep memory useful and restrained. Record provenance and decisions, not copied archives. Update misleading notes when evidence changes, and let Git preserve the old version.
