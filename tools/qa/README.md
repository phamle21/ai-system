# Tools — Sinh QA workbook (.xlsx)

Tool QA tái dùng cho mọi dự án (đúc kết từ `faeger-ug-sdd/04.qa`). Dùng cùng skill
[`skills/testing/qa-test-cases.yaml`](../../skills/testing/qa-test-cases.yaml): AI sinh JSON → script dựng workbook.

Sinh **1 file `.xlsx` chuẩn cho mỗi module**, gồm **5 sheet trong cùng 1 file**:
`00 Tổng quan · PCL · Test_Cases · Test_Run · Bugs`.

- **Test_Cases** = master (sinh từ JSON, **không sửa tay**).
- **Test_Run** = append-only — mỗi lần chạy thêm **1 dòng** (`Tester · Build · Kết quả`) → nhiều người test / nhiều vòng vẫn đủ chỗ, giữ lịch sử.
- **PCL** = auto-derive theo `area` (hoặc cung cấp `pcl` thủ công nếu cần checklist chi tiết).
- **Bugs** = dự phòng nếu không dùng issue tracker (khuyến nghị log bug ở GitBucket/Redmine, link Bug ID).

## Cách dùng

1. AI sinh **JSON** (gõ `export xlsx` sau khi `generate test cases`).
2. Dựng file (chạy từ thư mục gốc `ai-system/`):
   ```bash
   pip install openpyxl        # một lần
   python tools/qa/build_workbook.py <input.json>
   # hoặc: python tools/qa/build_workbook.py <input.json> <output.xlsx>
   ```
3. Import file `.xlsx` vào **Google Sheets** (`File → Import → Upload`) — mỗi module **1 Sheet sống**, không phát tán nhiều bản copy. Nhiều tester cùng điền `Test_Run`.

> Trong **Claude Code**, AI chạy luôn `python build_workbook.py …`. Sandbox không có openpyxl thì dùng renderer stdlib tương đương (cùng `prepare()`), output y hệt.

## Schema JSON (đầu vào)

```json
{
  "title": "PWA — Login / Auth (M0-1)",
  "filename": "【PWA】【QA】M0-1_Login_Auth.xlsx",
  "app": "PWA",
  "module": "Login",
  "source": "M0-1 Sign In",
  "test_cases": [
    {
      "id": "PWA-LOGIN-TC-001",
      "area": "Đăng nhập (Online)",
      "feature": "Đăng nhập thành công",
      "precond": "App online; tài khoản Monitor active",
      "data": "login_id=MON-2417; password=Password1234",
      "steps": ["1. …", "2. …"],
      "expected": ["- …", "- …"],
      "type": "Functional",
      "priority": "High",
      "notes": "[AUTH] Use Case"
    }
  ]
}
```

| Field | Bắt buộc | Ghi chú |
|---|---|---|
| `title`, `app`, `module`, `source` | ✓ | Hiển thị ở `00 Tổng quan`; `app`+`module` sinh PCL ID `{APP}-{MODULE}-PCL-NN`. |
| `filename` | – | Tên file ra (đặt theo tag `【APP】【QA】{ScreenID}_{Feature}.xlsx`). |
| `test_cases[].area` | ✓ | Nhóm trong module (vd `Đăng nhập (Online)`); là cơ sở auto-derive PCL. |
| `test_cases[].steps` / `expected` | ✓ | Mảng (mỗi phần tử 1 dòng) hoặc chuỗi. |
| `test_cases[]`: `id, feature, precond, data, type, priority, notes` | ✓ | Chuỗi. `[ASSUMPTION]`/`[Pending]` đặt trong `feature`/`notes`. |
| `pcl` | – | Cung cấp để override PCL auto (mảng `{pcl_id, area, check_point, source, type, priority, covered_by, notes}`). |

> JSON ví dụ ở trên lấy từ dự án tham chiếu (Faeger PWA) chỉ để minh hoạ format —
> thay `app`/`module`/`area`/data bằng domain dự án của bạn.

## Cột mỗi sheet
Xem [`templates/columns.md`](templates/columns.md). Layout/màu do script cố định để output luôn nhất quán — AI chỉ điền dữ liệu JSON.
