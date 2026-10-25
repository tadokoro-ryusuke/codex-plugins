# Supply chain: dependency intake and GitHub Actions

Detail for the supply-chain rules in [pipeline design](pipeline-design.md). The
principles live there; this file keeps only facts that change with versions and dates.

- **Checked 2026-10-26.** Setting names, defaults, and dates change quickly. Before
  applying one to a project, confirm the current value at its source.
- The vulnerability gate (which severity fails and how exceptions work) is defined
  in the "Dependency audit gate" section of pipeline design, not here.

## 1. Cooldown for newly published versions

Principle: wait 3 to 14 days before adopting a new version, always paired with an
exception path that takes security fixes immediately. Compromised versions spread
right after publication and are often detected and removed later; waiting without
an exception path also delays fixes.

| Tool | Applies by default? | Setting | Exception path |
|---|---|---|---|
| Dependabot version updates | **Yes**: waits 3 days after publication (since 2026-07-14) | `cooldown` in `dependabot.yml` changes or disables it | Security updates open PRs without waiting |
| pnpm 11 and later | **Yes**: 11.0.0 (2026-04-28) made `minimumReleaseAge` default to 1440 minutes (1 day); the current docs (pnpm 12 line) still show 1440 | Raise `minimumReleaseAge` in `pnpm-workspace.yaml`; 0 disables it | `minimumReleaseAgeExclude`; `pnpm audit --fix` adds fixed versions there automatically |
| npm 10 (Node 22 bundles 10.9.9) | No | Only `--before` (a date); no day-based setting | — |
| npm 11 (Node 24 bundles 11.19.1, Node 26 bundles 11.20.0) | **Needs explicit setting** (`min-release-age` defaults to null) | `min-release-age` in `.npmrc` (days; 11.10.0 and later) | `min-release-age-exclude` (11.17.0 and later) |
| npm 12 | **Needs explicit setting** (default null) | Same as npm 11 | Same as npm 11 |
| Renovate | Depends on presets; `config:best-practices` includes 3 days for npm (`security:minimumReleaseAgeNpm`) | `minimumReleaseAge` | Override per package with `packageRules` |
| uv | **Needs explicit setting** (`exclude-newer` has no default) | `exclude-newer`; accepts a timestamp or a duration such as `7 days` or `P7D` | Set `exclude-newer-package` to `false` for a package |
| pip | **Needs explicit setting** | `--uploaded-prior-to` (added in 26.0; durations such as `P3D` from 26.1) | — |

- A cooldown can also block fixed versions. npm warns and exits non-zero when
  `min-release-age` prevents `npm audit fix` from installing a fix. Prepare the
  exception path first.
- Even when Dependabot security updates are immediate, check that the package
  manager's own cooldown does not stop the install.

## 2. Install scripts (lifecycle scripts)

Principle: deny dependency install scripts by default and allowlist only the
packages that need them; allow native builds (for example, packages using node-gyp)
individually. `postinstall` and similar scripts run arbitrary code at install time
and, in CI, can reach secrets and tokens.

| Tool | Denies by default? | Setting |
|---|---|---|
| pnpm | **Yes**. Since 10.0.0 (2025-01-07) it does not run dependency lifecycle scripts. In 11.0.0 `strictDepBuilds` defaults to true and an unlisted build script is an error | Allow with `allowBuilds` (11.0.0 replaced `onlyBuiltDependencies` and related settings) |
| npm 12 | **Yes**. Since 12.0.0 (2026-07-08) it blocks dependency scripts not allowed by the root `allowScripts` | Record approval with `npm install-scripts approve`, then run them with `npm rebuild`; `strict-allow-scripts=true` fails the install when unreviewed scripts exist |
| npm 11 | **No**. `allowScripts` exists, but unreviewed scripts run with a notice | `strict-allow-scripts=true` (fail on unreviewed) or `ignore-scripts=true` |
| npm 10 | **No** | `ignore-scripts=true` |

- `ignore-scripts=true` also stops your own package's lifecycle scripts and the
  pre/post scripts of `npm run`. Check that the build still works.
- npm 12 also denies git dependencies and URL tarball dependencies by default
  (`allow-git` / `allow-remote` default to `none`). Allow them explicitly in
  `.npmrc` if you use them.

## 3. Lockfile and frozen install

- Commit the lockfile. Install in CI without rewriting it: `npm ci`,
  `pnpm install --frozen-lockfile`, `uv sync --locked`. A CI that resolves versions
  outside the lockfile pulls in unreviewed dependencies.
- npm 12 no longer reads `npm-shrinkwrap.json`; rename it to `package-lock.json`.

## 4. Publishing packages (Trusted Publishing)

When the project publishes packages, publish through Trusted Publishing (OIDC) and
remove long-lived publish tokens.

- **npm**: Trusted Publishing needs npm CLI 11.5.1 or later. Publishing from GitHub
  Actions or GitLab CI attaches provenance by default. Classic tokens were revoked
  on 2025-12-09; granular tokens with write permission last at most 90 days.
- **PyPI**: Trusted Publishing exchanges the CI's OIDC token for an API token valid
  for 15 minutes. `pypa/gh-action-pypi-publish` generates and uploads digital
  attestations by default when using Trusted Publishing.

## 5. GitHub Actions

- **Enforced SHA pinning**: since 2025-08-15, an allowed actions policy checkbox
  enforces SHA pinning at the enterprise, organization, or repository level; a
  workflow using an unpinned action fails. In the same policy, entries prefixed
  with `!` block specific actions or versions.
- **Automated pinning**: do not pin by hand; for example, Renovate's
  `helpers:pinGitHubActionDigests` (included in `config:best-practices`).
- **Workflow lockfile**: `.github/workflows/actions.lock` records actions, their
  transitive dependencies, and reusable-workflow commits (created with the
  `gh actions-lock` extension). Public preview since 2026-10-14; optional. A lock
  does not judge whether a dependency is safe, so review contents before locking.
- **`pull_request_target` / `workflow_run`**: privileged triggers that get the base
  repository's secrets, write permissions, and the same cache as the main branch.
  Checking out a fork PR hands those to the fork. Avoid them; if used, never check
  out the fork head and pass no secrets or write permissions.
- **Execution protections** (GA 2026-09-17): allowlists for who (actor rules) and
  which events (event rules) may start workflows, scoped per workflow file, with an
  evaluate mode to preview impact. Manageable through the REST API at enterprise,
  organization, and repository level.
  - GitHub added a default rule disabling `pull_request_target`, but it applies only
    to **public repositories** without an event policy. It does not cover private or
    internal repositories, common in client work; configure event rules there.
  - Automatic enforcement on public repositories is scheduled for 2026-12-02 (date
    updated 2026-10-21).
- **Pass untrusted values through env**: do not embed values such as
  `${{ github.event.pull_request.title }}` directly in `run:`; assign them to an
  intermediate environment variable first. An inline expression becomes part of the
  shell script, which is script injection.
- **Static checks**: lint workflows with actionlint or zizmor. Start new checks in
  warning mode, confirm false positives, then make them required.
- **Immutable Releases** (GA 2025-10-28): when enabled, assets and Git tags of a
  published release cannot be changed or deleted, and releases get attestations.
  Consider it for projects that distribute binaries through GitHub Releases (Tauri
  and similar).

## Sources (checked 2026-10-26)

- Dependabot default cooldown: https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/
- pnpm 11.0.0: https://github.com/pnpm/pnpm/releases/tag/v11.0.0 / pnpm 10.0.0: https://github.com/pnpm/pnpm/releases/tag/v10.0.0 / docs: https://pnpm.io/supply-chain-security
- npm 12.0.0: https://github.com/npm/cli/releases/tag/v12.0.0 / npm 11.10.0 (`min-release-age`): https://github.com/npm/cli/releases/tag/v11.10.0 / npm 11.17.0 (`min-release-age-exclude`): https://github.com/npm/cli/releases/tag/v11.17.0
- npm config (11 / 12): https://docs.npmjs.com/cli/v11/using-npm/config / https://docs.npmjs.com/cli/v12/using-npm/config
- npm versions bundled with Node: https://nodejs.org/dist/index.json
- Renovate: https://docs.renovatebot.com/configuration-options/#minimumreleaseage / https://docs.renovatebot.com/presets-config/#configbest-practices
- uv: https://docs.astral.sh/uv/reference/settings/#exclude-newer
- pip: https://pip.pypa.io/en/stable/news/
- npm Trusted Publishing: https://docs.npmjs.com/trusted-publishers / classic token revocation: https://github.blog/changelog/2025-12-09-npm-classic-tokens-revoked-session-based-auth-and-cli-token-management-now-available/
- PyPI Trusted Publishing: https://docs.pypi.org/trusted-publishers/ / attestation default: https://github.com/pypa/gh-action-pypi-publish
- Enforced SHA pinning: https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/
- Workflow lockfiles: https://github.blog/changelog/2026-10-14-github-actions-workflow-lockfiles-in-public-preview/
- Execution protections: https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available/
- Untrusted values and `pull_request_target`: https://docs.github.com/en/actions/reference/security/secure-use
- Immutable Releases: https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/
