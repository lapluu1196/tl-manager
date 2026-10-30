---
name: daily-risk
description: Theo dõi sprint mỗi ngày, dự báo rủi ro mục tiêu và chỉ định can thiệp dựa trên bằng chứng Jira, dependency và capacity BA Dev QA.
---

# Theo dõi ngày và rủi ro

Đọc [đầu vào](assets/input.md), baseline và change log; phân biệt `baseline_at` (mốc đo ngay sau sprint start), `locked_at` (lúc xác nhận) với `cutoff_at` theo dõi. Ghi [đầu ra](assets/output.md) trong `private/sprints/<sprint-id>/daily-risk/`. Lưu bản theo ngày khi cần lịch sử, ví dụ `2026-10-26.md`. Áp dụng [quy ước đo lường](../../docs/metrics.md).

1. Chụp thời điểm theo dõi, nguồn dữ liệu và tính đầy đủ. Giữ SP team trên Story/Bug ở baseline_at bất biến; SP hiện tại nếu cần dùng Original story points ưu tiên, chỉ fallback Story Points khi Original null/không có (0 hợp lệ), lưu trường nguồn và bằng chứng từng issue. So với ngày trước; đánh dấu thông tin cũ và khoảng trống. Không coi thiếu cập nhật là bằng chứng một cá nhân làm chậm.
2. Kiểm tra đường tới acceptance từng mục tiêu: việc BA chưa sẵn sàng, dependency bên ngoài, Dev chưa bàn giao, hàng đợi QA/retest, review/release và số ngày còn lại. SP resolved chưa đủ để xác nhận clear.
   - Khi kiểm tra release, đối chiếu riêng trạng thái issue, cờ `released` của fix version và task QA trước/sau release. Tên version có chữ “released” không thay thế cờ API; cờ `released=true` cũng không đủ xác nhận issue đã clear. Ghi rõ chênh lệch, nguồn và thời điểm; thiếu bằng chứng triển khai/QA thì giới hạn kết luận theo dữ liệu Jira. Nếu người dùng chưa nêu sprint/version, xác minh metadata và ghi rõ phạm vi được kiểm tra, tách các ticket cũ ngoài sprint.
3. Phân loại theo bằng chứng: xanh khi còn kế hoạch khả thi; vàng khi có nguy cơ cần can thiệp; đỏ khi chưa có phương án đáng tin để đạt hạn; chưa đủ dữ liệu khi không thể đánh giá. Ghi lý do và mức tin cậy, không tự suy xác suất chính xác.
4. Mỗi rủi ro có tác động, người xử lý, can thiệp cụ thể, hạn kiểm tra và điều kiện escalation. Tách owner công việc, owner dependency và leader ra quyết định; chỉ định owner không đồng nghĩa kết luận lỗi.
5. Đề xuất đổi scope/owner/deadline theo tác động. Ghi quyết định mới vào log và giữ baseline nguyên vẹn. Bàn giao các quyết định cần leader xử lý qua báo cáo, dùng [index](../../INDEX.md) để chuyển đầu việc.

Khi có báo cáo tập trung được cấu hình và được ủy quyền cập nhật, bàn giao qua [management-reporting](../management-reporting/SKILL.md); thêm snapshot theo cutoff, cập nhật rủi ro/quyết định trên Tổng quan và giữ lịch sử cùng ghi chú manager.

Mẫu yêu cầu: “Dùng `$daily-risk` cho sprint `<id>` tại `<cutoff>`, so với ngày trước, chỉ ra mục tiêu có nguy cơ và ba can thiệp cần làm sớm nhất kèm owner, hạn và bằng chứng.”
