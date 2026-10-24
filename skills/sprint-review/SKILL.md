---
name: sprint-review
description: Tổng kết sprint theo baseline cam kết, SP clear và chưa clear, scope thay đổi, mục tiêu, chất lượng và hành động cải tiến của team.
---

# Tổng kết sprint

Đọc [đầu vào](assets/input.md), baseline và changelog; viết [đầu ra](assets/output.md) vào `private/sprints/<sprint-id>/sprint-review/`. Tính theo [quy ước đo lường](../../docs/metrics.md), không dùng trạng thái hiện tại thay cho trạng thái tại cutoff.

1. Chốt cutoff và độ đầy đủ dữ liệu. Lấy baseline, thay đổi scope, lịch sử status và bằng chứng DoD/acceptance. Thiếu history hoặc estimate phải hiện trong phần giới hạn kết quả.
2. Đối chiếu từng issue: SP baseline, SP hiện tại, clear tại cutoff, resolved nhưng chưa xác nhận clear, added, removed, cancelled, reopened. Đây có thể là các cờ giao nhau; không cộng chúng thành tổng độc lập.
3. Báo C, D, U và tỷ lệ D/C với mẫu số rõ ràng. Removed vẫn trong cam kết gốc; added báo riêng. Phân biệt tổng giao theo estimate chốt với tổng theo estimate hiện tại. Không đếm trùng issue hoặc parent/subtask. Nếu tổng hợp nhiều board, khử trùng theo issue key và quy tắc board sở hữu; giữ số liệu riêng khi mapping hoặc thang estimate không tương đồng.
4. Đánh giá từng mục tiêu theo acceptance và hạn, ghi ai xác nhận. Nêu kết quả không đạt và tác động thực tế kể cả khi SP hoàn tất cao.
5. Phân tích hệ thống và trách nhiệm dựa trên timeline: scope, capacity, dependency, chất lượng, handoff, cảnh báo và quyết định của leader. Không kết luận lỗi chỉ từ assignee hoặc số SP.
6. Đưa ra hành động cải tiến có owner, hạn và tiêu chí thành công. Chuyển bằng chứng cần trao đổi cá nhân sang individual-review trong [index](../../INDEX.md); không đưa nhận xét nhạy cảm vào bản tổng hợp rộng.

Mẫu yêu cầu: “Dùng `$sprint-review` cho sprint `<id>` tại `<cutoff>`, đối chiếu cam kết gốc, nêu SP chưa clear và mục tiêu không đạt cùng nguyên nhân có bằng chứng, rồi đề xuất cải tiến có owner.”
