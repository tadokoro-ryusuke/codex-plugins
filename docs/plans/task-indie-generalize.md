# Indie product marketing generalization

## Outcome and authorization

Release `indie-product-marketing` 0.3.1 as a public, host-neutral knowledge
source. Replace identifiers from a private product study with generic
descriptions and make bundled references and assets readable on any agent host.
Keep the guidance, reference observations, and behavior cases otherwise
unchanged. This repository remains the source of truth; cc-plugins receives a
one-way Japanese adaptation.

Delivery authorization: the user approved pushing this change. Deliver it on
branch `codex/indie-generalize` through a pull request; verify the remote
revision and CI separately after push.

## Completion contract

| Criterion | State | Evidence |
| --- | --- | --- |
| No private product name, provisional price, or private repository path remains in the plugin | satisfied | Plugin-wide search for the former identifiers returned no matches |
| Bundled references and assets use neutral skill names; SKILL.md keeps native `$skill` syntax | satisfied | `$`-token search over `skills/*/references` and `skills/*/assets` returned no matches |
| Version, README, and sibling-repository ownership are recorded | satisfied | `plugin.json` 0.3.1; README description and migration entry; AGENTS.md sibling note |
| Repository validators and offline tests pass | satisfied | Verification below |

## Changes

- `global-landing-design`: the SKILL.md reference list, the reference-pattern
  sources and case heading, and two behavior cases now use generic descriptions
  such as "a prelaunch desktop productivity prototype" and "a provisional USD
  price". The case keeps
  its dated decisions and its reasoning about carrying a mechanism across
  languages. The private study location is not recorded. Third-party public
  observations are unchanged.
- `indie-idea-discovery`: two references and the validation-handoff asset hand
  off to "the indie-product-marketing skill" instead of Codex `$skill` syntax.
- `.codex-plugin/plugin.json` version 0.3.1. The marketplace entry carries no
  version and needs no change.
- README: generic label in the landing-design description and a 0.3.1
  migration entry.
- AGENTS.md: this repository owns the plugin's domain knowledge; cc-plugins owns
  only its Claude Code runtime reference.

## Verification

Executed on 2026-09-23:

- `node scripts/validate-codex-plugins.mjs`: passed.
- `node scripts/validate-skill-evals.mjs`: passed (57 cases).
- `uv run --python 3.12 --with PyYAML==6.0.2 python -m unittest discover -s scripts/tests -q`:
  71 tests passed.
- The plugin-wide search for the former identifiers and the `$`-token search
  over references and assets: no matches.
- No anchor links pointed to the renamed reference-pattern heading.

These checks cover packaging and text. They do not execute the behavior cases
with a model or test automatic skill selection in an installed runtime.

## Remaining

- An earlier creation record in `docs/plans/` still names the private product.
  Generalizing it is a separate decision.
- The cc-plugins runtime reference named in AGENTS.md is added by the
  corresponding cc-plugins adaptation.
- After merge, reinstall `indie-product-marketing@codex-plugins` and start a new
  thread to load 0.3.1.
