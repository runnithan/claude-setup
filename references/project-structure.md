# Project Structure

This repo is a portable Claude Code config, copied into a project as its `.claude/` folder (see [README.md](../README.md)).

```
claude-setup/
  CLAUDE.md                 # project instructions (curated — see lessons/README.md)
  IMPLEMENT.md              # third-party tools to install fresh per project (GSD, Ralph)
  README.md                 # how to copy this repo into a project's .claude/
  settings.json             # shared Claude Code settings (hooks, permissions)
  settings.local.json       # machine-local settings (not portable)
  package.json              # JS deps for hooks
  pyproject.toml / uv.lock  # Python deps for scripts/ (youtube-transcript-api)

  .claude/commands/         # slash commands (/extract-lessons, /pr, /ticket, /test, ...)
  agents/                   # custom subagent definitions (backend-dev, frontend-dev, qa,
                            #   code-reviewer, code-simplifier, pr-test-analyzer)
  hooks/                    # lifecycle hook scripts (auto-format, security reminder,
                            #   gsd-* hooks written by the GSD installer)
  skills/                   # locally-tuned skills (claude-md-improver, frontend-design)
  references/               # detail docs CLAUDE.md points to (integrations, this file)

  scripts/                  # transcript pipeline + scheduled-task setup
                            #   update_urls.py, fetch_transcripts.py, run_pipeline.py,
                            #   install_scheduled_task.ps1, ralph-*.sh

  transcripts/              # fetched YouTube transcripts, one folder per creator
                            #   urls.txt (source list), index.md (manifest),
                            #   no-transcript-available.md (skip ledger)
  lessons/                  # mined lessons, one file per lesson under <category>/
                            #   INDEX.md (active-lesson index), .processed.json (dedup)

  projects/                 # per-project improvement notes (one folder per tracked project)
```

Third-party tooling (GSD, Ralph) is installed fresh per project — see [IMPLEMENT.md](../IMPLEMENT.md). Its generated files (`get-shit-done/`, `gsd-file-manifest.json`) stay uncommitted.
