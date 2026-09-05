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

## Dev Core Entrypoints

Use narrow skills for daily work; `dev-workflow` provides shared orchestration.

| Skill | Use for |
| --- | --- |
| `$dev-grill` | Pressure-test a plan or decision one material question at a time; explicit invocation only. |
| `$dev-task` | Turn an idea into a design plan, acceptance criteria, BDD scenarios, and TDD iterations (template bundled). |
| `$dev-execute` | Execute an existing plan through branch/worktree prep, TDD, verification, review, and refactor gates. |
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

### Source update migration (2026-09-05)

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
