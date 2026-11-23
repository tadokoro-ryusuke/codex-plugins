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
| The measurement script is covered by tests written before the implementation | satisfied | 26 tests; the first run failed on the missing module |
| The count-only script has been reviewed independently | satisfied, with open findings | Round 4 reviewed it; its small findings are applied and two findings about the decision rule are open. The fixes made after round 4 were checked by tests only |
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
  run protocol, what the script reports, how to judge a difference against
  same-day repeats, analytics behavior, and blind spots.
- `references/off-site-rules.md`: the Own / Claim / Earn / Contest / Leave
  routes and rulings on off-site tactics under Japanese, US, EU, and UK rules
  and platform policies.
- `assets/`: question map, prompt set and snapshot log, source ledger, page
  action table.
- `scripts/visibility-stats.mjs`: validates run records and reports observed
  counts and rates per engine, surface, and prompt type, and the difference
  between two snapshots on the questions that are the same in both. It reports
  no confidence interval and no verdict. Node standard library only.
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

Reviewer for every round: Codex CLI 0.166.0, `gpt-6.2-astra`, reasoning effort
high, read-only sandbox, one-shot (settings confirmed from the client's startup
output each time). No conclusion or author's assessment was passed. Each finding
was checked against the code or the source before it was used.

| Round | Input | Result |
| --- | --- | --- |
| 1 | The whole candidate at `ed28ccd` plus the uncommitted skill, the repository rules, and the saved source copies | 44 findings (7 P1, 29 P2, 8 P3) |
| 2 | The script, its tests, and the measurement text at `17e4e34` | 26 findings (5 P1, 13 P2, 8 P3) |
| 3 | The same files after the script was redesigned | 29 findings (3 P1, 14 P2, 12 P3) |
| 4 | The count-only script, its tests, the measurement text, and the prompt-set template at `424967d` | 26 findings (2 P1, 9 P2, 15 P3) |

**Round 1, applied.**

- Script: a uniform change produced a directional verdict without an interval;
  rows from different surfaces could be pooled or compared; a missing `branded`
  flag defaulted to unbranded; a re-imported row changed the rate; a group
  present in one snapshot was dropped from a comparison; failed and answerless
  runs had no status. The script now requires `surface`, `run_id`, and
  `branded`, and accepts `question_id` and `status`.
- Rulings: disclosure of review incentives; neutral quotation versus selective
  reuse of reviews; the site reputation policy for paid placements; who may be
  invited to review.
- Privacy: prompts built from customer conversations must have identifying and
  confidential details removed.
- Source fidelity: the Ahrefs overlap figure counted result blocks; the "best X"
  figure came from top-of-funnel recommendation prompts; two Graphite figures
  were quoted without their unit; the agency study's circularity concern applied
  to different metrics than stated; schema results in that study cover
  third-party pages only; the domain finding does not rank causal levers; the
  Microsoft transition has a deadline and steps; Search Console settings inherit
  and can be overridden; operator reports can be absent or blank below a
  threshold; one enforcement example described settled allegations.
- Skill text: templates are copied into the user's project and never filled in
  place; the eligibility check is scoped to a live site; the description expands
  the acronyms; the automation prohibition names community posting and voting.
- Not adopted: a statement that G2 bars a seller from offering an incentive
  without notifying G2 was not found in the saved G2 guidelines.

**Rounds 2 and 3, and the decision they led to.** Both rounds found that the
script's intervals did not keep their stated coverage. Round 2 showed, and an
exact calculation confirmed, that an interval built from the spread between
questions covered the true rate about 87% of the time in a sparse case and
measured the wrong uncertainty for a fixed prompt set. The script was redesigned
around run-to-run variation with Wilson and Newcombe score intervals. Round 3
showed that this also failed when answered runs carried unequal weight: coverage
fell to 55% in one constructed case and a single random answer could produce a
directional verdict.

After three revisions of the same component, the inference was removed instead
of revised again. The script now validates records and reports observed counts
and rates. The documents tell the reader to judge a difference against same-day
repeats of the same set, on a comparison named in advance, and to confirm it in
a further snapshot. The findings about validation, pairing, missing answers,
variant weights, labels, and command-line handling from all three rounds are
applied in that version, except the two listed under Remaining; the findings
about calibration no longer apply.

**Round 4, on the count-only script.** The user asked for one more review and
asked that findings about the design be reported before they are changed.

- Applied: unknown and misspelled field names are rejected, with free-form
  detail under `notes`; a question that groups several prompts needs an explicit
  `question_id` on each; the summary shows complete and recorded questions side
  by side and labels each count with its population; the equal-weight flag
  accounts for answered runs outside complete questions; a one-sided group with
  a very large number of questions no longer fails; a value that would round to
  0.0% or 100.0% is shown as `<0.1%` or `>99.9%`; JSON field names carry the
  rate, the population, and the direction; variants are added in a fixed order,
  so identical records give an exact zero difference; notes carry raw
  identifiers; whole-group run counts are always printed; the documents state
  that the script knows only the prompts in the file and groups by snapshot,
  engine, and surface.
- Open, reported to the user and not changed: two P1 findings about the written
  rule for judging a difference. With sparse hits, two same-day snapshots with
  no hits followed by two later snapshots with one hit each satisfy "larger than
  the same-day difference, and persisting" at an unchanged underlying rate. And
  each comparison selects its own paired questions, so a baseline-to-follow-up
  and a baseline-to-confirmation comparison can rest on different questions.
- Not applied: duplicate JSON keys are still not detected.

The fixes made after round 4 were checked by tests only.

## Verification

Executed on 2026-11-23 on the final version:

- `node scripts/validate-codex-plugins.mjs`: passed.
- `node scripts/validate-skill-evals.mjs`: passed (68 cases, none for this
  plugin).
- `node --test plugins/indie-product-marketing/skills/ai-search-visibility/scripts/visibility-stats.test.mjs`:
  26 tests passed.
- `uv run --python 3.12 --with PyYAML==6.0.2 --with "anthropic[bedrock]>=1.17,<2" python -m unittest discover -s scripts/tests -q`:
  127 tests passed.
- `git diff --check`: clean.

These checks cover packaging, text references, and the script. They do not
execute the skill with a model or test automatic skill selection.

## Remaining

- Merge PR #7 before this branch, then push this branch and open a pull request.
- Reinstall the plugin and start a new task to load the skill.
- Decide how to resolve the two open round-4 findings about the decision rule.
  The reviewer's suggestion: stop calling a change real; report first observed
  hits and whether they recur, apply a business threshold written in advance,
  and judge persistence only on one common set of questions across all the
  snapshots involved.
- The script does not detect a JSON object that repeats a key; the parser keeps
  the last value.
- Decide whether to add a calibrated interval later. It would need a design the
  data can meet, such as a balanced set with one prompt per question, and its
  own validation.
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
