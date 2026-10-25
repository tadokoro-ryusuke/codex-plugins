# Pipeline design

Place each check where it gives useful feedback before the risk it guards:

| Stage | Typical responsibility |
|---|---|
| Pull request | Focused lint, types, tests, and affected build/integration/security checks |
| Merge | Broader regression and packaging against the exact merged revision |
| Release | Remaining environment, runtime, and exposure checks |

Adapt stages to the existing delivery system; a fixed number of stages or minutes
is not a requirement. Preserve required coverage and security gates. Investigate
flakes before an authorized quarantine with an owner, expiry, tracked failure,
and replacement coverage for critical paths; see `$test-design` if needed. Put the
quarantine procedure (label, skip method, owner, expiry, return condition) in the
pipeline template, and record runner-specific settings with their versions. For
example, Playwright 1.62 added `retryStrategy: 'isolated'`, which runs retries one
by one at the end of the suite to reduce interference; do not make it a blanket
default. Playwright 1.63 added test locks, which serialize only tests sharing a lock
name; try isolating state and data first, use a lock only for a resource that cannot
be isolated, and never serialize the whole suite. Source:
https://playwright.dev/docs/release-notes (checked 2026-10-26).

Consolidate verification commands using the stack's existing scripts or task
runner so local and CI behavior can be reproduced. Validate workflow behavior and
failure paths, not just YAML syntax. Report which checks ran locally and which
remote enforcement remains unverified.

## Dependency audit gate

Define the vulnerability gate once per project, here, and point local verification
and CI templates to it. When thresholds differ between files, an agent can choose
whichever passes.

- The gate is "the configured audit command passes at the configured threshold".
  Start by failing at High or above (for example, `pnpm audit --audit-level high`);
  record a different threshold and its reason in an ADR.
- Use CISA KEV and EPSS for ordering, deadlines, and exception rationale, not as
  gate conditions: KEV-listed first and immediately, high EPSS next with a deadline,
  other Critical/High in scheduled maintenance, Low or unreachable recorded and
  watched. Map these to response deadlines where a maintenance agreement defines them.
- Do not make "unreachable" or "not in KEV" an automated pass condition. Standard
  audit commands (`npm audit`, `pnpm audit`, `pip-audit`, `cargo audit`) judge known
  advisories and severity, not KEV listing or reachability, so such a condition lets
  an agent pass the gate by assertion.
- Accept exceptions only through an exceptions file (or a VEX document) with a
  reason, expiry, and approver per entry. Protect it with CODEOWNERS so an agent
  cannot add its own entries, and fail the gate on expired entries.
- To fail on KEV-listed findings below the threshold, add a scripted check: a scanner
  that reports KEV/EPSS (for example, Grype) or a match against the CISA KEV catalog.
- If you draw a line on EPSS scores, revisit it at each EPSS model update; the same
  score can mean something different. The 2026-10-25 score data used model_version
  v2026.06.15; the FIRST EPSS SIG maintains the scores and Empirical Security
  generates and publishes them (sources: https://www.first.org/epss/,
  https://epss.empiricalsecurity.com/epss_scores-current.csv.gz; checked 2026-10-26).
- Report a passing gate as "no findings at or above <threshold>", never "no
  vulnerabilities", and list excluded items with reason and expiry.

## Credentials and workflow integrity

Use short-lived workload identity such as OIDC where supported. Environment
protection and a secrets manager serve different purposes and may complement it;
choose from the actual provider and organization constraints rather than a fixed
product hierarchy. Keep credentials out of source, ordinary repository variables,
and logs, and avoid reading secret values merely to inspect configuration.

For GitHub Actions, pin third-party actions to reviewed commit SHAs and declare
least-privilege `permissions`. Separate untrusted contribution code from privileged
secrets and write tokens. Protect workflow changes through the repository's review
policy; propose CODEOWNERS or environment protections when they address a concrete
gap, and apply remote changes only within existing authorization.

- Enforce SHA pinning with the enterprise, organization, or repository allowed
  actions policy so a workflow using an unpinned action fails; automate pinning
  and updates (for example, Renovate) instead of editing pins by hand.
- Avoid `pull_request_target` and `workflow_run`. These triggers run with the base
  repository's secrets and write permissions even for fork PRs, so checking out
  fork code hands it those privileges. If one is unavoidable, never check out the
  fork head and pass no secrets or write permissions. GitHub's default rule that
  disables `pull_request_target` covers only public repositories; for private or
  internal repositories, configure execution-protection event rules yourself.
- Pass untrusted values such as `${{ github.event.* }}` to `run:` steps through
  environment variables, never inline, to prevent script injection. Lint workflows
  with actionlint or zizmor, starting in warning mode before making them required.
- Run any CI job that gives an agent untrusted input (issue or PR text, fork code)
  separately from jobs holding write permissions or secrets.

Harden dependency intake by default, because a compromised version or install
script reaches CI secrets the moment it installs:

- Wait 3 to 14 days before adopting newly published versions, paired with an
  exception path that takes security fixes immediately.
- Deny dependency install scripts by default and allowlist only the packages that
  need them, such as native builds.
- Commit the lockfile and install in CI without rewriting it (`npm ci`,
  `pnpm install --frozen-lockfile`, `uv sync --locked`).
- When the project publishes packages, use Trusted Publishing (OIDC) and remove
  long-lived publish tokens.

Which of these apply by default depends on the tool and version. For the current
defaults, setting names, and GitHub Actions controls with sources and check
dates, read [supply chain](supply-chain.md).

Keep dependency updates maintainable. Add artifact provenance, SBOM, or other
supply-chain controls when the delivery requirements justify them; the current
SLSA release is v1.2, published 2025-11-24 with a new Source Track (source:
https://slsa.dev/blog/2025/11/announce-slsa-v1.2, checked 2026-10-26). Recheck
current official provider guidance for implementation syntax and platform behavior.

Do not claim a passing pipeline establishes device behavior, production health,
or client acceptance. Retain the exact revision, command/job, result, and relevant
environment needed to assess what the evidence proves.
