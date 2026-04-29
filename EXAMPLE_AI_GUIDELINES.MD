# Project AI Guidelines (AGENTS.md)

## System Behavior (Always Follow)

### AI Engineer Protocol
- **No filler**: No conversational phrases. Output only what matters.
- **High signal**: Every sentence must provide value.
- **Correctness > Speed**: Do not rush into wrong solutions.
- **Surgical changes**: Modify ONLY what is necessary.
- **Respect codebase**: Follow existing patterns strictly.

### Thinking Protocol (Mandatory)
Before answering, ALWAYS:
1. **Understand**: Restate the problem internally. Detect ambiguity.
2. **Classify**: Simple → direct solve. Complex → require plan first.
3. **Consistency check**: Does solution match requirement? Any edge cases?

### Anti-Failure Guards
- **No Assumption Rule**: Never invent data structures, business logic, or API behavior. If missing → ask or state assumption clearly.
- **Anti-Drift**: If unsure, STOP and re-evaluate. Do NOT continue blindly.
- **Minimal Solution**: Prefer simplest working solution. No unnecessary abstractions.
- **Backward Compatibility**: Consider legacy data. Provide fallback if needed.

### Code Execution Rules
- Do NOT write code immediately if problem is unclear.
- Do NOT refactor unrelated code.
- Do NOT rename variables/functions without reason.
- Follow project conventions strictly.

### Output Format
- **Simple tasks**: Direct answer or code.
- **Complex tasks**: Understanding → Key Issues → Solution → Risks → Implementation.

---

## AI System Architecture

This project uses a centralized **ai-system/** for reusable skills, rules, and pipelines. The ai-system is shared across multiple projects and contains:
- `skills/` — reusable workflow skills (core, wordpress, laravel, frontend)
- `rules/` — behavioral protocols and coding standards
- `agents/` — routing and orchestration
- `pipelines/` — workflow definitions
- `templates/` — project bootstrap and conventions

### Auto-Load Protocol (MANDATORY)

When working on jrr/, ALWAYS load context in this order:

1. **jrr/.ai/context.yaml** — Project stack, modules, CPTs, tech details
2. **jrr/.ai/architecture.md** — System architecture (jrr-core, shortcodes, Elementor, Nuxt)
3. **jrr/.ai/rules.md** — JRR coding standards + spec & task management rules
4. **jrr/.ai/notes.md** — Patterns, gotchas, common issues, troubleshooting

Then load global rules from ai-system/:
5. **ai-system/rules/ai-engineer-protocol.md** — Behavioral rules
6. **ai-system/rules/engineering-workflow.md** — Engineering workflow
7. **ai-system/rules/wordpress-coding-standards.md** — WordPress coding standards

Apply ALL loaded rules to every task. Never skip auto-load.

---

## Project Conventions: jrr/ — WordPress Plugin (PHP 8.0+, PSR-12)

### Namespace
`JRR\Core\[Module]\[SubModule]`

### Shortcodes
- Extend `BaseShortcode`
- Use `$this->render_view('index.php', $vars)` for templates
- Cache-bust assets with `filemtime()`
- Constants: `private const STYLE`, `private const SCRIPT`
- Override `register_assets()` and `render($atts, $content, $shortcode_name)`

### AJAX
Nonce check → sanitize → business logic → `wp_send_json_success`

### SCSS
- BEM naming: `.block__element.is-modifier`
- Breakpoints: `@include breakpoints.respond(tablet/laptop/desktop)`
- Max 3-4 nest levels
- Use CSS custom properties for spacing/colors

### JavaScript
- IIFE + jQuery module pattern (object literal)
- Delegated events: `$(document).on("click", ".selector", self.handler.bind(self))`
- Namespaced events: `.jrrModule` suffix
- Batch DOM: `DocumentFragment`
- Debounce input search, abort previous AJAX

### Views / Templates
- Escaping: `esc_html()`, `esc_attr()`, `esc_url()`
- Partials prefixed with `_`
- Fallback: `$data['key'] ?? 'default'`
- Short echo tags: `<?= ... ?>`
- Protect file: `if (!defined('ABSPATH')) exit;`

### Data
- Meta keys: snake_case, prefix `jrr_` for custom data
- WP_Query with `tax_query` for taxonomy filters

---

## Spec & Task Management

Rules: `jrr/.ai/rules.md` (Section 9)

Structure:
```
specs/issues/[YYYY-MM]/issue-[id]-[short-description]/
├── tasks/
│   ├── FE-01-[description].md
│   ├── BE-02-[description].md
│   └── QA-03-[description].md
└── [short-description]-overview.md
```

- Simple tasks → Option A (Simple template)
- Complex tasks → Option B (Full template)
- Always update overview before breaking down tasks
- Title: English. Description: Vietnamese or English.
- Must include Risk & Impact table in overview
- QA tasks must depend on corresponding BE+FE tasks

---

## JRR Workflow Pipeline

When implementing a feature in jrr/:

1. **Read context**: Load `jrr/.ai/` files (context, architecture, rules, notes)
2. **Parse spec**: Use `analyze-overview` skill to extract objectives/scope from overview
3. **Breakdown**: Use `breakdown-tasks` skill to generate FE/BE/QA tasks
4. **Manage specs**: Use `spec-manager` skill to create task files
5. **Execute**: Router selects appropriate skill from `ai-system/skills/wordpress/`
6. **Verify**: Apply loaded rules and conventions from `jrr/.ai/rules.md`

This workflow reduces token usage by loading only necessary skills and context, not the entire ai-system.

---

## Workflow Automation (Agent Mode)

### Trigger Pattern
When user says: "Implement issue-XXX", "Start issue-XXX", or "Fix issue-XXX"

### Execution Protocol (SINGLE SHOT — DO NOT ASK)
When trigger is detected, DO NOT PROPOSE SOLUTIONS. DO NOT ASK FOR CONFIRMATION. 
Execute immediately in this exact order:

1. **Load Context**: Read `jrr/.ai/context.yaml`, `jrr/.ai/rules.md`, `jrr/.ai/notes.md`
2. **Locate Spec**: Find file `specs/issues/[YYYY-MM]/issue-XXX/[description]-overview.md`
3. **Parse & Generate**:
   - Read the overview file
   - Extract Section 13 (Task Breakdown)
   - Create `tasks/` directory if missing
   - Create task files (`FE-01-...`, `BE-02-...`, `QA-03-...`) with full content
4. **Execute**: Start implementing `BE-01` task immediately. Apply strict `jrr/.ai/rules.md` conventions.

### Error Handling
- If overview file missing → STOP and request user to provide overview content
- If Task Breakdown is empty → STOP and request update overview
- If task files already exist → Overwrite if changes needed, keep if accurate

### Token Optimization
- Only load `jrr/.ai/` files relevant to the current issue
- Only load skills needed for the specific task type (BE/FE/QA)
- Do NOT load entire ai-system — use Router to select only relevant skills
