---
id: environment-switching-local-cloud-ssh
created: 2026-06-11
status: active
supersedes: null
category: commands
sources:
  - transcripts/tristen-o-brien/top-6-claude-code-features-to-get-you-ahead-of-99-of-users-in-under-10-minutes_20260610.txt
---

# Switch Execution Environment (Local / Cloud / SSH) to Match the Workload

## TL;DR

The environment selector at the bottom of Claude Code switches where work executes: local for fast interactive iteration, cloud (Anthropic servers) for routines that must run with your machine off, SSH for driving a remote box like a VPS.

## Why it matters

People default to local for everything and then wonder why scheduled work dies when the laptop sleeps. The execution environment is a one-click choice per task: interactive dev wants local speed; unattended automation wants cloud persistence; workloads needing your own infra (GPUs, private network, persistent disk) want SSH.

## How to apply

Click the environment indicator (shows "local") at the bottom of the Claude Code window and pick cloud or SSH. Rule of thumb: local for anything you're watching; cloud for routines/scheduled agents; SSH when the job must run on a specific remote machine. Pairs with `vps-tmux-telegram-persistent-sessions` for the self-hosted variant.
