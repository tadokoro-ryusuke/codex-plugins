# Pull Request Workflow

Use this when creating or drafting a GitHub PR.

## Preflight

1. Check branch:

   ```bash
   git branch --show-current
   git status --short
   ```

2. Reject direct PR creation from `main` or `master`.
3. Preserve dirty changes. If commit/push is already authorized, stage only the intended files after checks. Otherwise prepare the requested local body without creating commits; ask only when actual delivery needs authority that is missing.
4. For actual PR creation, fetch remote state when network access is permitted. For a local draft, use available evidence and label a stale/unknown base:

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

Classify the PR according to repository conventions. Record the compared base and
head; check that the final diff still matches the reviewed one before submission.
Distinguish committed PR content from uncommitted local edits in a draft.

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

Honor the user's draft/ready choice. Use draft as a reversible default when they
requested creation without specifying readiness. Do not repeat an approval already
given. A request only for text authorizes no external PR creation.

Write the exact multiline body to a local file, inspect it, then pass its path.
Lead with the problem and resulting behavior, followed by relevant verification
and material limitations. Keep optional issue sections out when no issue is verified.

```bash
gh pr create --draft --title "<title>" --body-file <body-file> --base <base>
gh pr view --json url
```

After creation, report the URL and any checks that were skipped.
