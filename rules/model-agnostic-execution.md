# Model-Agnostic Execution Protocol

## Goal

Make every task executable by following explicit gates, checklists, and project context instead of relying on model intuition.

## Required Behavior

1. Start with intake.
2. Classify the request.
3. Check whether required inputs are present.
4. If required inputs are missing, ask only the missing questions.
5. Repeat intake until all required inputs are known or discoverable from the project.
6. Select a pipeline and skill only after the minimum inputs are satisfied.
7. Execute the checklist exactly.
8. Validate the result.
9. Summarize files changed, checks run, and unresolved risks.

## Clarification Rules

- Ask before guessing business logic, data model, permissions, or public/private API behavior.
- Ask at most 3 questions at a time.
- Each question must be answerable by a non-technical user.
- Prefer discovering answers from project files before asking.
- Do not ask if a safe project convention already answers the question.
- Do not implement while required inputs are unknown.

## Minimum Input Contract

Every executable task needs:

- project: where the change belongs
- intent: create | change | fix | review | debug
- target: feature, module, page, endpoint, data type, or file
- expected_behavior: what should happen after the change
- constraints: permissions, visibility, compatibility, or business rules

## Missing Input Response Format

Use this format when blocked:

```text
Need more information before implementation:
1. [question]
2. [question]
3. [question]
```

## Execution Response Format

Use this internal structure for complex tasks:

```text
Understanding
Required Inputs
Selected Workflow
Implementation Checklist
Validation
Risks
```

## Non-Expert User Rule

When a user describes a goal in plain language, translate it into technical inputs internally. Do not require the user to know class names, hook names, file paths, or framework internals unless the project cannot be inspected.
