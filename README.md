# AI SYSTEM ARCHITECTURE - MULTI PROJECT

## 1. Mục tiêu hệ thống

Xây dựng một hệ thống AI có khả năng:

* Tái sử dụng cho nhiều dự án (multi-project)
* Hỗ trợ nhiều stack (WordPress, Laravel, frontend)
* Giảm context usage bằng cách load đúng file cần thiết
* Chuẩn hóa cách AI phân tích -> lập kế hoạch -> thực thi
* Dễ mở rộng (scale skill + project + workflow)

---

## 2. Nguyên tắc thiết kế cốt lõi

### 2.1 Separation of Concerns

* Skill: biết làm gì
* Agent: điều phối
* Project: context riêng
* Pipeline: flow thực thi

Không trộn các layer.

---

### 2.2 Reusability First

* Skill phải generic
* Không hardcode project logic

---

### 2.3 Context Injection

* AI không “tự biết project”
* Luôn inject context trước khi chạy

---

### 2.4 Context Optimization

* Không load toàn bộ system
* Chỉ load:

  * skill cần thiết
  * context rút gọn
  * pipeline liên quan

---

## 3. Cấu trúc thư mục hiện tại

```
ai-system/
├── skills/
│   ├── core/
│   │   ├── analyze.yaml
│   │   ├── breakdown.yaml
│   │   ├── plan.yaml
│   │   ├── execute.yaml
│   │   ├── debug.yaml
│   │   └── summarize.yaml
│   ├── wordpress/
│   ├── laravel/
│   ├── frontend/
│   └── testing/
├── agents/
│   └── router.yaml
├── pipelines/
│   ├── build-feature.yaml
│   ├── debug.yaml
│   ├── review.yaml
│   └── simple-fix.yaml
├── templates/
│   ├── wordpress/
│   └── shared/
├── projects/
│   └── jrr/
├── rules/
│   ├── ai-engineer-protocol.md
│   ├── engineering-workflow.md
│   └── wordpress-coding-standards.md
├── tools/
│   ├── validate-ai-system.py
│   └── validate-ai-system.sh
└── README.md
```

---

## 4. Định nghĩa chuẩn cho Skill

### Format YAML

```yaml
name: skill-name
description: What this skill does

input:
  - field_1
  - field_2

steps:
  - step_1
  - step_2

rules:
  - must follow X
  - must avoid Y

output:
  type: code | text | analysis
```

---

### Nguyên tắc viết skill

* 1 skill = 1 nhiệm vụ rõ ràng
* Không dài quá 150–300 dòng
* Không chứa context project; project-specific logic belongs in `projects/[project]/`
* Có rule rõ ràng (rất quan trọng)

---

## 5. Agents (Orchestrator)

### 5.1 Router hiện có

`agents/router.yaml` chọn pipeline và skill theo task, stack, và project overlay.

```yaml
when:
  - task: create plugin
    use: wordpress/plugin/create
```

---

## 6. Pipeline (Workflow)

Pipelines hiện có:

* `simple-fix`: analyze -> execute -> validate -> summarize
* `build-feature`: analyze -> breakdown -> plan -> execute -> validate -> summarize
* `debug`: analyze -> reproduce -> isolate -> execute -> validate -> summarize
* `review`: analyze -> inspect -> findings -> summarize

Ví dụ `build-feature`:

```yaml
name: build-feature

steps:
  - analyze
  - breakdown
  - plan
  - execute
  - validate
  - summarize
```

---

## 7. Project Context (đặt trong repo project)

```
my-project/
├── .ai/
│   ├── context.yaml
│   ├── architecture.md
│   ├── modules.yaml
│   └── rules.md
```

---

### context.yaml

```yaml
name: ecommerce-system

stack:
  - laravel
  - mysql
  - redis

modules:
  - auth
  - product
  - order

rules:
  api: rest
  auth: jwt
```

---

## 8. Cách hệ thống hoạt động

```
User Input
   ↓
Analyzer
   ↓
Router
   ↓
Load Project Context
   ↓
Planner
   ↓
Executor (call skill)
   ↓
Reviewer
   ↓
Output
```

---

## 9. Token Optimization Strategy (CỰC QUAN TRỌNG)

### 9.1 Không load toàn bộ system

Chỉ load:

* 1–2 skill liên quan
* context rút gọn
* pipeline hiện tại

---

### 9.2 Context Compression

Thay vì:

```yaml
modules:
  - auth
  - product
  - order
  - payment
  - shipping
```

→ rút gọn:

```yaml
modules: [auth, product, order]
```

---

### 9.3 Skill Granularity

❌ Sai:

* 1 skill làm tất cả

✅ Đúng:

* chia nhỏ skill

---

### 9.4 Template-driven

* hạn chế generate từ đầu
* dùng template để giảm token

---

## 10. Git Ignore (QUAN TRỌNG)

### Nên ignore:

```
# cache
.cache/
.tmp/

# logs
logs/
*.log

# runtime
dist/
build/

# local config
.env
.env.local

# AI generated temp
.generated/
.ai-cache/
.ai-output/

# OS
.DS_Store
Thumbs.db
```

---

### Không nên ignore:

* skills/
* agents/
* pipelines/
* templates/
* rules/

👉 vì đây là “core knowledge”

---

## 11. Versioning Strategy

* version skill riêng
* không phụ thuộc project

Ví dụ:

```
skills/wp-plugin/create@v1.yaml
skills/wp-plugin/create@v2.yaml
```

---

## 12. Mở rộng trong tương lai

Bạn có thể thêm:

### 12.1 AI Memory Layer

* lưu history
* reuse decision

---

### 12.2 Auto Learning

* log task → refine skill

---

### 12.3 CI/CD Integration

* auto validate code
* auto deploy

---

### 12.4 Multi-agent parallel

* chạy nhiều agent cùng lúc

---

## 13. Checklist hoàn chỉnh

* [ ] Skill tách biệt
* [ ] Có router
* [ ] Có pipeline
* [ ] Có context project
* [ ] Có validation
* [ ] Có template
* [ ] Có token optimization

---

## 14. Kết luận

Hệ thống này giúp bạn:

* Tái sử dụng AI cho mọi project
* Giảm prompt thủ công
* Tăng consistency code
* Scale team/dev dễ dàng

---

## 15. Công thức tổng

```
Skill + Context + Agent + Pipeline = AI Dev System
```

---
