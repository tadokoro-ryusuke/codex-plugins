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
and replacement coverage for critical paths; see `$test-design` if needed.

Consolidate verification commands using the stack's existing scripts or task
runner so local and CI behavior can be reproduced. Validate workflow behavior and
failure paths, not just YAML syntax. Report which checks ran locally and which
remote enforcement remains unverified.

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

Keep dependency updates maintainable. Add artifact provenance, SBOM, or other
supply-chain controls when the delivery requirements justify them. Recheck current
official provider guidance for implementation syntax and platform behavior.

Do not claim a passing pipeline establishes device behavior, production health,
or client acceptance. Retain the exact revision, command/job, result, and relevant
environment needed to assess what the evidence proves.
