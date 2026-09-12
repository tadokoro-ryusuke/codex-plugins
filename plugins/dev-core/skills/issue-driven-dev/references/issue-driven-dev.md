# Issue templates and examples

Reuse the existing issue shape and accepted scope. Adapt these examples to the task; creating or posting issues requires the appropriate existing authorization.

## Issue Form examples

Adapt these examples only when Issue Forms are part of the requested workflow. Required form fields improve intake structure; they do not prove the semantics or approval of acceptance criteria, and alternate API or authorized task paths may bypass the form.

### Bug report — `bug_report.yml`

```yaml
name: Bug report
description: Report behavior that differs from what is expected
title: "[Bug]: "
labels: ["type/bug", "status/needs-triage"]
body:
  - type: textarea
    id: summary
    attributes:
      label: What is happening (current behavior)
      description: Observed facts only. Put speculation under "Technical notes"
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Numbered steps. Include the reproduction rate (always / sometimes / specific conditions)
      placeholder: |
        1. ...
        2. ...
        3. ...
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS / browser / app version / environment (production, staging, local)
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Error logs / screenshots
      description: Relevant redacted error messages and stack traces; exclude secrets and personal data
  - type: textarea
    id: notes
    attributes:
      label: Technical notes (optional)
      description: Suspected cause, files likely involved, recent related changes
```

### Feature request — `feature_request.yml`

```yaml
name: Feature request
description: Propose a new feature or improvement
title: "[Feature]: "
labels: ["type/feature", "status/needs-triage"]
body:
  - type: textarea
    id: background
    attributes:
      label: Background / why it is needed
      description: The problem this feature solves. Who is hurting (business context)
    validations:
      required: true
  - type: textarea
    id: story
    attributes:
      label: User story
      placeholder: "As a ..., I want to ..., because ..."
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance criteria
      description: Verifiable conditions as checkboxes. These become the completion conditions and the test spec verbatim
      placeholder: |
        - [ ] Condition 1
        - [ ] Condition 2
    validations:
      required: true
  - type: textarea
    id: out_of_scope
    attributes:
      label: Out of scope
      description: State explicitly what this issue will NOT do
    validations:
      required: true
  - type: textarea
    id: notes
    attributes:
      label: Technical notes (optional)
```

### Task — `task.yml`

```yaml
name: Task
description: A unit of work such as refactoring, configuration change, or investigation
title: "[Task]: "
labels: ["type/chore", "status/needs-triage"]
body:
  - type: textarea
    id: background
    attributes:
      label: Background / why
    validations:
      required: true
  - type: textarea
    id: work
    attributes:
      label: Work description
      description: What to do and how. Scale detail to the work; one clear line can suffice for a trivial task
    validations:
      required: true
  - type: textarea
    id: acceptance
    attributes:
      label: Completion conditions
      description: State observable completion conditions for the work
      placeholder: |
        - [ ] Condition 1
```

Set `blank_issues_enabled: false` only if the project intentionally disables that UI intake path. Do not claim it prevents every API or alternate path from creating an issue.


## Concrete issue examples

### Passing example

> **Title**: Allow resending the password reset email
>
> **Background / why**: Reset emails frequently land in spam, and users churn while locked out. One of the top support-ticket categories.
>
> **Current vs expected**: Currently no resend is possible for 60 minutes after a reset request. Expected: the resend button becomes enabled after a 60-second cooldown.
>
> **Acceptance criteria**:
> - [ ] The "Resend" button becomes enabled 60 seconds after a reset request
> - [ ] Resending invalidates the previous token and issues a new one
> - [ ] Resend requests within 60 seconds return 429, and the UI shows the remaining cooldown seconds
> - [ ] Automated tests cover the three points above
>
> **Out of scope**: Email template redesign; SMS-based reset.
>
> **Technical notes**: The existing RateLimiter middleware can likely be reused for rate limiting.

Why it passes: an implementer (human or AI) can start from this alone, the acceptance criteria are the test spec verbatim, and the explicit out-of-scope section keeps the implementation from ballooning.

### Failing example, and how to fix it

> **Title**: Make the login stuff nicer

Why it fails, and the fix:

- "Nicer" is unverifiable → rewrite as observable current behavior and expected behavior.
- The concern is unclear (UI? security? performance?) → split into 1 issue = 1 concern.
- No acceptance criteria → if delegated to an agent, the agent ends up deciding its own completion conditions, and a human can no longer judge pass/fail on the result.

For a self-evident task such as correcting `recieve` to `receive`, a title and one clear completion condition are enough. Do not create a full form or external issue when only a local edit was requested.
