---
id: claude-md-hierarchy-keep-it-under-200-lines
created: 2026-04-25
status: active
supersedes: null
category: configuration
sources:
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260424.txt
  - transcripts/simon-scrapes/every-level-of-claude-code-explained-in-39-minutes_20260307.txt
  - transcripts/simon-scrapes/the-claude-code-skills-trap-most-people-fall-for-this_20260307.txt
  - transcripts/simon-scrapes/200-hours-of-claude-code-lessons-in-14-minutes-for-business-owners_20260424.txt
  - transcripts/simon-scrapes/the-easiest-way-to-get-ahead-with-claude-code_20260424.txt
  - transcripts/john-kim/how-i-use-claude-code-meta-staff-engineer-tips_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-memory-system-compared-so-you-don-t-have-to_20260424.txt
  - transcripts/andrew-codesmith/master-95-of-claude-code-in-15-mins-as-a-beginner_20260424.txt
---

# Keep CLAUDE.md Under 200 Lines and Use the Four-Level Hierarchy

## TL;DR

CLAUDE.md is a table of contents, not an encyclopedia. Keep it ≤200 lines; put detailed rules in separate reference files it points to.

## Why it matters

Every line in CLAUDE.md loads into the context window on every session start. A 2000-line file burns context before any work begins, degrades output quality through context rot, and buries important rules in noise. The four-level hierarchy (enterprise → project CLAUDE.md → project rules → user memory) lets you apply rules at the right scope.

## How to apply

Write non-negotiables and architecture decisions directly in CLAUDE.md (target 50-150 lines). For any topic needing >20 lines of detail, create a separate markdown file in `.claude/` and reference it from CLAUDE.md with a single line pointer. Use `.claude/rules/` folder for path-scoped rules (rules that only apply to files in a specific directory). Commit CLAUDE.md to git so it compounds across the team over time.
