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
| `$dev-execute` | Coordinate an approved plan with role-specific implementation and independent review, TDD, and evidence gates. |
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

For substantial planned work, `dev-execute` keeps the parent coordinating and
delegates implementation and a separate review. Default model/effort assignments
live in one [execution profile](plugins/dev-core/skills/codex-collab/assets/execution-profile.json).
The bundled defaults are Astra high for the parent, implementer, and independent
reviewer, with Sol medium for optional read-only research. Use research for bounded
source lookup or log classification; keep design and acceptance judgments with the
parent. An execution-only parent may use Astra medium when the plan is settled.
The profile recommends the parent setting; choose that model in the task's host.
The plugin resolves explicit child requests against the host's exposed models
and effort settings, without silently falling back to another model.

The [execution contract](plugins/dev-core/skills/codex-collab/references/planned-execution.md)
defines bounded writes, parent decisions, fresh handoffs, review independence,
and evidence. Use the bundled Astra high implementation default for ordinary
and difficult work. Preserve explicit task selections and custom profiles, and
record authorized overrides before dispatch. Check the actual parent
setting separately: a profile recommendation cannot change the running task.
Native tools accepting model/effort arguments do not require installing custom
role files. Read-only task instructions and role names alone
do not establish an enforced sandbox. Small steps can stay with the parent when
delegation would add unnecessary overhead; explicit user preferences take priority.

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

To exercise role-based execution with actual agents, follow the
[native evaluation procedure](plugins/dev-core/skills/codex-collab/references/execution-evaluation.md).
Its helper prepares a disposable repository and grades behavior independently of
candidate-written tests. The helper itself does not call a model; native dispatch,
effective model metadata, and observed outcomes are recorded separately.

### Source update migration

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
