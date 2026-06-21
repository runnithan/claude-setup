---
description: "Pick up a Jira ticket: fetch details, transition to In Progress, create branch, checkout locally"
argument-hint: "PROJ-XX"
disable-model-invocation: true
---

Pick up the Jira ticket `$ARGUMENTS` and set up for development:

1. **Fetch the ticket** using `mcp__atlassian__getJiraIssue` with key `$ARGUMENTS`. Display the summary, description, type, and current status.

2. **Transition to In Progress**: Call `mcp__atlassian__getTransitionsForJiraIssue` to get available transitions, then `mcp__atlassian__transitionJiraIssue` to move it to "In Progress".

3. **Create a feature branch**: Generate a branch name as `{ticket-key}-{slugified-summary}` (lowercase, hyphens, max 50 chars). Create it from `main` using `mcp__github__create_branch` with owner `YOUR_ORG`, repo `YOUR_REPO`.

4. **Checkout locally**: Run `git fetch origin && git checkout {branch-name}`.

5. **Report**: Confirm the ticket is in progress, the branch exists, and you're checked out on it.
