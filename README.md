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
| `$dev-task` | Turn an idea into a design plan, acceptance criteria, BDD scenarios, and TDD iterations (template bundled). |
| `$dev-execute` | Execute an existing plan through branch/worktree prep, TDD, verification, review, and refactor gates. |
| `$dev-debug` | Investigate errors from root cause before fixing. |
| `$dev-tdd` | Run a focused test-first cycle for one behavior or regression. |
| `$dev-review` | Review with dev-core criteria: behavior, security, tests, architecture, maintainability, conventions. |
| `$dev-refactor` | Refactor safely without behavior changes. |
| `$dev-e2e` | Run or diagnose Playwright E2E tests. |
| `$dev-checkpoint` | Capture resumable state for handoff or continuation (template bundled). |
| `$verification-loop` | Six-step evidence-based verification; bundles `scripts/verify.sh`. |
| `$codex-collab` | Independent review, rescue, parallel subagents; bundles custom agent roles. |
| `$continuous-learning` | Turn a mistake into durable prevention (rules, hooks, tests). |
| `$dev-workflow` | Shared multi-phase orchestration when no narrower skill fits. |

Reference skills `$best-practices`, `$backend-patterns`, and `$frontend-patterns` are loaded on demand (not injected implicitly) to keep the always-on skill list small.

`dev-task` writes durable plans under `docs/plans/task-<slug>.md`. `dev-execute` treats those plans as executable contracts. `codex-collab` ships ready-made custom agent roles (`code-reviewer`, `security-auditor`) you can copy into `.codex/agents/`.

## HOTL Engineering

`$hotl-engineering` has two modes. Apply mode assesses a repository (stack, deploy target, risk paths, team, audit requirements), classifies its nature (experimental / internal / production / agent-based), proposes a proportional gate subset, and applies bundled GitHub Actions templates (5-layer CI, two-tier AI review, staged deploy with approval and auto-rollback, eval gate, read-only incident triage, issue-to-agent implementation) — always starting in observation-only Phase 1 and pushing back on "install everything" requests for experimental repos. Consult mode answers engineering-management questions (buy-vs-build, agent autonomy promotion, auto-merge, contractor permissions, audit explanations) grounded in `references/principles.md` and `references/decision-frameworks.md`, and always takes a position.

For assessment only, ask it to stop after the plan: "Use $hotl-engineering to assess this repo and stop before applying templates."

## Validation

```bash
node scripts/validate-codex-plugins.mjs
```

This checks the marketplace catalog, plugin manifests, SKILL.md frontmatter, `agents/openai.yaml` files, bundled file references, and hooks configuration. CI runs the same script plus hook and script smoke tests on every push.

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
