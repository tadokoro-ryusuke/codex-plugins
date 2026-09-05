# Task: Support line quantities

- Status: approved
- Acceptance criteria: pending

## Goal

Update `total_cents(lines)` to multiply each unit price by its optional quantity.

## Acceptance criteria

- Treat a missing `quantity` as `1`.
- Accept only positive integer quantities; reject booleans, zero, negative values,
  floats, strings, and other values with `ValueError`.
- Preserve empty input, default-quantity behavior, and support for iterable input
  such as generators.
- Keep unit-price validation out of scope.
- Add focused tests and record the commands and observed results in this plan.
