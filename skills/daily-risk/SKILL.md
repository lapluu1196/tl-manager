---
name: daily-risk
description: Theo dõi sprint mỗi ngày, dự báo rủi ro mục tiêu và chỉ định can thiệp dựa trên bằng chứng Jira, dependency và capacity BA Dev QA.
---

# Theo dõi ngày và rủi ro

Đọc [đầu vào](assets/input.md), baseline và change log; ghi [đầu ra](assets/output.md) trong `private/sprints/<sprint-id>/daily-risk/`. Lưu bản theo ngày khi cần lịch sử, ví dụ `2026-10-26.md`. Áp dụng [quy ước đo lường](../../docs/metrics.md).

1. Chụp thời điểm theo dõi, nguồn dữ liệu và tính đầy đủ. So với ngày trước; đánh dấu thông tin cũ và khoảng trống. Không coi thiếu cập nhật là bằng chứng một cá nhân làm chậm.
2. Kiểm tra đường tới acceptance từng mục tiêu: việc BA chưa sẵn sàng, dependency bên ngoài, Dev chưa bàn giao, hàng đợi QA/retest, review/release và số ngày còn lại. SP resolved chưa đủ để xác nhận clear.
3. Phân loại theo bằng chứng: xanh khi còn kế hoạch khả thi; vàng khi có nguy cơ cần can thiệp; đỏ khi chưa có phương án đáng tin để đạt hạn; chưa đủ dữ liệu khi không thể đánh giá. Ghi lý do và mức tin cậy, không tự suy xác suất chính xác.
4. Mỗi rủi ro có tác động, người xử lý, can thiệp cụ thể, hạn kiểm tra và điều kiện escalation. Tách owner công việc, owner dependency và leader ra quyết định; chỉ định owner không đồng nghĩa kết luận lỗi.
5. Đề xuất đổi scope/owner/deadline theo tác động. Ghi quyết định mới vào log và giữ baseline nguyên vẹn. Bàn giao các quyết định cần leader xử lý qua báo cáo, dùng [index](../../INDEX.md) để chuyển đầu việc.

Mẫu yêu cầu: “Dùng `$daily-risk` cho sprint `<id>` tại `<cutoff>`, so với ngày trước, chỉ ra mục tiêu có nguy cơ và ba can thiệp cần làm sớm nhất kèm owner, hạn và bằng chứng.”
