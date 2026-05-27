# Công dụng và cách sử dụng ai-system

## 1. ai-system dùng để làm gì?

`ai-system` là một MVP cho hệ thống điều phối delivery phần mềm bằng AI theo kiểu Codex/Devin workflow.

Mục tiêu của hệ thống:

- Quản lý nhiều dự án phần mềm riêng biệt.
- Chuyển yêu cầu ban đầu thành tài liệu BRD, SRD, FRD.
- Lập kiến trúc giải pháp trước khi triển khai code.
- Chia việc cho nhiều vai trò agent: PO, architect, BA, tech lead, QC, design, worker, reviewer.
- Tách quy trình delivery thành các workflow có approval gate.
- Lưu state, log, approval, task, tài liệu riêng cho từng dự án.
- Chạy được không cần AI API thật nhờ mock provider.
- Sẵn sàng mở rộng sang OpenAI, Codex hoặc local LLM.

Hệ thống hiện tại không chỉ là bộ prompt template. Nó có CLI, runtime, project registry, workflow runner, approval gate, provider abstraction và project isolation.

## 2. Hệ thống hiện hỗ trợ những gì?

### Multi-project

Mỗi dự án được quản lý riêng trong:

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

Registry toàn cục nằm tại:

```text
~/.ai-system/projects.json
```

### Multi-agent workflow

Hệ thống có các nhóm agent:

- Executive: `po-lead`, `solution-architect`, `delivery-orchestrator`
- Leads: `ba-lead`, `tech-lead`, `qc-lead`, `design-lead`
- Workers: `backend-worker`, `frontend-worker`, `tester-worker`, `reviewer-worker`, `devops-worker`

### Workflow delivery

Các workflow chính:

- `01-intake-to-docs`: từ requirement sang BRD/SRD/FRD
- `02-solution-architecture`: tạo solution architecture
- `03-parallel-lead-planning`: BA/Tech/QC/Design lập kế hoạch song song
- `04-task-breakdown`: chia thành task có thể thực thi
- `05-task-execution`: worker execution
- `06-code-test-review-commit`: test, review, commit gate

### Approval gates

Các gate quan trọng:

- `requirements`
- `architecture`
- `task-plan`
- `review`

Task execution bị chặn nếu chưa approve `task-plan`.
Commit task bị chặn nếu chưa có review khi project bật `review_required`.

## 3. Cách sử dụng nhanh

Chuyển vào repo `ai-system`:

```bash
cd /path/to/ai-system
```

### Đăng ký project

Ví dụ đăng ký một project web giả định:

```bash
python3 -m cli register-project --name DemoShop --path /example/projects/demo-shop --type web
```

Ví dụ đăng ký một project backend giả định:

```bash
python3 -m cli register-project --name BillingService --path /example/projects/billing-service --type backend
```

### Chọn project đang làm

```bash
python3 -m cli use-project DemoShop
```

### Xem danh sách project

```bash
python3 -m cli list-projects
```

### Xem trạng thái project

```bash
python3 -m cli project-status
```

## 4. Quy trình xử lý một feature

### Bước 1: Tạo file requirement

Ví dụ tạo file `req.md` trong project hoặc trong thư mục hiện tại:

```md
# Requirement

Cần tạo chức năng Product Bundle Mapping.

Người dùng có thể gom nhiều sản phẩm vào một bundle.
Hệ thống cần hiển thị bundle trong trang quản trị và dùng dữ liệu này cho storefront.
```

### Bước 2: Chạy intake

```bash
python3 -m cli intake --file req.md
```

Lệnh này tạo run log và document draft trong `.ai-system/runs/` và `.ai-system/docs/`.

### Bước 3: Approve requirements

```bash
python3 -m cli approve --gate requirements
```

### Bước 4: Tạo solution architecture

```bash
python3 -m cli run-workflow 02-solution-architecture
```

### Bước 5: Approve architecture

```bash
python3 -m cli approve --gate architecture
```

### Bước 6: Chia task

```bash
python3 -m cli run-workflow 04-task-breakdown
```

### Bước 7: Approve task plan

```bash
python3 -m cli approve --gate task-plan
```

### Bước 8: Chạy task

```bash
python3 -m cli run-task TASK-001
```

### Bước 9: Review task

```bash
python3 -m cli review-task TASK-001
```

### Bước 10: Approve review và ghi nhận commit intent

```bash
python3 -m cli approve --gate review
python3 -m cli commit-task TASK-001
```

## 5. Dry-run

Dùng dry-run để kiểm tra workflow mà không ghi artifact sinh ra:

```bash
python3 -m cli --dry-run run-workflow 01-intake-to-docs
python3 -m cli --dry-run run-task TASK-001
```

## 6. Cấu hình project

Mỗi project có file:

```text
.ai-system/project.yaml
```

Các field quan trọng:

```yaml
project_name: DemoShop
project_type: web
repo_path: /example/projects/demo-shop
default_branch: main
working_branch_prefix: ai/
tech_stack:
  - python
  - typescript
coding_rules:
  - Keep changes small and reviewable.
test_command: "npm test"
build_command: "npm run build"
deploy_command: ""
document_path: .ai-system/docs
review_required: true
human_approval_required: true
```

Nếu muốn task execution tự động chạy test, cấu hình:

```yaml
test_command: "npm test"
```

Hoặc với project Python:

```yaml
test_command: "pytest"
```

## 7. Kiểm tra hệ thống

Validate YAML/JSON:

```bash
python3 tools/validate-ai-system.py
```

Kiểm tra Python syntax:

```bash
python3 -m compileall cli runtime providers tools
```

## 8. Giới hạn hiện tại của MVP

Hiện tại hệ thống:

- Chưa gọi OpenAI API thật.
- Chưa tự sinh code thông minh bằng LLM.
- Chưa implement Git commit thật trong `commit-task`.
- Chưa enforce allowed files đầy đủ theo task schema.
- Chưa có UI approval.

Nhưng nền tảng đã sẵn sàng:

- CLI
- Project registry
- Project isolation
- Runtime state
- Workflow runner
- Approval gates
- Document templates
- Provider abstraction
- Mock provider
- Safety flow cơ bản

## 9. Hướng phát triển tiếp theo

Nên làm tiếp theo theo thứ tự:

1. Thêm provider OpenAI thật.
2. Thêm Codex provider để giao task code execution.
3. Thêm renderer sinh document từ template và context thật.
4. Thêm task planner tạo task JSON/Markdown có allowed files.
5. Thêm enforcement chỉ sửa file nằm trong allowed files.
6. Thêm Git commit implementation sau khi review pass.
7. Thêm UI/chat approval cho human-in-the-loop.
