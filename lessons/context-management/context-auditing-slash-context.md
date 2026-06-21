---
id: context-auditing-slash-context
created: 2026-06-03
status: active
supersedes: null
category: context-management
sources:
  - transcripts/john-kim/how-to-save-90-of-claude-code-token-usage_20260603.txt
  - transcripts/simon-scrapes/master-80-of-claude-code-just-learn-these-15-things_20260603.txt
---

# Run /context to Audit What's Eating Your Window

## TL;DR

`/context` shows exactly what is consuming the window (CLAUDE.md size, MCPs, files), so you can trim bloat proactively instead of discovering it after performance degrades.

## Why it matters

Context bloat is silent: an oversized CLAUDE.md or an unused MCP can eat a meaningful slice of every fresh session before you type a word, accelerating context rot. `/context` breaks the consumption down by category so you can see the culprit and act. It pairs with `context-rot-prevention-compact-proactively`.

## How to apply

Run `/context` and review the per-category breakdown. Trim an oversized CLAUDE.md (push detail into `references/` files loaded on demand), disable MCPs you are not using, `/clear` between unrelated tasks, and `/compact` (naming what to keep) after a long same-topic session. Re-check `/context` after trimming to confirm the win.
