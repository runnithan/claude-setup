# Changelog

## [0.1.0] - 2026-06-21

Initial public release — a portable Claude Code configuration.

- Slash commands for everyday work: `/extract-lessons`, `/extract-social-lessons`, `/consolidate-lessons`, `/optimise`, `/test`, `/review-pr`, `/pr`, `/ticket`, `/fact-check`, and Ralph-loop helpers
- Subagents (`backend-dev`, `frontend-dev`, `qa`, `code-reviewer`, `code-simplifier`, `pr-test-analyzer`), with read-only roles tool-restricted
- Lifecycle hooks: an advisory security reminder, a portable auto-formatter, and GSD statusline / context-monitor / update-check
- Skills: `claude-md-improver` and `frontend-design`
- A lessons library of actionable Claude Code tips, grown from practitioner content via `/extract-lessons` (transcripts) and `/extract-social-lessons` (posts), and curated with `/consolidate-lessons`
- Installable as a plugin marketplace (`/plugin marketplace add runnithan/claude-setup`), or copy the repo into a project's `.claude/`
- CI workflow validating settings, plugin manifests, and hook syntax
- A curated `CLAUDE.md` plus reference docs covering integrations, structure, and hook gotchas
