# Global landing design skill

## Request and scope

Create a reusable international landing-page design skill in this marketplace from the Stride LP work and additional research of SPREAD and Circleback. Add it to the existing `indie-product-marketing` plugin. Preserve unrelated work and the Stride application's pending changes.

## Acceptance

- [x] Inspect the supplied public sites and distinguish observations from transfer hypotheses.
- [x] Draft an English action skill with bounded research, build, localization, and review modes.
- [x] Bundle dated reference notes, a decision playbook, a reusable brief, and behavior-case specifications.
- [x] Register the skill in plugin discovery metadata and repository documentation.
- [x] Run repository and official skill/plugin validators; check bundled references and diff hygiene.
- [x] Review the skill against its scenarios and state the limits of validation.
- [x] Verify preservation of pre-existing changes and record final evidence.

## Decisions

- Extend `indie-product-marketing`; no duplicate marketplace entry or new plugin dependency is needed.
- Use `global-landing-design` for the LP workflow and retain the existing marketing skill for broader acquisition and launch work.
- Keep the package self-contained. Generalize the Stride design reasoning without requiring its palette, implementation stack, or local files.
- Treat public marketing screens as presentation evidence, not verification of product execution or conversion outcomes.
- Preserve the base plugin version and refresh its development cachebuster with the official helper.
- Deliver repository source in this task. Source validation does not establish that an installed cache or a current conversation loaded the new skill.

## Baseline

On 2026-09-08, the target branch was `codex/cost-aware-execution` with seven pre-existing changed/untracked paths. The Stride checkout had 27. The repository plugin validator passed before edits. A temporary baseline captured file hashes and the dirty README contents so the requested additive edit can be distinguished from existing work.

## Research evidence

- Inspected [SPREAD](https://www.spread.ai/) and [Circleback](https://circleback.ai/) with public page text and desktop browser screenshots on 2026-09-08. Mobile product behavior, trial completion, and conversion performance were not verified.
- Read the Stride research record dated 2026-09-07 for Inkdrop, Granola, Things, Mobbin, UI Pocket, and bilingual prototype decisions. Preserved the dates and original evidence limits in the bundled reference notes.
- Read repository instructions and the system skill-creator and plugin-creator guidance before drafting.

## Verification

Executed on 2026-09-08 against the new repository files:

- `node scripts/validate-codex-plugins.mjs`: passed.
- Official `skill-creator/scripts/quick_validate.py` on `global-landing-design`: passed.
- Official `plugin-creator/scripts/validate_plugin.py` on `indie-product-marketing`: passed.
- The official validators ran with PyYAML 6.0.2 through an isolated temporary `uv` environment; no project runtime dependency was added.
- Bundled-reference check: all four local Markdown links from the skill resolved inside its package; UI metadata had the required skill invocation and a valid short-description length. The main skill was 113 lines.
- `git diff --check`: passed. An additional check included new Markdown files, which are not included by the default tracked-file diff.
- Baseline comparison: 33 pre-existing files across the two repositories remained byte-for-byte identical. The remaining pre-existing file, the dirty marketplace README, received insertions only; no old content was removed or replaced.
- Plugin metadata now advertises the skill; its official helper-generated version is `0.2.0+codex.20260908014838`. The existing marketplace entry and installed plugin cache were not changed.

Author review covered all seven scenario specifications:

| Scenario | Instruction coverage reviewed |
| --- | --- |
| Prelaunch page from references | Available-action selection, synthetic examples, and pipeline boundaries in steps 1, 3, 5, and 6 |
| Research-only and partial access | Mode boundaries and observed/text-only evidence in step 2 |
| Different brand and released trial | Preserve accepted design, current stack, and actual buying motion in steps 3, 4, and 6 |
| Whole-experience localization | Hidden UI text, artifacts, currency, mobile, and focus verification in steps 6 and 7 |
| Web-only validation | No interview prerequisite; outcome, denominator, source, language, and observation window in steps 1 and 7 |
| AI and data claims | Local ownership versus processing, synthetic labels, and limited endorsements in step 5 |
| Narrow unrelated tasks | Explicit scope exclusions before step 1 |

This review found no blocking instruction inconsistency within that scope. The scenarios have not been executed as isolated model evaluations, and automatic skill selection has not been tested in a fresh installed runtime. No new landing page, public deployment, demand experiment, or conversion result is claimed by this package update.

## Next action

The requested source package is complete. For a later iteration, use it on an actual LP task and record behavioral findings against the bundled cases. Loading the new skill as an installed plugin requires refreshing the intended marketplace source and using a new task. No commit, push, install, or deployment was performed in this task.

## Article-driven update — 2026-09-09

Request: read the user-supplied [Inkdrop design account](https://www.devas.life/how-i-designed-my-saas-landing-page-with-ai-tools/) and update this skill. The dated record above describes the original creation; this section records the new update.

### Progress and decisions

- [x] Read the complete public article text in the browser after web extraction failed. Keep its publication date separate from the access date.
- [x] Preserve the existing modes, brand flexibility, buying-motion choices, and availability boundaries.
- [x] Add a concise entrypoint and playbook guidance; extend the working brief and add two behavior-case specifications.
- [x] Apply the bounded source update and refresh the plugin version.
- [x] Run current repository/official validators and reference checks; inspect the incremental diff.
- [x] Refresh the installed plugin from the verified local marketplace and compare its cache with source.

Keep the article attribution compact. The additional browser-boundary and input-ownership checks are engineering adaptations for this skill, not claims that the author tested those exact conditions. Do not turn the article's tools or personal aesthetic judgments into universal requirements. This request updates skill instructions, not Stride's landing-page implementation.

The existing installed `indie-product-marketing@codex-plugins` was enabled at `0.2.0+codex.20260908014838`, sourced from this local repository. Preserve unrelated marketplace and Stride changes. No commit or push is in scope.

### Verification and next action

Executed on 2026-09-09:

- Repository plugin validation and `git diff --check`: passed.
- Official skill and plugin validators, using isolated PyYAML 6.0.2: passed.
- Five package-local links, including the new section anchor, resolved; UI metadata and Markdown whitespace checks passed. The entrypoint is 115 lines.
- Reviewed the incremental seven-file diff and the two new behavior specifications. These extend the existing seven cases; none is claimed as an executed model evaluation.
- Verified that 35 pre-existing files outside this bounded update remained byte-for-byte identical, including all pending Stride files and the marketplace README.
- The official version helper produced `0.2.0+codex.20260909053507`. `codex plugin add indie-product-marketing@codex-plugins` succeeded against the verified local source.
- Verified identical source/cache file inventories and bytes for the installed plugin. A fresh plugin listing reported the new version as installed and enabled.

The source and installed copy are updated. Use a new task to pick up the refreshed skill instructions. Runtime skill selection, a new LP implementation, device interactions, and demand outcomes were not evaluated by this documentation update. No commit or push was performed.

## Main delivery review — 2026-09-10

- The user requested review of all current changes and delivery to `main`.
  Include the six skill-package files, plugin discovery metadata and version,
  corresponding README documentation, and this creation record.
- A new independent read-only review found no actionable issues. The parent
  inspected the complete skill package and its metadata and repeated the
  package checks against the current files.
- Repository and official skill/plugin validators passed. All five local links
  and the section anchor resolved; UI metadata and whitespace checks passed.
  Repository Python tests also passed (59 tests, Python 3.12 / PyYAML 6.0.2).
- Preserve the original 2026-09-08 creation evidence and 2026-09-09 article update
  as dated history. The nine behavior specifications remain unexecuted model
  evaluations; source checks do not establish automatic skill selection or LP
  outcomes. Verify the published revision and CI separately after push.
