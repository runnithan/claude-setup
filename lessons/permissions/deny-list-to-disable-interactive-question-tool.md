---
id: deny-list-to-disable-interactive-question-tool
created: 2026-04-25
status: active
supersedes: null
category: permissions
sources:
  - transcripts/ray-amjad/vibe-coding-news-this-week_20260307.txt
  - transcripts/simon-scrapes/every-claude-code-concept-explained-for-normal-people_20260307.txt
---

# Add AskUserQuestion to Deny List to Stop Unwanted Interruptions

## TL;DR

Adding `AskUserQuestion` to the deny list in settings.json prevents Claude from interrupting autonomous runs with clarifying questions.

## Why it matters

In automated and overnight runs, Claude stopping to ask 'Should I proceed?' breaks the workflow entirely. Disabling the AskUserQuestion tool forces Claude to make reasonable assumptions and proceed, which is usually what you want in headless mode. Pair this with a good initial specification to minimize incorrect assumptions.

## How to apply

In settings.json: `{"deny": ["AskUserQuestion"]}`. For fully automated runs, also consider adding `--dangerously-skip-permissions` (or use the auto-mode classifier) and `--disallowedTools AskUserQuestion`. Compensate by being more specific in your initial prompt about edge cases and acceptable assumptions, so Claude has enough context to decide without asking.
