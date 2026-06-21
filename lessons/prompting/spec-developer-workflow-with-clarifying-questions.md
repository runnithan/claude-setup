---
id: spec-developer-workflow-with-clarifying-questions
created: 2026-04-25
status: active
supersedes: null
category: prompting
sources:
  - transcripts/ray-amjad/the-top-0-01-user-s-guide-to-claude-code_20260307.txt
---

# Use the Spec Developer Workflow: Have Claude Ask Clarifying Questions Before Starting

## TL;DR

Tell Claude 'you are a spec developer; ask me questions to write a complete spec before writing any code.'

## Why it matters

Most context failures happen because requirements are underspecified at the start. The spec developer workflow forces Claude to surface all ambiguities upfront through structured questions, just as a senior engineer would before starting a sprint. This produces a written spec that both parties agree on before a single line is written.

## How to apply

Prompt: 'You are a spec developer. Your role is to ask me questions to create a complete specification for this feature before writing any code. Ask clarifying questions one at a time about: scope, edge cases, error handling, data model, integrations needed, and acceptance criteria. Once I've answered all questions, produce a spec document and wait for my approval before implementing.' Save the resulting spec to a file and reference it in subsequent sessions.
