# AI Delivery Operating System

`ai-system` is a runnable MVP for a multi-project AI software delivery operating system. It is designed for Codex/Devin-style workflows where requirements become documents, architecture, parallel lead plans, executable tasks, reviews, and commit-ready delivery logs.

The MVP runs without real AI APIs. It uses deterministic mock providers, YAML agent specs, YAML workflows, Markdown document templates, JSON runtime state, and approval gates.

## Architecture

```text
ai-system/
├── agents/
│   ├── executive/
│   ├── leads/
│   └── workers/
├── workflows/
├── documents/
│   ├── templates/
│   └── schemas/
├── runtime/
│   ├── approvals/
│   ├── runs/
│   ├── memory/
│   └── schemas/
├── providers/
│   ├── base/
│   ├── mock/
│   ├── openai/
│   ├── codex/
│   └── local/
├── cli/
├── projects/
├── tools/
├── skills/
└── rules/
```

## Delivery Flow

```text
Requirement
→ PO Analysis
→ BRD / SRD / FRD
→ Solution Architecture
→ BA / Tech / QC / Design planning
→ Task Breakdown
→ Worker Execution
→ Code / Test / Review / Commit
```

## Agents

Executive agents:

- `po-lead`
- `solution-architect`
- `delivery-orchestrator`

Lead agents:

- `ba-lead`
- `tech-lead`
- `qc-lead`
- `design-lead`

Worker agents:

- `backend-worker`
- `frontend-worker`
- `tester-worker`
- `reviewer-worker`
- `devops-worker`

Each agent is declared in YAML with role, goal, inputs, outputs, quality gates, rules, handoff targets, allowed tools, approval requirements, and execution policy.

## Workflows

- `01-intake-to-docs`
- `02-solution-architecture`
- `03-parallel-lead-planning`
- `04-task-breakdown`
- `05-task-execution`
- `06-code-test-review-commit`

Workflow files define ordered steps with agent assignment, input, output, approval gate, retry policy, next step, and failure behavior.

## Multi-Project Support

Each managed project gets isolated runtime data:

```text
.ai-system/
├── project.yaml
├── state.json
├── approvals/
├── runs/
├── memory/
├── tasks/
└── docs/
```

The global registry lives at:

```text
~/.ai-system/projects.json
```

Set `AI_SYSTEM_REGISTRY=/path/to/projects.json` for tests or isolated environments.

## CLI Usage

Run from this repository:

```bash
python3 -m cli init-project --name DemoShop --path /example/projects/demo-shop --type web
python3 -m cli register-project --name DemoShop --path /example/projects/demo-shop --type web
python3 -m cli use-project DemoShop
python3 -m cli list-projects
python3 -m cli project-status
```

Run delivery workflows:

```bash
python3 -m cli intake --file req.md
python3 -m cli run-workflow 02-solution-architecture
python3 -m cli approve --gate requirements
python3 -m cli approve --gate architecture
python3 -m cli approve --gate task-plan
python3 -m cli run-task TASK-001
python3 -m cli review-task TASK-001
python3 -m cli approve --gate review
python3 -m cli commit-task TASK-001
```

Use dry-run mode:

```bash
python3 -m cli --dry-run run-workflow 01-intake-to-docs
python3 -m cli --dry-run run-task TASK-001
```

## Runtime Safety

The MVP enforces these delivery controls:

- Task execution is blocked until `task-plan` approval exists.
- Workflow steps with approval gates stop when the gate is not approved.
- Task execution creates or checks an AI working branch when the target project is a Git repo.
- Configured tests run before task execution is marked complete.
- Diff summaries and execution logs are persisted.
- Review is required before commit intent is recorded when `review_required` is enabled.

## Provider Layer

Providers are isolated behind a clean interface:

- `providers/base` defines `Provider`, `ProviderRequest`, and `ProviderResponse`.
- `providers/mock` is the deterministic MVP provider.
- `providers/openai`, `providers/codex`, and `providers/local` are placeholders for future integrations.

No workflow hardcodes a real provider.

## Documents

Markdown templates exist for:

- BRD
- SRD
- FRD
- Solution Architecture
- Technical Design
- Database Design
- API Design
- Test Plan
- Test Cases
- Task Breakdown
- Review Report
- Deployment Plan
- Decision Log
- Assumptions Log

## Validation

Validate YAML structure and internal references:

```bash
python3 tools/validate-ai-system.py
python3 -m compileall cli runtime providers
```

## Roadmap

- Add package entrypoint for the `ai-system` command.
- Add JSON Schema validation in the CLI runtime.
- Add richer document rendering from templates and workflow context.
- Add OpenAI provider implementation.
- Add Codex provider execution bridge.
- Add local LLM provider adapters.
- Add task allowed-file enforcement from task schema.
- Add Git commit implementation with signed review metadata.
- Add human approval UI or chat integration.
