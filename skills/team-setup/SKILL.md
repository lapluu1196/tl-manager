---
name: team-setup
description: Thiết lập vai trò BA Dev QA, lịch làm việc, capacity và mapping Jira trước khi lập sprint hoặc khi team thay đổi.
---

# Thiết lập team và capacity

Đọc [đầu vào](assets/input.md), điền [đầu ra](assets/output.md) tại `private/sprints/<sprint-id>/team-setup/`. Dùng [quy ước đo lường](../../docs/metrics.md); xem các đầu việc kế tiếp ở [index](../../INDEX.md).

1. Đọc `.local/workspace.json` nếu có; chọn board của sprint từ `jira.boards` và xác nhận project/filter, trường SP/sprint, trạng thái Done/hủy, DoR và DoD của board bằng nguồn thực tế. Không suy diễn ID trường hoặc status từ tên tiếng Anh. Với nhiều board, ghi vùng issue giao nhau và quy tắc board sở hữu trước khi tổng hợp.
2. Tính ngày làm việc từ lịch hai tuần, `working_days`, nghỉ lễ và phép. Liệt kê phân bổ ngoài sprint và buffer. Với người kiêm vai trò, chia capacity BA/Dev/QA; tổng không vượt capacity của người đó.
3. Chốt vai trò, người quyết định ưu tiên/acceptance, người dự phòng, giới hạn WIP và thời gian bàn giao. Capacity chỉ tính theo đơn vị thống nhất; không chuyển SP thành giờ.
4. Chốt quy tắc label với prefix trong cấu hình: `goal-<slug>`, `stream-<slug>`, `type-<slug>`, `risk-<slug>`. Ghi danh mục giá trị hợp lệ và mục đích; không tạo label chứa thông tin nhân sự nhạy cảm.
5. Ghi nguồn, thời điểm và giả định còn thiếu. Chỉ đánh dấu sẵn sàng planning nếu mapping, DoD và capacity tối thiểu đã xác nhận; còn thiếu thì đưa ra bản nháp có người chịu trách nhiệm bổ sung.

Mẫu yêu cầu: “Dùng `$team-setup` cho sprint `<id>`, đọc input trong thư mục sprint, tính capacity từng vai trò và chỉ ra dữ liệu còn thiếu trước planning.”
