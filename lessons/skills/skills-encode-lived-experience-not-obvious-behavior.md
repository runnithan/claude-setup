---
id: skills-encode-lived-experience-not-obvious-behavior
created: 2026-04-25
status: active
supersedes: null
category: skills
sources:
  - transcripts/ray-amjad/anthropic-just-dropped-their-internal-skills-strategy_20260424.txt
  - transcripts/ray-amjad/anthropic-just-dropped-claude-code-skills-2-0_20260307.txt
---

# Skills Should Encode Unique Knowledge, Not Restate What Claude Already Knows

## TL;DR

A skill that restates obvious behavior pushes the distribution to a worse center; good skills move Claude to low-probability, high-value output.

## Why it matters

Anthropic's internal guide explains skills as forcing functions that shift Claude's output distribution away from the 'statistically most likely' response (distributional convergence) toward specific, low-probability regions of its knowledge. A skill that says 'make a landing page' just reinforces the generic AI-looking design everyone gets. The value is in encoding your own lived experience, expert judgment, or specific knowledge that isn't yet common in training data.

## How to apply

Ask yourself: does this skill tell Claude something it doesn't already have a high probability of doing? If not, it is not worth the context cost. Good candidates: specific billing library behaviors not in training data, a podcast insight about marketing that isn't mainstream yet, your brand voice that is genuinely distinct. Bad candidates: 'write clean code', 'use best practices'. When building a skill, encode that unique expertise in the gotchas section and in specific reference files rather than restating generic principles.
