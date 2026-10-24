---
name: sprint-commitment
description: Chốt cam kết sprint và baseline bất biến cho scope, SP, mục tiêu và due date; theo dõi mọi thay đổi sau khi chốt.
---

# Chốt cam kết sprint

“Commit” ở đầu việc này là cam kết sprint, không phải Git commit. Đọc [đầu vào](assets/input.md) và kế hoạch đã thống nhất; dùng [đầu ra](assets/output.md) tại `private/sprints/<sprint-id>/sprint-commitment/`. Áp dụng [quy ước đo lường](../../docs/metrics.md).

1. Kiểm tra người chốt, `locked_at`, sprint/board, phạm vi issue, mapping SP/Done và DoD. Đối chiếu capacity và acceptance từng mục tiêu; còn thiếu estimate phải nêu rõ trước khi cam kết.
2. Chụp baseline từng issue: key, SP tại lúc chốt, goal, owner vai trò, due date, label, status và nguồn. Ghi tổng SP đã biết và số issue chưa estimate riêng.
3. Lưu bản chốt có phiên bản, ví dụ `baseline-v1.md`, cùng thời điểm, người xác nhận và nguồn snapshot. Giữ bản đó bất biến. `output.md` có thể là bản làm việc dẫn đến baseline; không sửa đè bản đã chốt.
4. Bất kỳ thêm/bỏ issue, thay estimate, deadline hoặc mục tiêu nào sau `locked_at` đều vào change log với trước/sau, lý do, người quyết định và ảnh hưởng. Việc hủy hoặc removed không tự giảm mẫu số của cam kết gốc.
5. Nếu cần đính chính dữ liệu, lưu bản mới kèm liên kết bản gốc và lý do; báo cả hai thay vì âm thầm tái lập baseline. Bàn giao baseline và log cho daily-risk và sprint-review trong [index](../../INDEX.md).

Mẫu yêu cầu: “Dùng `$sprint-commitment` chốt sprint `<id>` theo planning đã được xác nhận; lập baseline SP, mục tiêu, due date và change log. Chỉ rõ dữ liệu chưa đủ để chốt.”
