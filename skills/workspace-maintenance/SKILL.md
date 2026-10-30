---
name: workspace-maintenance
description: Bổ sung hoặc sửa đầu việc quản lý, đăng ký tích hợp và phụ thuộc, cập nhật index và kiểm tra khả năng dùng workspace trên máy khác.
---

# Bảo trì workspace

Đọc [đầu vào](assets/input.md), ghi [đầu ra](assets/output.md) vào `private/sprints/<sprint-id>/workspace-maintenance/` hoặc hồ sơ vận hành riêng trong `private/` nếu không gắn sprint.

1. Với yêu cầu tự phát triển hoặc sau mỗi đầu việc, áp dụng [quy trình bắt buộc](../../docs/extending.md#tự-phát-triển-sau-mỗi-đầu-việc): rà soát điều đã thống nhất/bài học có bằng chứng, cập nhật skill/docs/template sở hữu; tách đề xuất chưa xác nhận, giữ dữ liệu thật trong `private/` và không mở rộng quyền hành động. Nếu không có điều mới, ghi kết quả rà soát.
2. Xác định đầu việc mới có khác đầu việc trong [index](../../INDEX.md) hay chỉ là một bước của quy trình hiện có. Chốt trigger, input, output và người dùng kết quả trước khi thêm package.
3. Nếu cần đầu việc mới, tạo khung bằng `python3 scripts/workspace.py add-workstream <slug> --title "Tên đầu việc"`. Dùng slug chữ thường, số và dấu gạch ngang. Hoàn thiện `skills/<slug>/SKILL.md`, `assets/input.md`, `assets/output.md`; điền thông tin registry trong `config/workstreams.json` và tái tạo index bằng `python3 scripts/workspace.py index`.
4. Đầu việc cần công cụ hoặc credential mới: khai báo tích hợp/phụ thuộc ở `config/integrations.json`, liên kết integration ID trong workstream, cập nhật hướng dẫn bootstrap và file mẫu cấu hình tương ứng. Kiểm tra schema hiện có trước khi sửa; không tạo package dependency không được sử dụng.
5. Credential thật chỉ đi vào file local bị gitignore hoặc secret manager đã chọn. File mẫu chỉ chứa tên biến/placeholder. Không đưa PAT, nội dung Jira nội bộ hoặc đánh giá nhân sự vào Git; xác minh dữ liệu private không nằm trong tracked files.
6. Chạy `python3 scripts/workspace.py bootstrap` và `python3 scripts/workspace.py validate`; kiểm tra các link, input/output được sao chép và index có đầu việc mới. Dùng `--help` để xác nhận cú pháp của lệnh phụ trước khi gọi. Ghi dependency/runtime và thao tác cần làm khi chuyển máy.
7. Đọc diff và chạy kiểm tra phù hợp với phần thay đổi. Commit/push theo phạm vi người dùng đã cho phép; báo rõ thay đổi cục bộ, thay đổi đã đồng bộ và credential vẫn phải cung cấp riêng trên máy mới.

Mẫu yêu cầu: “Dùng `$workspace-maintenance` thêm đầu việc `<slug>` cho `<mục đích>`; tạo package, input/output, đăng ký integration nếu cần và cập nhật index, rồi chạy validate.”
