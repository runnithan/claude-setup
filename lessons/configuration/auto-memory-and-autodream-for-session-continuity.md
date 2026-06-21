---
id: auto-memory-and-autodream-for-session-continuity
created: 2026-04-25
status: superseded
superseded_by: auto-dream-memory-consolidation
supersedes: null
category: configuration
sources:
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260424.txt
  - transcripts/simon-scrapes/the-only-claude-code-updates-you-need-to-know-apr-2026_20260424.txt
  - transcripts/simon-scrapes/every-claude-code-memory-system-compared-so-you-don-t-have-to_20260424.txt
  - transcripts/john-kim/new-claude-code-updates-are-so-cool_20260424.txt
---

# Enable Auto Memory and Use Autodream to Keep Memory Files Clean

## TL;DR

Auto memory captures session learnings incrementally; Autodream consolidates them nightly (deduplicate, merge, prune) to stay under 200 lines.

## Why it matters

After 50+ sessions, auto memory files accumulate contradictions, stale references, and redundant entries that degrade performance. Autodream is modeled on human memory consolidation during sleep: convert relative dates to absolute, delete contradicted facts, merge duplicates, prune stale notes. The memory.md index stays under 200 lines so it doesn't eat startup context.

## How to apply

Enable auto memory: in settings.json add `"autoMemory": true`. View your memory: type `/memory` in any session. Trigger Autodream manually: 'consolidate my memory files' (the /stream command is not yet reliable). Or ask Claude to reorganize: enter plan mode, paste the memory management setup prompt (see John Connelly's template), let it create a structured `~/.claude/memory/` with `general.md`, `tools/`, and `domains/` subdirectories. Set a session-start hook that auto-injects the memory.md index (not the full memories) at the start of each session.
