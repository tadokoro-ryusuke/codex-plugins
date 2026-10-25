# Codex Plugins

A Codex-native plugin marketplace: reusable agent skills, hooks, and custom agent roles for disciplined development workflows.

- Marketplace catalog: `.agents/plugins/marketplace.json`
- Plugin manifests: `plugins/<plugin>/.codex-plugin/plugin.json`
- Skills: `plugins/<plugin>/skills/<skill>/SKILL.md` (Agent Skills standard)

## Plugins

| Plugin | Purpose |
| --- | --- |
| `dev-core` | TDD, planning, execution, debugging, verification, review, refactoring, hooks, and continuous-learning workflows. |
| `github-tools` | Pull request preparation and documentation sync using the GitHub CLI. |
| `hotl-engineering` | Human-on-the-Loop delivery workflow design/application and CTO decision support (staged quality gates, AI review, eval gates, audit readiness). |
| `ui-ux-pro-max` | Searchable UI/UX design intelligence (styles, palettes, typography, charts, stacks). |
| `indie-product-marketing` | Opportunity discovery, demand validation, international landing-page design, launch, acquisition, retention, and unit economics. |

## Install

From GitHub (recommended for consumers):

```bash
codex plugin marketplace add tadokoro-ryusuke/codex-plugins
codex plugin add dev-core@codex-plugins
```

From a local clone (for development):

```bash
codex plugin marketplace add /path/to/codex-plugins
codex plugin add dev-core@codex-plugins
```

Then start a new Codex thread so the skills and hooks are picked up. You can also browse and install interactively with `/plugins` inside Codex.

Note: `dev-core` bundles hooks (destructive-command blocking, session-start project state). Codex asks you to review and trust plugin hooks before they run.

## Indie Product Marketing and Landing Design

- `$indie-idea-discovery`: find and rank evidence-backed product opportunities.
- `$indie-product-marketing`: validate demand, choose distribution, launch, and diagnose growth.
- [`$global-landing-design`](plugins/indie-product-marketing/skills/global-landing-design/SKILL.md): research references, design or build an international product LP, and localize or review an existing page.

The landing-page skill bundles dated observations of SPREAD, Circleback,
Inkdrop, Granola, Things, Mobbin, UI Pocket, and the Stride prototype. It
connects audience and buying motion to product proof, visual direction,
working CTAs, mobile layout, localization, and verification. It does not
prescribe one palette or treat a polished page as validated demand.

Example after loading the updated plugin:

> Use $global-landing-design to research these reference sites and build an English LP for my prelaunch product. Keep the existing brand, show the working demo, and distinguish unimplemented features. Add a Japanese version using the same structure.

The bundled behavioral cases specify future model evaluations; packaging
validation alone does not execute them. See the
[creation and verification record](docs/plans/task-global-landing-design-skill.md)
for the source update's scope and evidence.

## Dev Core Entrypoints

Use narrow skills for daily work; `dev-workflow` provides shared orchestration.

| Skill | Use for |
| --- | --- |
| `$dev-grill` | Pressure-test a plan or decision one material question at a time; explicit invocation only. |
| `$dev-task` | Turn an idea into a design plan, acceptance criteria, BDD scenarios, and TDD iterations (template bundled). |
| `$dev-execute` | Execute an approved plan with proportional delegation, risk-based review, TDD, and evidence gates. |
| `$dev-debug` | Investigate errors from root cause before fixing. |
| `$dev-tdd` | Run a focused test-first cycle for one behavior or regression. |
| `$dev-review` | Review with dev-core criteria: behavior, security, tests, architecture, maintainability, conventions. |
| `$dev-refactor` | Refactor safely without behavior changes. |
| `$dev-e2e` | Run or diagnose Playwright E2E tests. |
| `$dev-checkpoint` | Capture resumable state for handoff or continuation (template bundled). |
| `$verification-loop` | Project-specific evidence from build, type, lint, test, security, and diff checks; bundles an optional common-stack runner. |
| `$codex-collab` | Independent review, rescue, parallel subagents; bundles custom agent roles. |
| `$continuous-learning` | Turn a mistake into durable prevention (rules, hooks, tests). |
| `$dev-workflow` | Shared multi-phase orchestration when no narrower skill fits. |

Reference skills `$best-practices`, `$backend-patterns`, and `$frontend-patterns` are loaded on demand (not injected implicitly) to keep the always-on skill list small.

`dev-task` writes durable, default-fail completion contracts under `docs/plans/task-<slug>.md`. `dev-execute` keeps progress, decisions, evidence, and the next action in that same plan so fresh threads can resume without reconstructing state. `codex-collab` ships ready-made custom agent roles (`code-reviewer`, `security-auditor`) you can copy into `.codex/agents/`.

`dev-execute` chooses implementation ownership by independence and benefit, not
plan size. Sequential or tightly coupled work stays with the parent; bounded
delegation is useful for independent progress, specialized evidence, or context
isolation. Review is a separate decision: consequential public contracts,
security/permissions, persistent data, concurrency, and explicit project/user
gates require a fresh reviewer. Other work uses proportional review.
Default model/effort assignments for selected child roles
live in one [execution profile](plugins/dev-core/skills/codex-collab/assets/execution-profile.json).
Use the bundled profile as follows after choosing whether delegation helps:

| Work | Model / effort | Selection |
| --- | --- | --- |
| Parent design, integration and acceptance | GPT-6 Astra / high | Host recommendation |
| General delegated implementation | GPT-6 Sol / medium | Implementer default |
| Short mechanical edits with exact checks | GPT-6 Luna / high | `routine` preset |
| Settled behavior, named files, local dependencies, independent checks | GPT-6 Luna / max | `bounded` preset |
| Complex delegated implementation or bounded technical investigation | GPT-6 Sol / high | `complex` preset |
| Required independent review | GPT-6 Astra / high | Reviewer default |
| Bounded read-only source lookup or log classification | GPT-6 Luna / high | Researcher default |

Keep ambiguous requirements, root-cause judgment and consequential design decisions
with the parent. Return changed assumptions before widening a child's scope.
The profile recommends the parent setting; choose that model in the task's host.
The plugin resolves explicit child requests against the host's exposed models
and effort settings, without silently falling back to another model.

The [execution contract](plugins/dev-core/skills/codex-collab/references/planned-execution.md)
defines bounded writes, parent decisions, fresh handoffs, review independence,
and evidence. It authorizes preset selection for bundled delegated implementation,
including useful debug/TDD handoffs. Preserve explicit task selections and custom
profiles: omit presets for explicit model/effort overrides, and select a custom
profile's preset only when the user or project requests it. Legacy profiles remain
valid without presets; missing roles or presets are never merged from the bundle.
Record the selection reason before dispatch. Check the actual parent
setting separately: a profile recommendation cannot change the running task.
Native tools accepting model/effort arguments do not require installing custom
role files. Read-only task instructions and role names alone
do not establish an enforced sandbox. Resolve only roles actually selected. When
optional delegation is unavailable, disclose the limitation and continue suitable
work in the parent. Explicit role/model requirements and required independent
review remain pending until satisfied; never silently substitute another model.

Reuse check results only after inspecting raw evidence and confirming relevant
inputs and environment still match, when project rules permit it. Label reused
results as prior executions. Stop repeated similar fixes on the same failing
path after three attempts, while continuing independent authorized work.

## HOTL Engineering

`$hotl-engineering` has two modes. Apply mode assesses the stack, delivery risks,
team, and current protections, then prepares proportional CI, AI-review, eval,
and deployment templates. New advisory checks start in observation mode while
existing enforced gates are preserved. Bedrock/Azure examples need project
adaptation; production deployment requires rehearsed capture/restore adapters.
Consult mode supports engineering-management decisions about autonomy,
buy-vs-build, and audit evidence.

For assessment only, ask it to stop after the plan: "Use $hotl-engineering to assess this repo and stop before applying templates."

## Validation

```bash
node scripts/validate-codex-plugins.mjs
node scripts/validate-skill-evals.mjs
python3 -m unittest discover -s scripts/tests -v
```

Use Python 3.12 with PyYAML 6.0.2 for workflow fixtures. The validators check
packaging and behavior-case schema; the offline tests execute script/gate
behavior with fake toolchains and target responses. CI runs both layers plus
hook tests. None of these checks executes the skill scenarios with a model or
establishes hosted workflow/cloud behavior.

To exercise delegation decisions and role-based execution with actual agents, follow the
[native evaluation procedure](plugins/dev-core/skills/codex-collab/references/execution-evaluation.md).
Its helper prepares a disposable repository and grades behavior independently of
candidate-written tests. The helper itself does not call a model; native dispatch,
effective model metadata, and observed outcomes are recorded separately. The
procedure also defines matched parent-only, parent-with-review, and delegated
comparisons, plus model/effort comparisons against the prior Astra high baseline.
Required-review cases exclude the parent-only arm. A schema pass
or one native smoke does not establish a quality, cost, or latency advantage.

### Source update migration

- `hotl-engineering` 2.1.0 (2026-10-26): **BREAKING for template adopters**: the workflow
  templates no longer contain model IDs. Set the repository variables `HOTL_MODEL_LIGHT`
  (ai-review on every PR, incident-triage, agent-implement), `HOTL_MODEL_DEEP` (Tier 2
  deep review), and `HOTL_JUDGE_MODEL` (eval judge); a job whose variable is unset fails
  before the agent runs, and `run_evals.py` exits 2 without `JUDGE_MODEL`. The former
  Sonnet 4.5 default is deprecated. Every agent now gets an explicit `--tools` set plus
  `--setting-sources user` and `--strict-mcp-config`, so repository settings and
  `.mcp.json` cannot widen its permissions. `ai-review` pre-approves the PR comment tools
  and a write to one freshly created verdict file. `agent-implement` pre-approves only
  the plan comment, its own branch, commit and push, and lint / typecheck / test,
  installs dependencies before the agent, and opens the Draft PR from a separate job
  that runs neither the agent nor repository code. Adapted from cc-plugins.

  **BREAKING for eval template adopters**: the judge gate binarizes each axis at
  `judge.pass_score` (default 4) and gates on the pass rate per axis (an absolute floor
  plus an allowed drop from the baseline) instead of the mean of the summed three-axis
  score, which hid which axis dropped and could not be calibrated against human verdicts.
  In `thresholds.json`, replace `judge_total_floor` / `judge_total_drop_allowed` with
  `judge_axis_pass_rate_floor` / `judge_axis_pass_rate_drop_allowed` and add
  `judge.pass_score`; regenerate `baseline.json` with a calibration run that omits
  `--baseline`. `run_evals.py` stops before evaluating on the legacy keys, or on a baseline
  without per-axis pass rates or scored at another pass line. Cases below the pass line on
  any axis are reported as failed with the axis name. L3 calibration now measures per-axis
  agreement on binarized human and judge verdicts. Rate thresholds (floors, allowed drops,
  `must_pass_rate`) and the baseline's per-axis pass rates must be finite numbers from 0 to
  1, and `must_not_violations` a non-negative integer; NaN, null, or out-of-range values
  would silently make the comparison false and open the gate, so the run stops first.

  Every action in the templates and in this repository's CI moves to a major whose
  `action.yml` runs on Node 24 (GitHub removed Node 20 from hosted runners on 2026-09-23):
  checkout, setup-node, and setup-python v7, upload-artifact v7, download-artifact v8,
  github-script v9, create-github-app-token v3, configure-aws-credentials v6, azure/login
  v3, paths-filter v4, gitleaks-action v3, sticky-pull-request-comment v3, and
  pnpm/action-setup v6.1.0 (the floating `@v6` tag predates pnpm 12 support); use v5 for
  pnpm 10 or earlier. claude-code-action stays on v1. Self-hosted runners need v2.327.1 or
  later. `ai-review` now downloads each verdict by name into its tier directory, because
  download-artifact v5 and later extract a single pattern match directly into the path and
  the gate always saw the light verdict as missing. The App token keeps `app-id`
  (actionlint 1.7.12 does not know `client-id`). The default Node is 24, `deploy.yml`
  grants `id-token: write` per job and passes shellcheck, and `validate.yml` runs with
  `contents: read`.
- `hotl-engineering` 2.0.2 (2026-10-25): fix the shipped templates. Since anthropic
  SDK 1.0.0 (2026-08-20), `messages.create` rejects sampling parameters, so the eval
  runner's `temperature` made every judge vote fail and the fail-closed eval gate always
  blocked. The runner no longer sends sampling parameters and the template pins
  `anthropic[bedrock]>=1.17,<2` (2.x sends API version 2026-10-21, which the
  previous-generation judge does not support on Bedrock). `incident-triage` now passes a
  job-scoped read token, restricts the agent to read-only tools, passes the alert payload
  as a file, posts only the final answer to the Issue from a separate job, and falls back
  to a run link when no summary is available. `ci.yml` drops a "changed files" coverage
  step that actually enforced a whole-codebase threshold. Gate calibration now promotes
  on representative results rather than elapsed days. Adapted from cc-plugins.
- `ui-ux-pro-max` 1.3.1 (2026-10-25): ship the upstream MIT `LICENSE` and a `NOTICE.md`
  recording the upstream commit and local modifications.
- `dev-core` 5.5.0 (2026-09-23): adopt Sol medium for general implementation,
  Luna high for bounded research and routine edits, Luna max for settled bounded
  implementation, and Sol high for complex implementation. Keep Astra high parent
  and review recommendations. Add capability-checked implementation presets without
  overriding custom profiles, explicit selections, scope or review gates. See the
  [implementation record](docs/plans/task-sol-luna-routing.md) for validation,
  native smoke evidence, comparative limits and installation state.

- `dev-core` 5.4.0 (2026-09-17): choose delegation by independent work and expected
  benefit, and decide review separately by risk. Preserve the role model defaults
  and strict dispatch validation; let unavailable optional delegation fall back
  to suitable parent work without waiving required review or explicit selections.
  Align SessionStart and skills on proportional checks, verified evidence reuse,
  and same-path failure limits. Add cancellation/effort bounds and comparative
  evaluation cases. See the [implementation record](docs/plans/task-adaptive-delegation.md)
  for checks, behavior observations, and activation status.

- `dev-core` 5.3.0 (2026-09-12): recommend Astra high for the parent and add an
  optional read-only Sol medium researcher. Keep implementation/review at Astra
  high; permit an execution-only parent to use Astra medium. Preserve existing
  two-role custom profiles and reject requests for a missing researcher instead
  of merging in bundled defaults.

- `dev-core` 5.2.0 (2026-09-12): use Astra high for implementation and independent
  review; retain Astra medium as the parent recommendation. Narrow skill
  descriptions and load workflow/domain references only when relevant. Continue
  already-authorized work through its completion criteria without extra approval
  stops. Preserve TDD, ownership, model overrides, and evidence requirements.
- `indie-product-marketing` 0.3.0 and `ui-ux-pro-max` 1.3.0 (2026-09-12): focus
  discovery and guidance on the selected task; preserve existing product intent,
  brand, stack, and observed evidence instead of imposing a fixed recipe.

- `hotl-engineering` 2.0.1 (2026-09-12): scope assessment, templates, and
  consultation output to the actual delivery decision while preserving gate
  enforcement and recovery evidence.

See the [Astra refresh record](docs/plans/task-astra-skill-refresh.md) for the
article-based audit, scope, and validation limits. Earlier migrations:


- `dev-core` 5.1.2: recommend Astra medium for the parent and restore Sol medium
  as the ordinary implementation default. Retain Astra high independent review
  for substantial work; recommend a high-effort parent for difficult design or
  acceptance decisions. Keep small changes with one agent and select Astra
  medium for difficult implementation items. Compare requested routing with
  child runtime metadata when available. Reinstall and select the parent setting
  in the host; neither a profile edit nor reinstall changes the active parent.

- `dev-core` 5.1.1: change the bundled implementation default to Astra medium;
  retain Astra high for the parent recommendation and independent reviewer.
  Permit a documented Sol medium selection for bounded implementation work.
  Preserve explicit overrides and custom profiles; an unavailable Astra request
  does not silently fall back to Sol. Reinstall and start a new task to load the
  updated profile and instructions.

- `dev-core` 5.1.0: substantial approved-plan execution delegates implementation
  and independent review using the centralized execution profile. Explicit task
  overrides take priority. Supply capability observations from the current host;
  an unavailable requested model is reported without silent substitution. Parent
  recommendations do not change the host's selected model. Existing custom agent
  TOML files do not automatically import this profile.

- `dev-core` 5.0.0: the fallback runner returns `2` for incomplete verification
  (including no workload checks), `1` for failed checks, and `0` only for selected
  passing checks. Use project commands for nested workspaces and managed Python
  environments. Yarn/Bun audit needs an explicit version-appropriate command.
- `github-tools` 1.4.0: preserve dirty work and existing authorization; prepare
  local drafts without mandatory fetch, and use a body file for multiline PRs.
- `hotl-engineering` 2.0.0: install the trusted verdict validator before enabling
  AI-review enforcement; emit verdicts with the reviewed SHA; adapt target
  responses to include their deployed revision; implement recovery adapters
  before production deployment. See the bundled `assets/ADJUST.md`.

These are source versions. Reinstall from the intended marketplace source after
release, then verify the installed version in a new task; a source edit does not
prove the active cached plugin changed.

Optionally cross-check with the official validator bundled with Codex:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" plugins/dev-core
```

## Local development loop

After editing a plugin, bump its version (or add a `+codex.<timestamp>` cachebuster suffix), reinstall, and start a new thread:

```bash
codex plugin add dev-core@codex-plugins
```

## Research notes

Current Codex plugin/skill/hook guidance and the migration decisions behind this layout are recorded in `docs/research/codex-plugin-research.md`.

The development-workflow refresh, source evidence, prioritized findings, and
remaining deployment adaptations are recorded in
[the 2026-09-05 audit](docs/research/development-practices-2026-09-05.md).
