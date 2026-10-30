# Đầu vào ước lượng story point

- Hồ sơ: run ID, người yêu cầu, nội dung ủy quyền cập nhật Jira/provisional estimate, thời điểm lấy/cutoff và múi giờ.
- Phạm vi: board ID, project/filter, version ID hoặc sprint ID, issue types Story/Bug, JQL, phân trang, issue key khử trùng; board sở hữu nếu giao nhau.
- Chế độ: đề xuất / điền thiếu / đánh lại điểm đã có trong phạm vi yêu cầu; các field được ủy quyền cập nhật.
- Mapping: field ID/type/context của Original story points và Story Points, nguồn xác minh, quyền đọc và `editmeta` theo project/issue type/issue; tách thiếu field, không writable, lỗi đọc và `null`.
- Snapshot issue: description, AC, task/subtask Dev/QA, links, comment làm rõ, changelog, hai điểm hiện tại và mốc snapshot; nội dung không truy xuất được.
- Baseline cam kết hiện có: đường dẫn, `baseline_at`, quy tắc ghi change log; không sửa bản chốt.
- Mẫu riêng board: đường dẫn/version base point, thang quan sát và thang đã xác nhận, anchor keys, điểm/field nguồn/mốc, bằng chứng xác nhận, review state/confidence; hoặc nêu chưa có mẫu.
- Mẫu lịch sử bổ sung: JQL/phạm vi/thời điểm, độ đầy đủ, nguồn estimate, lý do chọn/loại; tách issue AI mới đánh khỏi anchor đã team xác nhận.
- Điểm chưa rõ: Dev, QA/retest, dependency, reproduction/root cause bug, tiêu chí nghiệm thu; assumptions cho provisional estimate nếu được ủy quyền.
- Hiện trạng triển khai: chức năng/API/data model/test đã có, phần reuse, phần bổ sung; nguồn SRS/quy tắc nghiệp vụ. Repo/branch/commit và module thực sự đã kiểm tra, hoặc ghi chưa kiểm tra; chỉ cần nguồn liên quan có khả năng làm đổi estimate.
- Registry nguồn private: URL/đường dẫn SRS gốc/module, repo theo ứng dụng/vai trò, branch/commit, modified time và trạng thái đọc/quyền truy cập. Kiểm tra đúng Client/Coach/Web/Backend; phân biệt code develop với release/production baseline.
- Research/Investigation: deliverables nghiên cứu, phạm vi kiểm chứng, phần triển khai tương lai được loại; phần trùng/dependency giữa issue dùng chung tài liệu nguồn.

Không yêu cầu người dùng nhập lại dữ kiện đọc được từ Jira/cấu hình local. Hồ sơ thật lưu trong `private/estimation/runs/<run-id>/`, kèm board ID; bộ base point lưu riêng tại `private/estimation/boards/<board-id>/`.
