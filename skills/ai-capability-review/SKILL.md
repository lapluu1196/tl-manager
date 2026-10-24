---
name: ai-capability-review
description: Đánh giá năng lực sử dụng AI theo L1–L5, ghi điểm và bằng chứng vào Google Sheet, thống nhất mục tiêu phát triển cho BA Dev QA.
---

# Đánh giá năng lực sử dụng AI

Đọc [input](assets/input.md), dùng [output](assets/output.md) và giữ nguyên [khung L1–L5](assets/levels.md). Kết quả cá nhân nằm trên Sheet đã được người dùng chỉ định hoặc trong `private/ai-capability-review/<kỳ>/`, không đưa lên Git public.

1. Xác định kỳ đánh giá, danh sách người/vai trò, người chấm và Sheet/tab đích từ input hoặc `.local/google-workspace.json`. Phân biệt spreadsheet ID với `gid` (sheet ID). Đọc cấu trúc/nội dung hiện có trước khi ghi; không thay thế tab đang chứa dữ liệu.
2. Kiểm tra [Google Workspace](../../docs/google-workspace.md) đã đăng nhập và truy cập đúng tài khoản/file. Thiếu OAuth thì chuẩn bị nội dung cục bộ và báo bước còn thiếu; không tuyên bố đã tạo/cập nhật Sheet.
3. Dùng điểm nguyên 1–5 tương ứng L1–L5, giữ riêng tự đánh giá và điểm leader chốt. Level và mức độ được suy ra từ điểm leader. Không tự mặc định người chưa chấm là L1 hoặc 0; thiếu bằng chứng ghi rõ, không tự điền điểm.
4. Thu bằng chứng đúng vai trò: bài làm, prompt/workflow, cách kiểm chứng, kết quả trước/sau và mức hỗ trợ cần thiết. Không quy năng lực chỉ từ số lần dùng AI, thương hiệu công cụ hoặc biết lập trình; workflow của BA/QA có giá trị tương ứng.
5. Với L3 kiểm tra bằng chứng tích hợp thường xuyên, kiểm chứng và hiệu quả; L4 cần workflow/automation/agent cùng cải thiện và chia sẻ; L5 cần tác động, nhân rộng và định hướng tổ chức. Đối chiếu toàn bộ biểu hiện, không nâng level chỉ do biết tên kỹ thuật. Leader quyết định khi bằng chứng không đồng đều; ghi lý do và phản hồi người được đánh giá.
6. Thiết kế bảng có các tab Khung level, Đánh giá và Tổng hợp; dùng điểm dropdown 1–5, công thức để trống khi chưa chấm, cột evidence/nhận xét/mục tiêu/hạn đánh giá lại. Tổng hợp chỉ đếm người có tên và điểm hợp lệ, tách chưa chấm; không xếp hạng cá nhân tự động.
7. Khi được yêu cầu tạo/cập nhật Sheet, thực hiện đúng phạm vi đã ủy quyền, giữ dữ liệu hiện có và xác minh lại kết quả. Quyền này không bao gồm chia sẻ file, gửi thông báo hay sửa tài liệu Google khác. Ghi link/tab/range đã cập nhật và các phần chưa hoàn tất.

Mẫu yêu cầu: “Dùng $ai-capability-review chuẩn bị bảng đánh giá L1–L5 cho danh sách trong input, giữ điểm trống và tạo phần tổng hợp theo level.”
