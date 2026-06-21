---
id: session-resume-keyboard-shortcuts
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/vibe-coding-news-this-week_20260307.txt
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260424.txt
---

# Master /resume Keyboard Shortcuts for Fast Session Navigation

## TL;DR

In /resume: P previews, B shows branches from compaction, R renames, A shows all projects, Ctrl+W shows all worktrees.

## Why it matters

Session management is a daily friction point. Knowing keyboard shortcuts means you can resume the right session, see its state, rename it for clarity, and switch between projects in seconds rather than scrolling through undifferentiated session lists.

## How to apply

Type `/resume` or `claude --resume [session-name]` to open. Keyboard shortcuts: P=preview session contents without resuming, B=show branches from compaction (sessions forked via compact), R=rename the selected session, A=toggle showing all projects vs. current directory only, Ctrl+W=show all worktrees. To name a session: `/rename [name]` or press R in the resume list. Then resume by name: `claude --resume youtube`. Use these to maintain a coherent multi-session workspace across long projects.
