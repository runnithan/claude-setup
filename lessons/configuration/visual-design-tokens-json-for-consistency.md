---
id: visual-design-tokens-json-for-consistency
created: 2026-06-07
status: active
supersedes: null
category: configuration
sources:
  - transcripts/simon-scrapes/i-taught-claude-code-to-build-you-a-personal-brand-watch-this_20260607.txt
---

# Create a tokens.json Design-System File for Consistent Generated Visuals

## TL;DR

Extract your brand visual identity (colors, typography, logos) into a tokens.json config; point all visual-generation skills at it so every output is on-brand without manual art direction.

## Why it matters

Manually art-directing each visual output is tedious and inconsistent. When design tokens live in one place, every generated carousel, slide, or graphic pulls from the same palette and typography, creating instant brand recognition across outputs.

## How to apply

Gather 3–5 visual references that match your brand aesthetic (carousels, Figma designs, brand PDFs). Ask Claude to extract: color palettes (primary, secondary, accent), typography (headings, body, scale), logos, and layout patterns. Save as `tokens.json` in your brand context folder (see `shared-brand-context-folder-for-all-skills`). When generating visuals, reference the tokens file in the skill prompt or pass its path explicitly.
