# Kết quả: Tổng kết sprint

| Thông tin | Giá trị |
| --- | --- |
| Sprint / board / khoảng thời gian / múi giờ | |
| Baseline / baseline_at mốc đầu sprint / locked_at xác nhận | |
| cutoff_at / fetched_at / nguồn / độ đầy đủ | |
| DoD / cấp issue tính SP | |
| Phạm vi board / cách khử trùng nếu tổng hợp bộ phận | |
| Người xác nhận báo cáo / lúc xác nhận | |

## Kết quả cam kết

| Chỉ số | Giá trị | Cách tính / giới hạn |
| --- | --- | --- |
| C: SP baseline đã biết | | |
| D: SP baseline clear tại cutoff | | |
| U: SP baseline chưa clear | | C - D |
| Hoàn thành cam kết | | D/C; N/A nếu C = 0; gắn chưa đầy đủ nếu thiếu estimate |
| Issue baseline thiếu estimate | | Không tính như 0 SP |
| Issue added thiếu estimate tại lúc nhận thêm | | Không tính như 0 SP |
| Issue đã clear thiếu estimate theo mốc tương ứng | | Tách baseline và added; tổng SP giao chưa đầy đủ |
| Added: số issue / SP tại lúc nhận thêm | | Ngoài C |
| Added đã clear: số issue / SP tại lúc nhận thêm | | |
| Removed: số issue / SP baseline liên quan | | Không giảm C |
| Reopened trước cutoff / sau cutoff | | Tách thời điểm; có thể giao với các nhóm khác |
| Resolved nhưng chưa xác nhận clear | | |
| Giao thực tế theo estimate đã chốt | | D + SP lúc nhận của added đã clear |
| Tổng clear theo SP hiện tại, nếu cần | | Chỉ số riêng; ghi thời điểm estimate |

## Nguồn SP từng issue

SP team trên Story/Bug; loại issue Designer/BA riêng, không cộng task/subtask. Ưu tiên Original story points; fallback Story Points chỉ khi Original null/không có. Original=0 hợp lệ; cả hai thiếu là chưa estimate. Không dùng field estimate mặc định board thay quy tắc team. Giữ nguồn tại từng mốc, không điền SP hiện tại ngược về baseline.

| Issue | Mốc: baseline_at / lúc added / hiện tại | Original story points | Story Points | SP chọn / trường nguồn / lý do fallback | Bằng chứng snapshot / history |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Mục tiêu

| Goal | Đạt / một phần / không đạt / thiếu dữ liệu | Acceptance / bằng chứng | Đúng hạn? | Người xác nhận | Tác động còn lại |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Cam kết chưa clear và scope thay đổi

| Issue | SP baseline / chưa estimate | Status tại cutoff | Cờ removed / cancelled / reopened | Nguyên nhân đã xác minh hoặc giả thuyết | Tác động mục tiêu | Quyết định xử lý tiếp |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Hiệu suất và chất lượng team

| Nhận định | Bằng chứng / thời điểm | Bối cảnh capacity / scope | Giới hạn kết luận | Hành động |
| --- | --- | --- | --- | --- |
| | | | | |

## Cải tiến đã thống nhất

| Action ID | Việc thay đổi | Owner | Hỗ trợ cần có | Hạn | Tiêu chí thành công / ngày kiểm tra |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Dữ liệu cần bổ sung hoặc đính chính

| Nội dung | Ảnh hưởng số liệu / kết luận | Owner | Hạn | Bản báo cáo kế tiếp |
| --- | --- | --- | --- | --- |
| | | | | |
