---
id: agent-view-native-orchestration-ui
created: 2026-06-03
status: active
supersedes: null
category: workflows
sources:
  - transcripts/john-kim/claude-code-just-got-better-agent-view_20260603.txt
  - transcripts/simon-scrapes/claude-code-has-a-new-ui-pair-it-with-claude-os_20260603.txt
---

# Use `claude agents` (Agent View) Instead of Juggling Terminals

## TL;DR

`claude agents` opens a native multi-session dashboard that persists across terminal restarts — the built-in answer to managing 5+ parallel sessions, replacing tmux/window juggling.

## Why it matters

Running many parallel sessions previously meant babysitting terminal windows and losing sessions when a terminal closed. Agent View gives one persistent dashboard with status at a glance, sessions that survive terminal close, and per-project scoping (git worktrees under the hood for collision-free parallel work). It is the native replacement for the "build your own Kanban" advice.

## How to apply

Run `claude agents` (v2.1.139+); `/bg` backgrounds the current session into it. Keys: Right = attach, Left = detach, Space = peek / quick reply, `Ctrl+S` = sort by repo, `Ctrl+R` = rename working dir, `Ctrl+T` = pin, `Ctrl+X` twice = delete. Status colours: gray = working, yellow = waiting/checking, purple = merging (e.g. a worktree), green = done/merged. Caveats (research preview): terminal-only, sorts to parent-folder level (not subfolders), and approving from the summary view was unreliable — attach to approve.
