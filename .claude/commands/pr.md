---
description: "Create a PR from current branch targeting main, with Jira ticket reference"
disable-model-invocation: true
---

Create a pull request from the current branch:

1. **Get branch info**: Run `git branch --show-current` to get the current branch name. Extract the Jira ticket key (the `PROJ-XX` prefix).

2. **Gather changes**:
   - Run `git log main..HEAD --oneline` for commit history
   - Run `git diff main...HEAD --stat` for changed files summary

3. **Create the PR** using `mcp__github__create_pull_request`:
   - `owner`: `YOUR_ORG`
   - `repo`: `YOUR_REPO`
   - `base`: `main`
   - `head`: current branch name
   - `title`: `{PROJ-XX} {concise description of changes}` (under 70 chars)
   - `body`: Include a summary section with bullet points of key changes, a link to the Jira ticket, and a test plan checklist

4. **Report**: Show the PR URL and a summary of what was included.
