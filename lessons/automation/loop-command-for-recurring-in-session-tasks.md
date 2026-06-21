---
id: loop-command-for-recurring-in-session-tasks
created: 2026-04-25
status: active
supersedes: null
category: automation
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-that-kills-openclaw_20260307.txt
  - transcripts/simon-scrapes/claude-code-2-0-has-arrived-it-s-insane_20260424.txt
  - transcripts/simon-scrapes/the-only-claude-code-updates-you-need-to-know-apr-2026_20260424.txt
  - transcripts/john-kim/new-claude-code-updates-are-so-cool_20260424.txt
---

# Use /loop for Recurring In-Session Tasks; Scheduled Tasks for Persistent Automation

## TL;DR

/loop fires a prompt on a cron schedule in your current session (max 3 days). For daily/weekly persistence, use scheduled tasks in the desktop app.

## Why it matters

/loop fills the gap between one-shot prompts and permanent infrastructure. It creates cron jobs that fire automatically without any user interaction, enabling monitoring, polling, or repeated workflows. But loops die when the session closes and expire after 3 days. For anything that needs to run when the laptop is closed, use the desktop app's persistent scheduled tasks, which catch up missed runs on reopen.

## How to apply

Syntax: `/loop every 10 minutes check my inbox for important emails`. Or: `/loop every day check my YouTube for new videos and run my content repurposing skill`. For one-off reminders: `/loop in 1 minute remind me to [X]`. For persistent automation: open the desktop app, go to Scheduled Tasks, fill in name/description/prompt/frequency/model/folder and save. Cloud-based scheduled tasks (set up via claude.ai) run whether your machine is on or off. Use loops for project-duration monitoring; scheduled tasks for ongoing business workflows.
