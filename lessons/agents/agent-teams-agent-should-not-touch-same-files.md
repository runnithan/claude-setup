---
id: agent-teams-agent-should-not-touch-same-files
created: 2026-04-25
status: active
supersedes: null
category: agents
sources:
  - transcripts/john-kim/claude-code-s-new-agent-teams-are-insane-opus-4-6_20260424.txt
  - transcripts/ray-amjad/learn-claude-code-agent-teams-in-12-minutes_20260307.txt
---

# Structure Agent Teams So Teammates Never Touch the Same Files

## TL;DR

File conflicts between agents are the primary failure mode of agent teams; design team roles around domain isolation, not component ownership.

## Why it matters

When two agents in a team edit the same file, merge conflicts and inconsistent state emerge rapidly. Agent teams work best when each agent has a clearly bounded domain with minimal file overlap: frontend vs. backend vs. test, or security review vs. performance review vs. coverage review. Each agent should have read access to everything but write access only to its domain.

## How to apply

Before spawning an agent team: list all files that will be touched. Assign each file to exactly one agent. If a file needs input from multiple agents (e.g., a shared API contract), have one agent own it and others read it via the task list messages. For code review teams: make all review agents read-only; only the implementation agent writes. For debugging with competing hypotheses: all investigation agents are read-only; the main agent applies the winning fix. Use git worktrees as an additional layer of isolation if domain boundaries are unclear.
