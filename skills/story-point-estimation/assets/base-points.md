# Mẫu bộ base point riêng từng board

Sao chép vào `private/estimation/boards/<board-id>/base-points-v<version>.md`. Đây là khung tham khảo, không chứa Jira thật và chưa xác lập thang điểm board nào. Mẫu thật, mapping và quyết định review luôn ở private.

## Metadata bộ mẫu

- Board ID / project/filter / board sở hữu:
- Version / ngày tạo / cutoff / nguồn API/JQL / độ đầy đủ:
- Thang quan sát và thang đã xác nhận, nguồn xác nhận; chưa có ghi `chưa xác nhận`:
- Mapping hai field / quy tắc nguồn theo `docs/metrics.md`:
- Review state: `proposed` / `historical-observed` / `team-confirmed` / `retired`.
- Người review, thời điểm, bằng chứng xác nhận; confidence và giới hạn:
- Version trước / thay đổi / lý do / ngày xem xét lại:

## Khung tham khảo ban đầu

Tất cả dòng có provenance `generic-template`, review state `proposed`, confidence `chưa hiệu chỉnh`. Chỉ giữ mức phù hợp thang board sau khảo sát. Ví dụ hình dung độ lớn tương đối, không gán điểm bằng khớp mô tả máy móc. Không ép trần 13 nếu board có mẫu mức cao hơn.

| Mức tham khảo | Ví dụ giả định để tìm mẫu thật tương đồng | Cần kiểm chứng Dev + QA trước khi dùng |
| --- | --- | --- |
| 1 | Thay đổi giới hạn trong một hành vi đã hiểu rõ | Không có vùng ảnh hưởng ẩn; kiểm tra đúng hành vi và hồi quy liên quan |
| 2 | Điều chỉnh nhỏ có vài nhánh dữ liệu hoặc lỗi đã tái hiện | Nhánh điều kiện và vùng retest đã rõ |
| 3 | Luồng tính năng giới hạn hoặc sửa bug qua vài lớp | Phạm vi tích hợp, dữ liệu và hồi quy có thể liệt kê |
| 5 | Luồng nhiều nhánh, tương tác giữa các phần đã biết | Dependency, dữ liệu và ma trận QA tương ứng đã được tính |
| 8 | Phạm vi tương đối lớn hoặc nhiều tương tác so với mẫu board | Bất định/vùng ảnh hưởng được giải thích, cân nhắc tách |
| 13 | Phạm vi rất lớn so với anchor board | Kiểm tra khả năng chia nhỏ hoặc làm rõ trước chốt; không tự tạo issue |
| 21, 34 hoặc mức lớn khác (tùy board) | Chỉ dùng nếu có bằng chứng thang/mẫu riêng board | Xác minh phạm vi, khả năng tách và xác nhận; không thành mức mặc định chung |

## Anchor có bằng chứng

Mỗi anchor lưu một bản ghi; một mức có thể có nhiều mẫu. Không có mẫu thì ghi thiếu, không bịa issue. Issue Done chỉ là bối cảnh; status không quyết định effort.

| Anchor ID / issue key / link | Loại / phạm vi tại mốc estimate | Original / Story Points | Điểm chọn / field nguồn / thời điểm | Bằng chứng description / AC / task / link / changelog | Vì sao đại diện Dev + QA | Review state / reviewer / bằng chứng xác nhận | Confidence / giới hạn |
| --- | --- | --- | --- | --- | --- | --- | --- |

`historical-observed` chỉ xác nhận đã quan sát điểm trên Jira. Điểm AI đề xuất/vừa điền giữ `proposed`, không tự chuyển `team-confirmed` kể cả lần sau thấy điểm trên Jira. Lưu nguồn tạo estimate hoặc run để tránh dùng kết quả AI làm bằng chứng xác nhận vòng lặp.

## Ngoại lệ và lịch sử review

| Thời điểm | Anchor/mức/issue | Ngoại lệ hoặc mâu thuẫn | Ảnh hưởng chọn mẫu | Quyết định / người xác nhận / nguồn | Version mới hoặc review tiếp |
| --- | --- | --- | --- | --- | --- |

Ghi scope đổi, thiếu QA, hai field chênh lệch, thiếu lịch sử và tính không tương đồng. Loại anchor mâu thuẫn chưa rõ lý do hoặc ghi ambiguity; không tự sửa issue ngoài scope. Giữ version cũ để tra cứu; chỉ nâng quy tắc sau xác nhận phù hợp, không biến giả định một lần thành quy ước cho mọi board.
