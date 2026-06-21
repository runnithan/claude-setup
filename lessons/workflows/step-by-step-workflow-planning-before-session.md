---
id: step-by-step-workflow-planning-before-session
created: 2026-06-07
status: active
supersedes: null
category: workflows
sources:
  - transcripts/simon-scrapes/how-anthropic-teams-actually-use-claude-code-day-to-day-for-non-engineers_20260607.txt
---

# Plan the Full Workflow Step-by-Step Before Starting the Claude Code Session

## TL;DR

Sketch the entire task or workflow in plain text or a browser chat first, then move to Claude Code only once you know what you're building and how to decompose it.

## Why it matters

Anthropic's legal team and growth marketing do end-to-end planning in claude.ai first, then execute in Claude Code. This prevents mid-session drift, reduces iteration, and clarifies scope before consuming tokens. It differs from `plan-mode-before-every-nontrivial-change`: this planning happens *before* the session even starts, outside the agent loop.

## How to apply

Write a plain text file or doc describing the full workflow, inputs, outputs, and decision points. Use Claude in the browser to brainstorm variations and refine steps. Once the plan is solid, paste it into Claude Code with an "execute this plan step-by-step" prompt. This takes 10–15 minutes upfront and saves hours of rework.
