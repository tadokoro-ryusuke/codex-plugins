# ADJUST.md — Replacement Points When Applying the Template

The templates in assets/ are written assuming pnpm + Next.js/TS + Azure Container Apps + AWS
Bedrock Tokyo. A list of the points you must check and replace when applying them.

## Common to all files
- [ ] Bedrock model ID (`apac.anthropic.claude-*`) → replace with the inference profile enabled for your organization
- [ ] AWS region (ap-northeast-1) → your organization's region
- [ ] Secret names (GITHUB_OIDC_ROLE / AZURE_CLIENT_ID* / TEAMS_WEBHOOK_URL, etc.) → align with the secrets that actually exist; if not yet created, attach the creation steps to the deliverable
- [ ] Pin third-party actions (`dorny/paths-filter` / `marocchino/sticky-pull-request-comment` /
      `gitleaks/gitleaks-action`, etc.) to a commit SHA rather than a tag
      (the template writes `@vN` for readability; since CI itself is Tier 2, pinning is the default when applying it)

## workflows/ci.yml
- [ ] pnpm → the actual package manager (npm/yarn/uv/poetry). For a Python stack, map L1-L5 to ruff / mypy / pip-audit / pytest
- [ ] `pnpm lint` / `pnpm test` / `pnpm build` → the script names that actually exist
- [ ] Coverage threshold (70%) → start from a realistic value matched to existing coverage results
- [ ] In Phase 1, enable `continue-on-error: true` on the security job

## workflows/ai-review.yml
- [ ] Tier 2 paths-filter → fully rewrite to the risk paths identified in the assessment (most important)
- [ ] Keep CODEOWNERS and the paths definition in sync
- [ ] During Phase 1, keep the "block with exit 1" instruction in the prompt disabled

## workflows/agent-implement.yml
- [ ] Add an Issue template (acceptance criteria required) alongside it in .github/ISSUE_TEMPLATE/
- [ ] Confirm that the blocked operations (adding a dependency, dropping a column) match the project's actual situation

## workflows/eval-gate.yml (agent systems only)
- [ ] Trigger paths (prompts/, etc.) → the actual location of your prompts and retrieval logic
- [ ] Set the TARGET_ENDPOINT / EVAL_BUCKET vars
- [ ] Do not use the thresholds.json values as-is; set them from the measured results of the first full run
- [ ] Keep the trusted-runner approach for PRs (checkout from the base side). For a PR that changes
      the runner (run_evals.py), notify the team that "the new runner first runs with secrets in the
      nightly run after merge"

## evals/run_evals.py (agent systems only)
- [ ] Rewrite `call_target()` to match the API contract of the system under evaluation (it is isolated to this one function)
- [ ] The L1 metrics (recall@5 / MRR) assume retrieval-based QA. For an agent without retrieval, trim
      to deterministic checks only (prohibited output, format, refusal)
- [ ] Redesign the golden-set file names and categories for your own domain (the template's
      golden.sample.jsonl is a structural example; follow the category design in references/eval-design.md)

## workflows/deploy.yml
- [ ] The full set of deploy-target commands (assuming Container Apps) → rewrite for the actual
      platform. Invariant: staging automatic → environment approval (CP3) → health watch → automatic rollback
- [ ] Confirm the existence of a health endpoint equivalent to /api/health (implement it first if missing)
- [ ] Attach the setup steps for GitHub Environments (production) Required reviewers to the deliverable

## workflows/incident-triage.yml
- [ ] Guarantee via IaC/procedure that the investigation role is Read-Only (Reader + log viewing only)
- [ ] Rewrite the --allowedTools command list to the read-only commands of the target platform
- [ ] The alert → repository_dispatch relay (Function/Logic App) requires separate implementation

## templates/
- [ ] AGENTS.md.template → fully rewrite to the project's absolute norms, commands, and conventions (keep only the template's structure)
- [ ] CODEOWNERS.template → actual usernames, Tier 2 paths
- [ ] setup-branch-protection.sh → run in Phase 2 (do not run in Phase 1)
