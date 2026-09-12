---
name: conventions-as-guardrails
description: "Convention enforcement for repository tooling and agent instructions. Use when encoding recurring rules or reducing an overloaded AGENTS.md."
---

# Conventions as Guardrails

Translate stable, mechanically checkable conventions into the repository's tooling.
Keep domain intent and non-obvious operating constraints in concise documentation.
Use the target project's rules and language; do not install a universal starter
kit or change established architecture during a focused convention fix.

Inspect the actual violation and its source of truth. Use deterministic checks for
syntax or dependency rules, semantic review for meaning, and owner decisions for
material contract or policy changes. A passing check proves only its encoded rule;
it does not make the entire convention unbreakable.

## Select the enforcement surface

- For formatter, linter, architecture tests, or agent hooks, read
  [tooling and hooks](references/tooling-and-hooks.md).
- For writing or trimming `AGENTS.md`, read
  [agent instructions](references/agent-instructions.md).
- For an explicit logging-convention task, read
  [structured logging](references/structured-logging.md).

Reuse established naming and domain language. Create a naming table only when the
project needs a shared contract; do not duplicate formatter or linter settings in
prose. API naming follows the authoritative API contract and `$backend-patterns`,
not the screen-design spec.

## Authority and completion

Resolve routine configs and justified narrow suppressions under existing task and
repository authority. Preserve required reason comments and review gates. Ask the
owner only for a material policy waiver, permission expansion, or business decision
outside existing authority; do not reopen already agreed conventions.

Demonstrate the changed guardrail against a representative permitted case and a
real violation. Run the relevant project checks and report remote enforcement or
hook invocation that was not exercised. Complete the requested surface; a linter
fix does not also require new hooks, architecture tests, and log retention policy.

Use `$continuous-learning` when recurring failures justify a durable guardrail,
`$test-design` for testing strategy, or `$cicd-release-design` for delivery gates.
