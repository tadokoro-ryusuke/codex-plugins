# Pull Request Workflow

Use this when creating or drafting a GitHub PR.

## Preflight

1. Check branch:

   ```bash
   git branch --show-current
   git status --short
   ```

2. Reject direct PR creation from `main` or `master`.
3. If the working tree is dirty, either help commit logical groups or create a PR draft body only.
4. Fetch remote state:

   ```bash
   git fetch origin
   ```

5. Determine base branch:

   ```bash
   git symbolic-ref refs/remotes/origin/HEAD
   ```

## Issue Detection

Look for an issue number in:

- Explicit user argument.
- Branch name, such as `feature/issue-31`.
- Recent commit messages containing `#31`.

If found, verify with:

```bash
gh issue view <number> --json title,url,state
```

## Change Analysis

Collect:

```bash
git diff --name-only origin/<base>...HEAD
git diff --shortstat origin/<base>...HEAD
git log --oneline origin/<base>...HEAD
```

Classify the PR as `feat`, `fix`, `test`, `docs`, `refactor`, or `chore` based on changed files and commits.

## Quality Checks

Run project-specific checks when available. Prefer commands from `package.json`, `AGENTS.md`, or CI config. If `dev-core` is installed, use `verification-loop` for the evidence standard.

## PR Body Template

```markdown
## Summary

- 

## Related Issue

- Closes #

## Changes

- 

## Verification

- [ ] 

## Notes

- 
```

## Create The PR

Ask whether it should be draft unless the user specified ready/draft.

```bash
gh pr create --title "<title>" --body "<body>" --base <base>
gh pr view --json url
```

After creation, report the URL and any checks that were skipped.

