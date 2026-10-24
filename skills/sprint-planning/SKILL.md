---
name: sprint-planning
description: Lập kế hoạch sprint hai tuần với mục tiêu, SP, workload BA Dev QA, phụ thuộc, due date và label chuẩn.
---

# Lập kế hoạch sprint

Đọc [đầu vào](assets/input.md) cùng kết quả team-setup; viết [đầu ra](assets/output.md) vào `private/sprints/<sprint-id>/sprint-planning/`. Dùng [quy ước đo lường](../../docs/metrics.md) và [index](../../INDEX.md).

1. Xếp thứ tự mục tiêu theo giá trị và hạn thực tế. Mỗi mục tiêu có tiêu chí acceptance kiểm chứng được và người nghiệm thu; không suy mục tiêu từ tổng SP.
2. Kiểm tra DoR: yêu cầu/AC, thiết kế hoặc dữ liệu cần có, dependency, estimate. Thiếu DoR thì đề xuất làm rõ hoặc tách spike với đầu ra cụ thể; không tự tạo estimate thay team.
3. Ước lượng bằng thang cấu hình, ghi bất định và người xác nhận. Chọn một cấp issue tính SP, không cộng parent và subtask. Dùng velocity tương đồng làm tham khảo cho tổng team.
4. Phân rã việc BA/Dev/QA với owner, effort và capacity cùng đơn vị. Kiểm tra ngày bàn giao, dependency, thời gian QA/retest, buffer, WIP và việc ngoài sprint. Một story có assignee không có nghĩa một người thực hiện tất cả vai trò.
5. Đề xuất thứ tự, due date, label theo danh mục đã chốt. Chỉ đưa vào cam kết khi khả thi theo vai trò và có đường đi tới DoD. Ghi rõ phương án giảm scope hoặc đổi thứ tự khi quá tải.
6. Xuất kế hoạch nháp với dữ liệu thiếu và các quyết định cần chốt; bàn giao sang sprint-commitment. Thay đổi Jira chỉ trong phạm vi người dùng đã cho phép; nếu chưa có, xuất bảng thay đổi đề xuất.

Mẫu yêu cầu: “Dùng `$sprint-planning` cho sprint `<id>` với input đã điền; đề xuất scope phù hợp BA/Dev/QA, nêu nút thắt, lịch QA và các label cần áp dụng.”
