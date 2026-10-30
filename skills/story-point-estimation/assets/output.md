# Kết quả ước lượng story point

## Phạm vi và chất lượng dữ liệu

- Board/project/filter, version hoặc sprint ID; run ID, người yêu cầu/phạm vi ủy quyền.
- `fetched_at`, `cutoff_at`, múi giờ, nguồn/JQL, phân trang và số Story/Bug duy nhất.
- Nguồn không truy xuất được, scope chưa rõ, estimate thiếu và giới hạn kết luận.
- Registry nguồn code/SRS đã được cung cấp; nguồn nào đã đọc, chưa đọc do quyền, thiếu repo/nhánh ứng dụng và khác biệt giữa develop với release/production. Không coi mô tả Jira là hiện trạng khi code đã có thay đổi; cũng không suy code đã deploy chỉ từ snapshot repo.
- Bộ base point đúng board: đường dẫn, version, thang quan sát/đã xác nhận, review state, confidence, thay đổi và điều chờ xác nhận.

## Estimate và căn cứ

| Issue | Original hiện tại | Story Points hiện tại | Điểm đề xuất | Anchor/nguồn | Tương đồng và chênh lệch Dev + QA | Assumptions / bất định / ngoại lệ | Confidence / review state |
| --- | --- | --- | --- | --- | --- | --- | --- |

Ghi rõ `null`, `0` và lỗi truy xuất. `Chưa đủ dữ liệu` không có điểm số; ghi câu hỏi/người làm rõ. Provisional estimate có assumptions và điều kiện review, không tự thành team-confirmed. Research chỉ tính deliverables nghiên cứu; issue giao nhau ghi ranh giới tránh double count. Tổng điểm đề xuất chỉ cộng phần đã biết, kèm số issue thiếu; không làm baseline quá khứ.

Với issue point lớn so với mẫu board, ghi rõ điểm đã có giữ nguyên hay AI vừa đánh; tách chức năng hiện có, phần reuse, phần bổ sung và regression Dev + QA. Nêu bằng chứng code/business đã kiểm tra, giả định chưa kiểm chứng và câu trả lời nào có thể làm thay đổi mức điểm; không dùng độ dài mô tả để bảo vệ estimate.

Phân biệt yêu cầu bắt buộc với phương án UX/kiến trúc, mở rộng tương lai và hành vi chưa chốt. Với app dùng chung source/phân quyền, ghi kiến trúc đã được xác nhận cùng bằng chứng role/routing/target identity/ACL thực sự kiểm tra được.

## Kiểm tra và cập nhật Original story points / Story Points

| Project / issue type / issue | Tên field | Field ID / type | Tồn tại/áp dụng | Đọc được / writable | Nguồn catalog/context/editmeta | Xử lý và lý do |
| --- | --- | --- | --- | --- | --- | --- |

| Issue | Field ID | Old trong diff | New | Re-read trước ghi | Kết quả ghi | Giá trị xác minh sau ghi | Thời điểm / lý do / người quyết định |
| --- | --- | --- | --- | --- | --- | --- | --- |

Tách chưa được ủy quyền, giữ điểm đã có, thiếu field, không writable, xung đột, lỗi và thành công. Nếu chỉ điền thiếu và hai field còn khác nhau, nêu sự khác biệt. Không tạo field, không sửa baseline; dẫn change log cho estimate thay đổi sau baseline.

## Kết quả và bước tiếp theo

- Số issue: trong phạm vi, đủ căn cứ estimate, đã cập nhật ít nhất một field, giữ nguyên, chưa đủ dữ liệu, lỗi/xung đột. Các nhóm giao nhau phải đánh dấu, không cộng như tập loại trừ nhau.
- Số ghi và xác minh từng field; SP hiện tại đã xác minh tách SP đề xuất; thiếu giá trị không là 0.
- Ngoại lệ, câu hỏi, owner/hạn xử lý; đề xuất tách issue nếu cần.
- Tự phát triển: quy ước đã xác nhận, skill/template đã cập nhật, mẫu private đã thêm với provenance/review state và việc chờ review; hoặc đã rà soát và không có điều mới.
