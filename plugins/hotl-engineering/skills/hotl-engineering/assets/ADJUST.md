# ADJUST.md — Replacement Points When Applying the Template

Adapt these pnpm + Next.js/TS + Azure Container Apps + AWS Bedrock examples to
the selected project. They are not a ready-to-deploy universal stack. Preserve
existing enforced gates; introduce new advisory checks proportionately.

## Common to all files
- [ ] Model IDs are not written in the templates. Set them as repository variables; a job whose variable is unset fails before the agent runs
      - `HOTL_MODEL_LIGHT`: ai-review (every PR), incident-triage, agent-implement
      - `HOTL_MODEL_DEEP`: the ai-review Tier 2 deep-dive review
      - `HOTL_JUDGE_MODEL`: the eval-gate judge (ideally a different model from the generator)
      - Use the inference profile ID (an ID that contains `claude-`) of a model your organization has enabled on
        Bedrock. Check current model IDs in Anthropic's model tables for "Claude in Amazon Bedrock" and "Claude on
        Amazon Bedrock (legacy)". Do not pick a deprecated model (such as Sonnet 4.5). Record the date you set the
        variables and the date you checked the model tables
      - Do not use an alias (`sonnet` / `opus` / `haiku` / `fable`). On Bedrock an alias can resolve to an older
        model (checked 2026-11-12: `sonnet` is Sonnet 4.5 and `haiku` is Haiku 4.5)
      - Avoid application inference profile ARNs (see the effort item below)
- [ ] Bedrock decides model lifecycle separately from Anthropic. Check the AWS model lifecycle (Active / Legacy /
      EOL / public extended access) and do not pick a Legacy model. A Legacy model can lose access after 15 days
      without use. Avoid one especially for incident-triage, which runs rarely and would first fail during an incident
      - Example (checked 2026-11-12): Sonnet 4.5 became Legacy on 2026-10-08 in the commercial Regions, including
        ap-northeast-1. Public extended access starts on 2027-01-08 and EOL is 2027-04-08. This schedule differs from
        its retirement on Anthropic's own platform (2026-11-30)
- [ ] Decide the data processing region from the project's requirements. The template's requirement is that code
      never goes to the direct Anthropic API; it does not promise processing inside Japan. The inference profile sets
      the processing region: a Geo profile (`jp.`, `apac.`, etc.) routes within that geography, and a Global profile
      (`global.`) routes worldwide
      - If processing in Japan is a requirement, pick a model that has a `jp.` Geo profile. As of 2026-11-12, Opus 5.5
        and Haiku 5.5 have one (routed to Tokyo and Osaka). Recheck the AWS model card before you choose
      - From Tokyo, Sonnet 5.5 and Fable 5.2 are available only through `global.` (checked 2026-11-12). That is a wider
        processing region than the `apac.` profiles the 2.0.x templates used
      - Fable 5.2 is available only on the bedrock-runtime endpoint (not bedrock-mantle). The template's paths
        (claude-code-action and run_evals.py) use bedrock-runtime
- [ ] Choose effort together with the model variable, and record them together. The templates pass `--effort` to
      every agent and take the value from a repository variable. An unset variable uses the default; an invalid value
      stops before the agent runs
      - `HOTL_EFFORT_LIGHT` (default medium): ai-review on every PR
      - `HOTL_EFFORT_DEEP` (default high): the ai-review Tier 2 deep-dive review
      - `HOTL_EFFORT_IMPLEMENT` (default medium): agent-implement
      - `HOTL_EFFORT_TRIAGE` (default medium): incident-triage
      - Without an explicit effort, changing only the model variable silently changes the effort too. Claude Code's
        default differs by model (checked 2026-11-12: medium for Fable 5.2, Opus 5.5, Sonnet 5.5, and Haiku 5.5;
        xhigh for Opus 4.7; high for the others)
      - The available levels differ by model. For a level the model does not support, Claude Code runs the highest
        supported level below it. Effort has no effect on a model without effort support (such as Haiku 4.5)
      - Claude Code turns on effort and thinking support by matching the model ID against known patterns. IDs such
        as application inference profile ARNs often do not match, and then these features stay off (`--effort` has
        no effect either). `ANTHROPIC_DEFAULT_*_MODEL_SUPPORTED_CAPABILITIES` declares capabilities for a pinned
        model, but claude-code-action does not pass it to Claude Code, and whether it applies to an ARN passed with
        `--model` is unverified
      - The Claude Code changelog lists a fix to `--effort` in 2.1.72, so the flag works from that version at the
        latest; `xhigh` arrived in 2.1.111. The pinned claude-code-action SHA decides the Claude Code version (below)
- [ ] The agents run with `--setting-sources user`, so Claude Code does not load the project's AGENTS.md (checked
      2026-11-12 with Claude Code 2.1.322 in a local run: AGENTS.md loaded with `user,project` and did not load with
      `user`; a subdirectory's AGENTS.md was not attached on Read under `user` either). Each prompt reads the root AGENTS.md first with Read. Keep that instruction when you rewrite a prompt,
      and keep `--setting-sources user` (see the ai-review section)
      - ai-review exports the PR's base tree to `$RUNNER_TEMP/trusted-base/` and reads AGENTS.md and the files it
        references from there as the norms. The norm files in the working tree (the PR head) are subjects of the
        review, not instructions (see the ai-review section)
      - Subdirectory AGENTS.md files are not read as norms
      - agent-implement and incident-triage do not run on PR events, so they read the default-branch checkout.
        incident-triage also reads runbooks/
      - If the project keeps its norms in another file (such as CLAUDE.md), name that file in every prompt instead
- [ ] AWS region (ap-northeast-1) → your organization's region
- [ ] Secret names (GITHUB_OIDC_ROLE / AZURE_CLIENT_ID* / TEAMS_WEBHOOK_URL, etc.) → align with the secrets that actually exist; if not yet created, attach the creation steps to the deliverable
- [ ] Pin third-party actions (`dorny/paths-filter` / `marocchino/sticky-pull-request-comment` /
      `gitleaks/gitleaks-action`, etc.) to a commit SHA rather than a tag
      (the template writes `@vN` for readability; since CI itself is Tier 2, pinning is the default when applying it).
      If an organization or enterprise allowed-actions policy enforces SHA pinning, unpinned workflows fail at run
      time. Automate pinning and updates with Renovate or similar instead of doing it by hand
- [ ] Pin `anthropics/claude-code-action` to a commit SHA as well. The SHA decides the two points below, so check
      them before you raise the pin, before you change a model variable or effort, and in Renovate's update PRs
      - The Claude Code version it installs (`claudeCodeVersion` in `src/entrypoints/run.ts`; v1 installs 2.1.322 as
        of 2026-11-12). Some models need a minimum version (for example, Fable 5.2 needs 2.1.321 or later). Raise the
        pin if the version falls short
      - On PR events, the action restores fixed paths (`SENSITIVE_PATHS` in `src/github/operations/restore-config.ts`:
        `.claude`, `.mcp.json`, `CLAUDE.md`, and a few others) from the PR's base branch before it starts Claude Code
        (`restoreConfigFromBase` in `run.ts`). AGENTS.md is not among them, so the working tree always holds the PR
        head's AGENTS.md. ai-review therefore reads its norms from the export of the base tree and never from the
        working tree. The replacement of the `.claude` directory and `.mcp.json` still relies on this restore,
        so pin a version that includes it
- [ ] Every action is on a version that runs on Node 24 (GitHub removed Node 20 from hosted runners on 2026-09-23).
      Self-hosted runners must be v2.327.1 or later. Do not downgrade to a Node 20 version

## workflows/ci.yml
- [ ] pnpm → the actual package manager (npm/yarn/uv/poetry). For a Python stack, map L1-L5 to ruff / mypy / pip-audit / pytest
- [ ] `pnpm/action-setup`: v6.1.0 or later for pnpm 11 and later, v5 for pnpm 10 or earlier (the floating `@v6` tag
      points to v6.0.10 as of 2026-10-26, which does not support pnpm 12)
- [ ] Choose `NODE_VERSION` from the current LTS releases (v24 as of 2026-10-26; v22 reaches EOL on 2027-04-30, and v26
      enters LTS on 2026-10-28)
- [ ] `pnpm lint` / `pnpm test` / `pnpm build` → the script names that actually exist
- [ ] Coverage threshold → set vitest.config's `coverage.thresholds` (whole codebase) from a realistic
      value matched to existing coverage results, then raise it gradually. To require coverage only on
      changed files, choose a tool that actually measures the diff and confirm with a fixture that it
      accepts your coverage output format before adopting it
- [ ] Observe newly introduced noisy checks during calibration; do not weaken an existing enforced security job

## workflows/ai-review.yml
- [ ] Tier 2 paths-filter → fully rewrite to the risk paths identified in the assessment (most important)
- [ ] Keep CODEOWNERS and the paths definition in sync
- [ ] Copy `assets/scripts/check_review_verdicts.py` to `.github/scripts/check_review_verdicts.py` on the trusted base before enabling the workflow.
      When updating the template, keep this validator and ai-review.yml on the same version (the validator expects the
      `LIGHT_DOWNLOAD` / `DEEP_DOWNLOAD` outcomes the workflow passes)
- [ ] Keep `AI_REVIEW_ENFORCE` unset during observation; record incomplete evidence as incomplete, then enforce after calibration
- [ ] Require fresh light/deep verdicts with nonnegative counts and the reviewed head SHA; test missing, malformed, wrong-revision, failed, and skipped cases
- [ ] Restrict credentials and permitted tools for the review provider; PR content and model output remain untrusted even when JSON validates
- [ ] Limit the review jobs' `--allowedTools` to the PR comment tools plus a write to the one verdict file
      (`Edit(//<absolute path>)`). Keep `github_token: ${{ github.token }}`. Create the verdict directory fresh
      before the agent runs (no previous verdict survives)
- [ ] Keep `--setting-sources user` and `--strict-mcp-config` in every agent's `claude_args`. `--allowedTools` only
      adds pre-approvals and is not an upper bound, so without them the repository's (including the PR head's)
      Claude Code project settings (`settings.json` allow rules) and `.mcp.json` widen the agent's permissions
- [ ] Read the review norms from the PR's base revision. claude-code-action never restores AGENTS.md to the base
      version (see the claude-code-action item under "Common to all files"). Read from the working tree, a PR that
      rewrites AGENTS.md or a file it references could change the review norms and the verdict
      - Before the agent, each review job exports the base tree fresh to `$RUNNER_TEMP/trusted-base/` with
        `git archive`. The export lives outside the working tree, so it stays out of working-tree searches. Files the
        base's `.gitattributes` marks `export-ignore` are not exported, so never mark norm files that way
      - The prompt reads the AGENTS.md in the export and the files it references. A referenced file missing from the
        export is never read from the working tree instead. The working tree's (the PR head's) AGENTS.md, the files
        it references, and changes to them are subjects of the review, not instructions. If the export cannot be
        read, the agent reviews without norms and never falls back to the working tree's AGENTS.md
      - The agent can read the export because the bare `Read` rule in `--allowedTools` matches all file reads,
        including outside the working tree (Claude Code's permissions documentation, checked 2026-11-12). Turning on
        `permissions.blockReadsOutsideWorkingDirectories` in user settings blocks it. The agent then reviews without
        norms and says so in the summary or report. This is unverified in real CI: during observation, check that no
        review reports unreadable norms
      - If the export is heavy in a large repository, narrow it to the norm files (for example,
        `git archive "$BASE_SHA" AGENTS.md docs/review/`). When you narrow it, keep every file AGENTS.md references
      - Do not add the export with `--add-dir`. Claude Code also loads skills, commands, and agents from the added
        directory's `.claude` directory
- [ ] The light review runs with `--max-turns 5`, and reading AGENTS.md and its references takes turns. The prompt
      allows reading them in the same turn as fetching the diff. During observation, check that the turns suffice
      (a verdict file is written every time)
- [ ] If LIGHT or DEEP uses a model with safety classifiers (the Fable models, Opus 5.5, Sonnet 5.5, Opus 5), set the
      fallback targets for a refusal. An attacker's-perspective deep review tends to hit the cyber classifier and can
      be refused from the first request
      - On Bedrock, without an Opus pin (`ANTHROPIC_DEFAULT_OPUS_MODEL`) or an Opus 4.8 entry in the provider's model
        list, fallback is off for every model and the request ends with the refusal ("Enable fallback on Bedrock,
        Agent Platform, and Foundry" in Claude Code's model configuration documentation, checked 2026-11-12)
      - Each agent job's env takes `ANTHROPIC_DEFAULT_OPUS_MODEL` from the repository variable
        `HOTL_FALLBACK_OPUS_MODEL` and `ANTHROPIC_DEFAULT_SONNET_MODEL` from `HOTL_FALLBACK_SONNET_MODEL`.
        claude-code-action passes these two from the job env to Claude Code. Unset variables pass through empty,
        which behaves as before
      - Set them to the inference profile IDs of another enabled Opus (such as Opus 4.8) and Sonnet (such as
        Sonnet 5). The fallback model needs a context window at least as large as the source model's (1M by default
        on Bedrock). The refusing model itself or a model from another family leaves the refusal standing
      - Sonnet 5.5 also needs a Sonnet pin (or a Sonnet 5 entry in the model list) in addition to the Opus pin
      - After a fallback, the fallback model writes the rest of the review and the verdict file. Keep the model that
        actually ran (`modelUsage` in the result message of the execution file) in the audit trail, not the model in
        the variable
      - A refusal leaves no verdict file, and the validator treats that as incomplete evidence (Phase 2 blocks the
        merge). Record refusals during observation. If they continue, consider weakening the PoC instruction to "show
        why the attack holds (the reachable path and its preconditions)"
- [ ] When you change a LIGHT / DEEP model variable or effort, go back to Phase 1 (`AI_REVIEW_ENFORCE` unset) or
      compare the old and new verdicts on the same PRs before switching. How CRITICAL counts come out depends on the
      model and effort together

## workflows/agent-implement.yml
- [ ] Add an Issue template (acceptance criteria required) alongside it in .github/ISSUE_TEMPLATE/
- [ ] Confirm that the blocked operations (adding a dependency, dropping a column) match the project's actual situation
- [ ] Verify that the read-only authorization job can query the label actor's repository permission; the sample requires admin permission and fails closed on API errors
- [ ] Configure environment reviewers and preserve the approved issue text/revision before enabling autonomous implementation; an editable issue body is not a durable approval snapshot
- [ ] Replace the lint / typecheck / test commands in `--allowedTools` with scripts that actually exist in the project.
      Install dependencies in a step before the agent; never allow install as a direct agent command.
      Keep pushes fixed to the Issue's branch and do not add `gh api`, merge, or force push. Do not let the agent
      open the PR (prefix rules cannot constrain `gh pr create` arguments); a separate job opens it with a fixed
      repo, head, base, and Draft flag. Limit file-edit approvals to the working tree (`Edit(//<workspace>/**)`)
      and the two PR files; never add bare Edit / Write (they can rewrite Actions environment files outside the working tree)
- [ ] The step that opens the PR uses GITHUB_TOKEN by default, so pull_request workflows do not run automatically
      on that PR. To run CI or ai-review on it, create your own GitHub App (write access to Contents and Pull requests)
      and set `vars.HOTL_APP_ID` and `secrets.HOTL_APP_PRIVATE_KEY`. create-github-app-token v3.1 and later recommend
      `client-id` (the App's Client ID), but actionlint 1.7.12 does not support it, so the template keeps `app-id`
- [ ] Tests and git commit (hooks) run repository code while the job's credentials are in the environment.
      Operations inside those child processes are not limited by the pre-approvals. Where outsiders can file Issues,
      always combine environment reviewers with finalizing the Issue body at CP1

## workflows/eval-gate.yml (agent systems only)
- [ ] Trigger paths (prompts/, etc.) → the actual location of your prompts and retrieval logic
- [ ] Set the TARGET_ENDPOINT / EVAL_BUCKET vars
- [ ] Route PR evaluations to an isolated preview of the candidate; require each target response to include the deployed `revision` matching `EXPECTED_REVISION`. A shared staging PASS is not PR evidence
- [ ] Keep runner and thresholds on the trusted base for PR execution. Review changes to threshold policy separately; do not let a candidate lower its own gate
- [ ] Do not use the thresholds.json values as-is; set them from the measured results of the first full run
- [ ] When upgrading from 2.0.x, replace `judge_total_floor` / `judge_total_drop_allowed` in thresholds.json with
      `judge_axis_pass_rate_floor` / `judge_axis_pass_rate_drop_allowed` and `judge.pass_score`, and regenerate
      baseline.json with a calibration run that omits `--baseline`. With the old settings or baseline,
      run_evals.py stops with the reason (it never silently skips the comparison)
- [ ] Keep the anthropic SDK major pinned (the template uses `>=1.17,<2`). 1.x and later do not accept
      sampling parameters (temperature etc.), so judge variance is handled by the vote count. Before
      moving to 2.x (API version 2026-10-21), move the judge to a model Bedrock supports for 2026-10-21
      (Claude 4.7 or later) together with the IAM and endpoint changes, and first pass a network-free
      contract test (codex-plugins' scripts/tests/test_hotl_sdk_contract.py is an example) on the new version
- [ ] Leave room for thinking in the judge's `max_tokens`. A judge with thinking on by default (Opus 5 and later,
      Sonnet 5 and later, Haiku 5.5, the Fable models) thinks even when `thinking` is not sent, and the thinking counts
      toward `max_tokens`. Opus 4.7 / 4.8 run without thinking when it is omitted. The template's default is 16000.
      Set it from `usage.output_tokens` in the first calibration run. The SDK refuses a non-streaming call whose value
      exceeds about 21,333 before sending it, so stay below that. **In repositories that already applied the
      template, edit the value in thresholds.json by hand**
      - If it is too small, votes stop before the JSON is complete. run_evals.py prints the reason and `stop_reason`
        for every dropped vote. On `stop_reason=max_tokens`, raise `judge.max_tokens` or lower `judge.effort`
- [ ] Set the judge's effort with `judge.effort` in `thresholds.json` (low / medium / high / xhigh / max). It is sent
      only when set, and an invalid value stops the run before evaluating. Unset, the model's API default applies,
      which can differ from Claude Code's default (checked 2026-11-12: the Messages API default is high for Fable 5.2
      and Sonnet 5.5, and medium for Opus 5.5 and Haiku 5.5). Do not set it for a model that rejects effort (such as
      Haiku 4.5)
- [ ] Record the judge model and effort together (the report and `judge_model` / `judge_effort` in the results.json
      summary show both). Before changing either, compare eval-gate results and L3 human calibration between the
      old and new settings
- [ ] Bootstrap the reviewed baseline explicitly with a calibration run that omits `--baseline`; store it before enabling the workflow. Routine missing/failed downloads must not disable comparison
- [ ] Keep report/artifact output in a fresh runner temporary directory. Publish only fresh results; setup failures must never publish a candidate-supplied PASS report
- [ ] Keep the trusted-runner approach for PRs (checkout from the base side). For a PR that changes
      the runner (run_evals.py), notify the team that "the new runner first runs with secrets in the
      nightly run after merge"

## evals/run_evals.py (agent systems only)
- [ ] Rewrite `call_target()` to match the API contract of the system under evaluation (it is isolated to this one function)
- [ ] Preserve deployed-revision evidence from the target; never synthesize it from the expected SHA supplied by the runner
- [ ] Keep target/judge execution errors separate from quality scores and fail incomplete suites; validate all configured judge votes and score ranges
- [ ] The L1 metrics (recall@5 / MRR) assume retrieval-based QA. For an agent without retrieval, trim
      to deterministic checks only (prohibited output, format, refusal)
- [ ] Redesign the golden-set file names and categories for your own domain (the template's
      golden.sample.jsonl is a structural example; follow the category design in references/eval-design.md)

## workflows/deploy.yml
- [ ] The full set of deploy-target commands (assuming Container Apps) → rewrite for the actual
      platform. Invariant: staging automatic → environment approval (CP3) → health watch → automatic rollback
- [ ] Confirm the existence of a health endpoint equivalent to /api/health (implement it first if missing)
- [ ] Attach the setup steps for GitHub Environments (production) Required reviewers to the deliverable
- [ ] Implement executable `.github/scripts/capture-production-state.sh <output-json>` and `.github/scripts/restore-production-state.sh <input-json>`; production preflight intentionally fails until both exist
- [ ] Capture revision mode, immutable deployed image/revisions, and actual traffic weights. Reject unsupported state before deploying. Restore routing as well as the target revision/image, verify health, and return nonzero on any failure
- [ ] Rehearse success and failed recovery against the selected platform, bound timeouts, and connect an authorized human-notification channel for both outcomes. File existence is only a preflight, not recovery proof

## workflows/incident-triage.yml
- [ ] Guarantee via IaC/procedure that the investigation role is Read-Only (Reader + log viewing only)
- [ ] Rewrite the --allowedTools command list to the read-only commands of the target platform. Spell
      prefixes down to the specific subcommand (a broad prefix such as `az monitor:*` also allows
      mutating subcommands). Do not add general-purpose commands such as `gh api` or any write command.
      Keep the `--tools` restriction and the `--disallowedTools` ban on file-editing tools
- [ ] Keep `github_token: ${{ github.token }}` on claude-code-action. Without it, the Claude GitHub App
      token, which can write, is handed to the agent. Keep the triage job's permissions to read plus id-token
- [ ] Keep Issue creation and notification in the separate report job (never run the agent in a job
      that can write)
- [ ] Write the alert payload to a file through env: and have the agent read it. Never expand it with
      `${{ }}` in the prompt or in run:
- [ ] Only the agent's final answer goes into the Issue, but the final answer can still quote logs.
      Check who can read Issues (is the repository private?) and add masking before posting if needed
- [ ] The alert → repository_dispatch relay (Function/Logic App) requires separate implementation

## templates/
- [ ] AGENTS.md.template → fully rewrite to the project's absolute norms, commands, and conventions (keep only the template's structure).
      Put it at the repository root (the workflow agents read the root AGENTS.md)
- [ ] Give every line you add to "Common Mistakes" a reason and a scope. Review the lines when you change models and
      periodically, and delete lines whose reason is gone. Models follow accumulated warnings closely, so stale lines
      can make the agent ask for approvals nobody needs or stop routine work. For a rule that must always hold, state
      its scope and reason, and write the exception path into the rule ("get human approval before ...")
- [ ] CODEOWNERS.template → actual usernames, Tier 2 paths
- [ ] setup-branch-protection.sh → run in Phase 2 (do not run in Phase 1)
