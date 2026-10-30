---
name: sprint-commitment
description: Chốt cam kết sprint và baseline bất biến cho scope, SP, mục tiêu và due date; theo dõi mọi thay đổi sau khi chốt.
---

# Chốt cam kết sprint

“Commit” ở đầu việc này là cam kết sprint, không phải Git commit. Đọc [đầu vào](assets/input.md) và kế hoạch đã thống nhất; dùng [đầu ra](assets/output.md) tại `private/sprints/<sprint-id>/sprint-commitment/`. Áp dụng [quy ước đo lường](../../docs/metrics.md).

1. Kiểm tra người chốt, `baseline_at`, `locked_at`, sprint/board, phạm vi issue, mapping SP/Done và DoD. Với baseline đầu sprint, `baseline_at` là ngay sau sprint start thực tế; `locked_at` là lúc xác nhận/lưu bản chốt. Sprint chưa start chỉ có planning draft, không tạo baseline đầu sprint giả. Đối chiếu capacity và acceptance từng mục tiêu; còn thiếu estimate phải nêu rõ.
2. Tính SP team Dev + QA trên chính Bug/Story, loại issue Designer/BA riêng, không cộng task/subtask hoặc phân bổ cho cá nhân. Mọi board ưu tiên Original story points; chỉ fallback Story Points khi Original null/không có, Original=0 hợp lệ, cả hai thiếu là chưa estimate. Không lấy field estimate mặc định board thay quy tắc này. Tách tổng SP đầu sprint và SP cam kết clear: Bug trong scope tự thuộc cam kết; Story cần task QA thuộc chính sprint đang tính và có liên kết/subtask tới Story tại `baseline_at`, với bằng chứng vai trò QA. Task QA sprint trước không đủ; task QA đã bóc chưa chứng minh clear thực tế.
3. Chụp hoặc tái dựng baseline từng issue tại `baseline_at`: key/type, giá trị hai trường SP, SP được chọn/trường nguồn/lý do fallback, căn cứ cam kết, task QA và sprint/link, goal, owner vai trò, due date, label, status và nguồn. Snapshot hiện tại không thay thế lịch sử tại start; cần bao phủ cả issue/task đã removed, thay SP và role/link. Thiếu bằng chứng thì ghi chưa xác minh, không chốt tổng đầy đủ. Ghi tổng SP đã biết và số issue thiếu estimate riêng.
4. Lưu bản chốt có phiên bản, ví dụ `baseline-v1.md`, cùng hai mốc đo/xác nhận, người xác nhận và nguồn snapshot/lịch sử. Giữ bản đó bất biến. `output.md` có thể là bản làm việc dẫn đến baseline; không sửa đè bản đã chốt.
5. Bất kỳ thêm/bỏ issue, thay estimate, task QA, deadline hoặc mục tiêu nào sau `baseline_at` đều vào change log với trước/sau, lý do, người quyết định và ảnh hưởng. Việc hủy hoặc removed không tự giảm mẫu số của cam kết gốc. Nếu cần đính chính dữ liệu, lưu bản mới kèm liên kết bản gốc và lý do; báo cả hai thay vì âm thầm tái lập baseline.
6. Bàn giao baseline và log cho daily-risk và sprint-review trong [index](../../INDEX.md). Thực hiện [tự phát triển workflow](../../docs/extending.md#tự-phát-triển-sau-mỗi-đầu-việc), ghi quy ước đã cập nhật và phần còn chờ quyết định; không mở rộng quyền thao tác Jira/Git.

Khi có báo cáo tập trung được cấu hình và được ủy quyền cập nhật, bàn giao qua [management-reporting](../management-reporting/SKILL.md); công bố snapshot cam kết có mốc đo và giới hạn dữ liệu, giữ nguyên baseline gốc và lịch sử công bố.

Mẫu yêu cầu: “Dùng `$sprint-commitment` chốt sprint `<id>` theo planning đã được xác nhận; lập baseline SP, mục tiêu, due date và change log. Chỉ rõ dữ liệu chưa đủ để chốt.”
