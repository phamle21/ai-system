# Giải thích cột — QA workbook (5 sheet / module)

1 module = **1 Google Sheet sống** với 5 tab: `00 Tổng quan · PCL · Test_Cases · Test_Run · Bugs`.
File `.xlsx` sinh từ [`../build_workbook.py`](../build_workbook.py) đã có đủ 5 sheet; các
CSV ở đây chỉ là tham chiếu cột / để dựng tab thủ công.

## Test_Cases — master (sinh từ JSON, KHÔNG sửa tay)
`No. · TC ID · PCL ID · Nhóm · Chức năng · Tiền điều kiện · Dữ liệu test · Các bước · Kết quả mong đợi · Loại · Ưu tiên · Nguồn · Ghi chú`
- `PCL ID` trace lên sheet PCL; `Nhóm` = area (Online/Offline/…); `Loại` ∈ Functional/Negative/Boundary/Integration/Regression/Online/Offline/Permission/Sync-LWW.
- Nội dung tiếng Việt có dấu; giữ nguyên UI/field/status/endpoint/ID. Expected **phải có khả năng FAIL**.

## PCL — checklist (auto-derive theo `Nhóm`, hoặc tự viết)
`PCL ID · Khu vực · Check Point · Nguồn · Loại · Ưu tiên · Covered By · Ghi chú`
- `Covered By` = các TC ID phủ check point này → đo coverage.

## Test_Run — nhật ký chạy (APPEND-ONLY, nhiều tester / nhiều vòng)
`Run ID · TC ID · Cycle/Build · Môi trường · Tester · Ngày · Kết quả · Actual Result · Bug ID · Ghi chú`
- Mỗi lần chạy 1 TC = **1 dòng mới** (không đè). 5 người test 3 vòng = 5×3 dòng. `Kết quả` ∈ Pass/Fail/Blocked/Skip/Not Run.

## Bugs — dự phòng (khuyến nghị dùng issue tracker thay thế)
`Bug ID · TC ID · Tiêu đề · Mức độ · Ưu tiên · Trạng thái · Bước tái hiện · Mong đợi · Thực tế · Môi trường · Người báo · Phụ trách · Ghi chú`
- `Trạng thái`: Open → In Progress → Fixed → Verified → Closed / Won't fix. Dùng GitBucket/Redmine thì log ở đó, ghi link/issue vào `Bug ID`.
