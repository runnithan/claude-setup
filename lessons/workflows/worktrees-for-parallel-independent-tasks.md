---
id: worktrees-for-parallel-independent-tasks
created: 2026-04-25
status: active
supersedes: null
category: workflows
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-17-new-claude-code-features_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-workflow-explained-u0026-when-to-use-each_20260424.txt
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
---

# Use Worktrees for Parallel Independent Tasks That Cannot Share Files

## TL;DR

`claude -w <name>` creates an isolated worktree branch; multiple can run simultaneously without file conflicts.

## Why it matters

Running multiple tasks in one session fills the context window and creates file conflicts. Worktrees give each task its own isolated workspace with its own context window. When you close a worktree session, Claude automatically cleans up if nothing changed or asks what to do if there's work to keep.

## How to apply

Start a worktree: `claude -w new-onboarding-flow`. Open multiple terminals each with different worktrees: `claude -w fix-checkout-bug`, `claude -w redesign-settings`. Each is isolated on its own git branch. View all running worktrees in `/resume` by pressing Ctrl+W. Add `--tmux` flag to get split-pane visualization: `claude worktree <name> --tmux`. Use `--from-pr <id>` to create a worktree from an existing PR. In agent frontmatter: set `isolation: worktree` to spawn subagents with their own worktree. Best for: independent features, bug fixes, and experiments that don't touch the same files.
