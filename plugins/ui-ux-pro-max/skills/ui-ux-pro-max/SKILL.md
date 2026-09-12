---
name: ui-ux-pro-max
description: Search bundled UI/UX patterns, palettes, typography, charts, and stack guidance when designing, implementing, or reviewing interfaces and making specific visual or usability choices.
---

# UI/UX Pro Max

Use the bundled design database to resolve a concrete interface decision, then
complete the requested design, implementation, or review. Treat search results
as candidate guidance to adapt to the product, not a specification to copy.

## Preserve the product context

Inspect the relevant interface, design tokens, components, and project guidance.
Identify the user's task, the interaction or visual decision in scope, and any
constraints on audience, platform, accessibility, or implementation.

Preserve the existing stack and accepted brand. For a new standalone prototype
with no stack constraints, use `html-tailwind` as an available starting point.
A palette request does not require a full redesign; a component repair does not
require choosing a new style, font, or page structure.

## Search for the missing information

Choose the domain or stack that can answer the current question. Use specific
product, interaction, or style terms; the bundled data uses English keywords.
Refine or combine searches when the results leave a material gap. Stop searching
when there is enough context to make the decision and do the requested work.

Use an available Python 3 runtime; the script needs only the standard library.
Run these commands from this skill's directory, or use the absolute path to its
`scripts/search.py` from another working directory. Data paths resolve relative
to the script, independently of the target project.

```bash
python3 scripts/search.py "keyboard navigation" --domain ux -n 3
python3 scripts/search.py "form validation" --stack react -n 3
```

Use `--domain` (`-d`) for a design category, or `--stack` (`-s`) for framework
guidance. Omitting both lets the script infer a domain. `--max-results` (`-n`)
defaults to 3; add `--json` for structured output. Stack search takes precedence
if both selectors are supplied.

If Python or the bundled data is unavailable, report that limitation and continue
work that does not depend on database access. Do not claim a search ran or install
a runtime merely to apply this skill.

| Domain | Use when deciding |
| --- | --- |
| `product` | Product-specific patterns and design considerations |
| `style` | Visual direction, surfaces, and effects |
| `typography` | Font pairings and typographic tone |
| `color` | Candidate palettes for a product or audience |
| `landing` | Landing-page structure and CTA placement |
| `chart` | Data representation and chart interactions |
| `ux` | Interaction, accessibility, and usability issues |
| `prompt` | Style vocabulary and CSS implementation keywords |

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`,
`react-native`, and `flutter`. Use the one that matches the project; the database
is not a reason to change frameworks.

## Apply and verify the result

Adapt useful findings to existing tokens and components. Choose typography,
colors, icons, spacing, and motion for the product's purpose and established
design language. Treat bundled framework examples, package recommendations,
and external links as reference material; verify version-sensitive decisions
against the project's versions and current official documentation.

For implementation, inspect the rendered interface and exercise the changed
interaction. Check the relevant supported viewports and themes, keyboard access,
visible focus, labels, contrast, and reduced-motion behavior when applicable.
Prevent clipping, hidden content, and unintended layout shifts. Run the project's
applicable checks and record gaps in browser, device, or accessibility coverage.

Return the requested artifact or actionable review, the material design choices,
and evidence from checks actually run. Distinguish database recommendations,
implemented behavior, and observed results; a search result does not establish
usability or accessibility compliance.
