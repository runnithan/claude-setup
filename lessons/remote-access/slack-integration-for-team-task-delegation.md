---
id: slack-integration-for-team-task-delegation
created: 2026-04-25
status: active
supersedes: null
category: remote-access
sources:
  - transcripts/ray-amjad/anthropic-just-added-these-features-to-claude-code_20260424.txt
---

# Use the Slack Integration to Delegate Tasks From Team Channels

## TL;DR

@Claude in a Slack channel delegates tasks to Claude Code; connect Sentry or logging MCPs to let it respond to production events automatically.

## Why it matters

For team workflows, delegating via Slack means the whole team can assign tasks to Claude without terminal access. Connecting Sentry or your logging system as a custom connector means Claude can automatically pick up and respond to production incidents tagged in Slack, reducing mean time to response.

## How to apply

In Slack: go to Apps, search 'Claude', click Add to Slack. Allow permissions, connect your Anthropic account. Choose code-only or code+chat mode. In any channel: add Claude to the channel, then @Claude [task description]. Claude asks which repo to work in if it can't determine it. To extend: go to Claude in Slack → Connect → add a custom Sentry MCP connector or your own logging system URL. Claude will then be able to fetch error context automatically when tagged in an incident channel.
