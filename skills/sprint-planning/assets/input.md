# Đầu vào: Planning sprint

| Thông tin | Giá trị |
| --- | --- |
| Sprint / ngày bắt đầu và kết thúc / múi giờ | |
| Board / project / filter đã chọn | |
| Nguồn capacity team-setup / thời điểm xác nhận | |
| Snapshot Jira / JQL / fetched_at | |
| Phân trang dữ liệu đã đủ? | |
| DoR / DoD / cấp issue tính SP | |
| Velocity tham khảo / sprint tương đồng / giới hạn so sánh | |
| Đơn vị effort theo vai trò | |

## Phạm vi và bằng chứng đầu sprint

Áp dụng `docs/metrics.md`, mục “Tổng hợp planning và cam kết đầu sprint”. Sprint chưa start chỉ ghi planning draft; không điền số hiện tại như baseline đầu sprint.

| Thông tin | Giá trị / nguồn xác minh |
| --- | --- |
| Trạng thái sprint / start thực tế / baseline_at ngay sau start | |
| locked_at xác nhận (nếu có) / cutoff_at / fetched_at | |
| Issue type Bug + Story / SP team trên parent / mapping Original story points và Story Points | |
| Cách nhận diện và loại issue Designer/BA riêng | |
| Lịch sử membership, estimate, role/link và task QA / bao phủ removed / giới hạn | |
| Board sở hữu / khử trùng issue key giữa các board | |
| Tổng SP team Bug + Story đầu sprint đã biết / số chưa estimate hoặc chưa xác minh | |
| SP cam kết clear đã biết / số thiếu estimate hoặc chưa đủ bằng chứng | |

SP trên Story/Bug là điểm cả team Dev + QA. Ưu tiên Original story points; chỉ fallback Story Points khi Original null/không có; Original=0 hợp lệ, cả hai thiếu là chưa estimate. Không cộng task/subtask hoặc dùng field mặc định board thay quy tắc team.

Bug trong scope đầu sprint tự thuộc cam kết clear. Story cần task QA thuộc chính sprint đang tính và có liên kết/subtask tới Story tại baseline_at; task QA sprint trước không đủ. Tách cam kết sẽ clear khỏi kết quả clear thực tế theo DoD.

| Bug / Story key | Original story points tại baseline_at | Story Points tại baseline_at | SP chọn / trường nguồn / lý do fallback | Bằng chứng estimate / scope tại baseline_at | Task QA / sprint / liên kết và bằng chứng tại baseline_at | Thuộc cam kết clear? / căn cứ hoặc phần chưa xác minh |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Mục tiêu và ưu tiên

| Goal ID | Kết quả mong muốn | Tiêu chí acceptance | Ưu tiên / lý do | Due date | Người nghiệm thu |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Backlog ứng viên

Không có estimate thì ghi `chưa estimate`, không ghi 0.

| Issue / nguồn | Goal | AC / DoR | SP team / trường nguồn / người estimate | BA owner / effort | Dev owner / effort | QA owner / effort | Dependency / ngày sẵn sàng | Label hiện tại |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## Giới hạn và quyết định chờ

| Giới hạn / dữ liệu thiếu | Nguồn / thời điểm | Tác động | Người xử lý / hạn |
| --- | --- | --- | --- |
| | | | |

Phạm vi đã cho phép thay đổi Jira, nếu có:

## Yêu cầu cho trợ lý

Lập kế hoạch theo ưu tiên và capacity; nêu các story nên tách hoặc hoãn, rủi ro từng mục tiêu và quyết định cần chốt trước cam kết. Phân biệt dữ kiện với giả định.
