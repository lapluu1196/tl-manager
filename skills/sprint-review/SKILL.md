---
name: sprint-review
description: Tổng kết sprint theo baseline cam kết, SP clear và chưa clear, scope thay đổi, mục tiêu, chất lượng và hành động cải tiến của team.
---

# Tổng kết sprint

Đọc [đầu vào](assets/input.md), baseline và changelog; viết [đầu ra](assets/output.md) vào `private/sprints/<sprint-id>/sprint-review/`. Tính theo [quy ước đo lường](../../docs/metrics.md), không dùng trạng thái hiện tại thay cho trạng thái tại cutoff.

1. Chốt cutoff và độ đầy đủ dữ liệu. Phân biệt `baseline_at` (mốc đo ngay sau sprint start), `locked_at` (lúc xác nhận) và cutoff kết quả; không dùng SP tại locked_at thay baseline_at. Lấy baseline, thay đổi scope, lịch sử status và bằng chứng DoD/acceptance. Thiếu history hoặc estimate phải hiện trong phần giới hạn kết quả.
2. Đối chiếu từng Bug/Story: SP team tại baseline_at, lúc added và hiện tại cùng hai giá trị gốc, trường SP được chọn và bằng chứng. Mọi board ưu tiên Original story points; chỉ fallback Story Points khi Original null/không có, Original=0 hợp lệ, cả hai thiếu là chưa estimate. Không theo field estimate mặc định board. Đối chiếu clear tại cutoff, resolved nhưng chưa xác nhận clear, added, removed, cancelled, reopened. Đây có thể là các cờ giao nhau; không cộng chúng thành tổng độc lập.
3. Kiểm tra scope cam kết đầu sprint: Bug tự thuộc cam kết; Story cần task QA thuộc chính sprint đang tính, đã liên kết/subtask tới Story tại baseline_at. Task QA sprint trước không đủ và task QA đã bóc không chứng minh clear. Báo C, D, U và tỷ lệ D/C với mẫu số rõ ràng. Removed vẫn trong cam kết gốc; added báo riêng. Phân biệt tổng giao theo estimate chốt với tổng theo estimate hiện tại. Không đếm trùng issue hoặc parent/subtask. Nếu tổng hợp nhiều board, khử trùng theo issue key và quy tắc board sở hữu; giữ số liệu riêng khi mapping hoặc thang estimate không tương đồng.
4. Đánh giá từng mục tiêu theo acceptance và hạn, ghi ai xác nhận. Nêu kết quả không đạt và tác động thực tế kể cả khi SP hoàn tất cao.
5. Phân tích hệ thống và trách nhiệm dựa trên timeline: scope, capacity, dependency, chất lượng, handoff, cảnh báo và quyết định của leader. Không kết luận lỗi chỉ từ assignee hoặc số SP.
6. Đưa ra hành động cải tiến có owner, hạn và tiêu chí thành công. Chuyển bằng chứng cần trao đổi cá nhân sang individual-review trong [index](../../INDEX.md); không đưa nhận xét nhạy cảm vào bản tổng hợp rộng.

Khi có báo cáo tập trung được cấu hình và được ủy quyền cập nhật, bàn giao bản tổng hợp team qua [management-reporting](../management-reporting/SKILL.md); giữ baseline và snapshot cũ, không đưa đánh giá cá nhân nhạy cảm vào Sheet chia sẻ rộng.

Mẫu yêu cầu: “Dùng `$sprint-review` cho sprint `<id>` tại `<cutoff>`, đối chiếu cam kết gốc, nêu SP chưa clear và mục tiêu không đạt cùng nguyên nhân có bằng chứng, rồi đề xuất cải tiến có owner.”
