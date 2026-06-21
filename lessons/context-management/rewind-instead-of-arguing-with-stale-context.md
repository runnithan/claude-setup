---
id: rewind-instead-of-arguing-with-stale-context
created: 2026-04-25
status: active
supersedes: null
category: context-management
sources:
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
  - transcripts/ray-amjad/anthropic-just-dropped-the-feature-nobody-knew-they-needed_20260424.txt
  - transcripts/andrew-codesmith/master-95-of-claude-code-in-15-mins-as-a-beginner_20260424.txt
---

# Rewind Instead of Arguing With Stale Context

## TL;DR

When Claude has a fundamental misconception, /rewind back to before the error and reprompt; don't try to correct 20% stale context inline.

## Why it matters

Correcting a mistake inline adds the wrong reasoning and the correction to the conversation history. If the misconception happened 10 messages ago, you now have 20-30% of your context window filled with a mistake and a discussion of the mistake. Future responses are biased by all of that stale context. Rewinding deletes it cleanly.

## How to apply

Press Escape twice to see the checkpoint list, or use `/rewind`. Navigate to the last checkpoint before the bad decision. Select 'restore code and conversation' then reprompt with the corrected, more detailed instructions. Use /btw to identify the misconception first without interrupting Claude, then /rewind to fix it. Checkpoints are auto-created before each edit.
