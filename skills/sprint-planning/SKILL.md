---
name: sprint-planning
description: Lập kế hoạch sprint hai tuần với mục tiêu, SP, workload BA Dev QA, phụ thuộc, due date và label chuẩn.
---

# Lập kế hoạch sprint

Đọc [đầu vào](assets/input.md) cùng kết quả team-setup; viết [đầu ra](assets/output.md) vào `private/sprints/<sprint-id>/sprint-planning/`. Dùng [quy ước đo lường](../../docs/metrics.md) và [index](../../INDEX.md).

1. Xếp thứ tự mục tiêu theo giá trị và hạn thực tế. Mỗi mục tiêu có tiêu chí acceptance kiểm chứng được và người nghiệm thu; không suy mục tiêu từ tổng SP.
2. Kiểm tra DoR: yêu cầu/AC, thiết kế hoặc dữ liệu cần có, dependency, estimate. Thiếu DoR thì đề xuất làm rõ hoặc tách spike với đầu ra cụ thể; không tự tạo estimate thay team.
3. Ước lượng bằng thang cấu hình, ghi bất định và người xác nhận. Khi tổng hợp planning đầu sprint, áp dụng mục “Tổng hợp planning và cam kết đầu sprint” trong quy ước đo lường: SP team Dev + QA trên chính Bug/Story, loại issue Designer/BA riêng, không cộng task/subtask. Mọi board ưu tiên Original story points; chỉ fallback Story Points khi Original null/không có, Original=0 vẫn hợp lệ, cả hai thiếu là chưa estimate. Lưu giá trị hai trường, trường được chọn và bằng chứng theo từng issue; không theo field estimate mặc định board. Dùng velocity tương đồng làm tham khảo cho tổng team.
4. Phân rã việc BA/Dev/QA với owner, effort và capacity cùng đơn vị. Kiểm tra ngày bàn giao, dependency, thời gian QA/retest, buffer, WIP và việc ngoài sprint. Một story có assignee không có nghĩa một người thực hiện tất cả vai trò.
5. Đề xuất thứ tự, due date, label theo danh mục đã chốt. Chỉ đưa vào cam kết khi khả thi theo vai trò và có đường đi tới DoD. Ghi rõ phương án giảm scope hoặc đổi thứ tự khi quá tải.
6. Xuất kế hoạch nháp với dữ liệu thiếu và các quyết định cần chốt; tách tổng SP đầu sprint khỏi scope/SP cam kết clear (Bug tự thuộc cam kết; Story cần task QA thuộc chính sprint đang tính và đã liên kết/subtask tại mốc đầu sprint; task QA sprint trước không đủ). Sprint chưa start chỉ có planning draft; nếu đã start, lấy mốc thực tế ngay sau start và tái dựng lịch sử đủ cả removed, không dùng snapshot hiện tại giả làm baseline quá khứ. Bàn giao sang sprint-commitment. Thay đổi Jira chỉ trong phạm vi người dùng đã cho phép; nếu chưa có, xuất bảng thay đổi đề xuất.

Khi cần đánh điểm Story/Bug hoặc hiệu chỉnh base point, dùng [story-point-estimation](../story-point-estimation/SKILL.md): mẫu riêng từng board, cập nhật hai trường theo ủy quyền và giữ nguyên baseline đã chốt.

Khi có báo cáo tập trung được cấu hình và được ủy quyền cập nhật, bàn giao qua [management-reporting](../management-reporting/SKILL.md); giữ Markdown và nguồn private, ghi rõ nháp hay baseline, không cộng hai loại số liệu.

Kết thúc đầu việc, thực hiện [tự phát triển workflow](../../docs/extending.md#tự-phát-triển-sau-mỗi-đầu-việc): cập nhật quy ước đã xác nhận vào nơi sở hữu và ghi riêng điều còn chờ quyết định.

Mẫu yêu cầu: “Dùng `$sprint-planning` cho sprint `<id>` với input đã điền; đề xuất scope phù hợp BA/Dev/QA, nêu nút thắt, lịch QA và các label cần áp dụng.”
