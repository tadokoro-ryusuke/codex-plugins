---
name: github-workflows
description: "GitHub workflow support for preparing pull requests, drafting PR titles and bodies, linking issues, checking branch state, and updating documentation. Use when the user asks to create a PR, prepare a draft PR, summarize changes for GitHub, link an issue, or update README/docs after code changes."
---

# GitHub Workflows

Use this skill for GitHub-facing development tasks. Prefer `gh` when it is installed and authenticated; otherwise produce a clear draft the user can submit.

## Workflow Map

| User asks for | Read |
| --- | --- |
| Create or prepare a pull request | `references/pull-request.md` |
| Update README or docs after code changes | `references/docs-update.md` |

## Shared Rules

- Check branch and working tree state before creating a PR.
- Do not create a PR from `main` or `master`.
- Do not hide uncommitted changes; report them and ask whether to commit, stash, or draft only.
- Run relevant project checks before PR creation when feasible.
- Keep issue linking optional and evidence-based. Infer issue numbers from branch names or commits, but verify before using `Closes #...`.

