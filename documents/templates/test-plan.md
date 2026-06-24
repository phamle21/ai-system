# Test Plan

> Functional QA by default. Non-functional (performance, security, usability) is
> out of scope unless explicitly requested.

## Scope
- In scope: [features / modules / surfaces under test]
- Out of scope: [explicitly excluded]

## Test Levels
- Manual QA (UI-executable test cases) — see Test Cases doc / 5-sheet workbook.
- Automated: [unit / integration / e2e, if any]

## Coverage Strategy
- Types: Functional / Negative / Boundary / Integration / Regression (+ project extras).
- Actor × Surface matrix (data lineage): cover every surface that READS or is affected
  by the changed data, not only the surface whose code changed.
- Techniques applied: [EP / BVA / Decision Table / State Transition / Use Case / Error Guessing]

## Test Environment
- [env, build/version, accounts, devices/browsers]

## Test Data
- [concrete in-domain values, accounts, fixtures]

## Commands
- [build / lint / automated-test commands]

## Entry Criteria
- [feature doc available, build deployed, accounts ready]

## Exit Criteria
- [all Critical/High cases Pass, no open blocker bugs, [Pending] items resolved]

## Open Items
- `[Pending]`: [business decisions needed]
- `[ASSUMPTION]`: [QA-baseline assumptions made, with reasons]
