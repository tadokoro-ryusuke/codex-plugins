# AI search visibility skill

## Outcome and authorization

Release `indie-product-marketing` 0.4.0 with a fourth skill,
`ai-search-visibility`, for work on AI answer engines (often called AEO, GEO,
or LLMO): crawler eligibility, mention and citation measurement, page and
third-party-source decisions, and audits of vendor claims. This repository is
the source of truth; cc-plugins receives a one-way Japanese adaptation.

Delivery authorization: the user approved building the skill here first and
adapting it to cc-plugins. The change is committed on branch
`codex/indie-ai-search-visibility`. It is not pushed and no pull request is
open; both wait for the user.

The branch merges `codex/indie-generalize` (open PR #7, plugin 0.3.1), because
the cc-plugins copy of this plugin is synchronized to that branch. PR #7 has to
be merged first, or this branch delivers its two commits as well. The merge
needed one manual resolution in the README migration list, where both sides had
added entries.

## Completion contract

| Criterion | State | Evidence |
| --- | --- | --- |
| The skill ships SKILL.md, four references, four templates, a tested script, and `agents/openai.yaml` | satisfied | Files under `plugins/indie-product-marketing/skills/ai-search-visibility/` |
| Statements in the references are supported by the cited source | satisfied for the statements checked; exceptions listed under Remaining | Source check below |
| The skill excludes undisclosed posts, bought or exchanged links, assistant-manipulation instructions, and unrequested external actions | satisfied | SKILL.md "Sort gaps" and "Respect action boundaries"; `references/off-site-rules.md` |
| The measurement script is covered by tests written before the implementation | satisfied | 24 tests; the first run failed on the missing module |
| An independent review ran on the candidate and its findings were verified before use | satisfied | Independent review below |
| Version, README, sibling routing, and CI are updated | satisfied | `plugin.json` 0.4.0; README list, validation command, and migration entry; routing sentences in the sibling skill and its channel reference; `validate.yml` step |
| Repository validators and offline tests pass | satisfied | Verification below |
| The skill triggers and behaves as intended in an installed runtime | pending | No behavior case was executed |

## Changes

- New skill `ai-search-visibility` with five modes: eligibility check, baseline
  measurement, gap and action plan, claim or vendor audit, re-measurement.
- `references/engine-eligibility.md`: what Google, OpenAI, Perplexity,
  Anthropic, and Microsoft state about eligibility, controls, measurement, and
  manipulation, with a checklist and a list of claims that have no first-party
  support.
- `references/evidence-base.md`: evidence grades, an audit of common claims,
  and questions for auditing a vendor proposal or case study.
- `references/measurement.md`: metric definitions, prompt-set construction, the
  run protocol, how the script computes and what its intervals mean, analytics
  behavior, and blind spots.
- `references/off-site-rules.md`: the Own / Claim / Earn / Contest / Leave
  routes and rulings on off-site tactics under Japanese, US, EU, and UK rules
  and platform policies.
- `assets/`: question map, prompt set and snapshot log, source ledger, page
  action table.
- `scripts/visibility-stats.mjs`: mean per-question mention and citation rates
  with approximate 95% intervals and paired comparison of two snapshots. Node
  standard library only.
- `indie-product-marketing` SKILL.md and `references/channel-strategy.md` route
  AI-answer work to the new skill.
- `.codex-plugin/plugin.json` 0.4.0, README, and a `node --test` step in
  `.github/workflows/validate.yml`.

The skill names one agency's case study as the worked example for the claim
audit and credits its two frameworks. Prohibited tactics are stated in general
form and are not attributed to any company.

## Source check

Executed on 2026-11-23. Each source was fetched as raw HTML or PDF and the
passage behind each statement was read in context: the operator pages for
Google, OpenAI, Perplexity, and Anthropic; Microsoft's two blog posts and its
security post; the Consumer Affairs Agency designation Q&A, operating standard,
and one order; 16 CFR 255.1, 255.5, 465.2, 465.4, 465.5, 465.6, 465.8 and two
FTC guidance pages; the EU directive annex and the UK schedule; Wikipedia,
Trustpilot, and G2 policies; and the studies cited in the evidence base. The
Bing Webmaster Guidelines page renders with JavaScript, so its statements were
read in a rendered browser session and no static copy exists.

## Independent review

Reviewer: Codex CLI 0.166.0, `gpt-6.2-astra`, reasoning effort high, read-only
sandbox, one-shot (settings confirmed from the client's startup output). Input:
the working tree at `ed28ccd` plus the uncommitted candidate, the repository
rules, and the saved source copies. No conclusion or author's assessment was
passed. Result: completed, 44 findings (7 P1, 29 P2, 8 P3).

Each finding was checked against the code or the source before it was used.

- **Script (P1 and P2).** Confirmed and fixed: a uniform change produced a
  directional verdict without an interval; rows from different surfaces could be
  pooled or compared; a missing `branded` flag defaulted to unbranded; a
  re-imported row changed the rate; a group present in one snapshot was dropped
  from a comparison; the difference interval could exceed the possible range;
  the tables omitted counts; failed and answerless runs had no status. The
  script now requires `surface`, `run_id`, and `branded`, accepts `question_id`
  and `status`, and reports mean per-question and pooled figures.
- **Interval wording (P1).** Confirmed. The documents now call the interval
  approximate, state the sampling assumption, and tell the reader to group
  prompt variants under one question.
- **Rulings (P1).** Confirmed against the sources and fixed: disclosure of
  review incentives; neutral quotation versus selective reuse of reviews; the
  site reputation policy for paid placements; who may be invited to review.
- **Privacy (P1).** Confirmed. Prompts built from customer conversations must
  have identifying and confidential details removed.
- **Source fidelity (P2).** Confirmed and fixed: the Ahrefs overlap figure
  counted result blocks; the "best X" figure came from top-of-funnel
  recommendation prompts; two Graphite figures were quoted without their unit;
  the agency study's circularity concern applied to different metrics than
  stated; schema results in that study cover third-party pages only; the domain
  finding does not rank causal levers; the Microsoft transition has a deadline
  and steps; Search Console settings inherit and can be overridden; operator
  reports can be absent or blank below a threshold; one enforcement example
  described settled allegations.
- **Skill text (P2 and P3).** Confirmed and fixed: templates are copied into the
  user's project and never filled in place; the eligibility check is scoped to a
  live site; the description expands the acronyms; the automation prohibition
  names community posting and voting.
- **Not adopted.** One statement in a finding, that G2 bars a seller from
  offering an incentive without notifying G2, was not found in the saved G2
  guidelines. The ruling states only what that page supports.

## Verification

Executed on 2026-11-23 after the review fixes:

- `node scripts/validate-codex-plugins.mjs`: passed.
- `node scripts/validate-skill-evals.mjs`: passed (68 cases, none for this
  plugin).
- `node --test plugins/indie-product-marketing/skills/ai-search-visibility/scripts/visibility-stats.test.mjs`:
  24 tests passed.
- `uv run --python 3.12 --with PyYAML==6.0.2 --with "anthropic[bedrock]>=1.17,<2" python -m unittest discover -s scripts/tests -q`:
  127 tests passed.
- `git diff --check`: clean.

These checks cover packaging, text references, and the script. They do not
execute the skill with a model or test automatic skill selection.

## Remaining

- Merge PR #7 before this branch, then push this branch and open a pull request.
- Reinstall the plugin and start a new task to load the skill.
- Run behavior cases in an installed runtime: a citation baseline, a
  vendor-only audit, ordinary crawler troubleshooting and geographic
  landing-page work as negatives, and a request for an undisclosed post.
- Reddit's rules pages and help center refused automated retrieval. The Reddit
  rows rest on the User Agreement as filed with the New York Attorney General
  and on help-center excerpts returned by search.
- Two enforcement notes about Reddit moderators and Reddit's public statement
  are marked as reported and were not re-checked.
- Engine operators changed their documentation several times in 2026. Re-read
  `references/engine-eligibility.md` against the live pages at the next
  freshness audit.
