# Kết quả: Kế hoạch sprint

| Thông tin | Giá trị |
| --- | --- |
| Sprint / khoảng thời gian / múi giờ | |
| Board / project / filter đã chọn | |
| Tạo lúc / nguồn và thời điểm dữ liệu | |
| Trạng thái: nháp hoặc sẵn sàng chốt | |
| Tổng SP đã biết / số issue chưa estimate | |
| Quy ước DoR / DoD áp dụng | |

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

## Mục tiêu đề xuất

| Goal | Ưu tiên | Tiêu chí acceptance | Issue liên quan | Owner điều phối / người nghiệm thu | Due date | Rủi ro |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Phân công và lịch bàn giao

| Issue | SP | BA owner / hạn đầu vào | Dev owner / hạn bàn giao | QA owner / hạn test và retest | Due date clear | Dependency | Label đề xuất | DoR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## Kiểm tra workload

| Vai trò / người | Capacity khả dụng | Nhu cầu cùng đơn vị | Phần dư / thiếu | Tỷ lệ tải hoặc N/A | Nút thắt theo ngày | Điều chỉnh |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Scope hoãn và quyết định

| Issue / quyết định | Lý do / bằng chứng | Phương án | Người chốt | Hạn |
| --- | --- | --- | --- | --- |
| | | | | |

## Bàn giao commitment

| Điều kiện còn thiếu | Owner | Hạn | Ảnh hưởng nếu chưa có |
| --- | --- | --- | --- |
| | | | |

Thay đổi Jira đề xuất/đã thực hiện theo quyền được giao, kèm nguồn xác minh:

## Tự phát triển workflow

| Quy ước đã xác nhận / bài học có bằng chứng | Skill / docs / template đã cập nhật | Kiểm tra / kết quả | Đề xuất còn chờ xác nhận |
| --- | --- | --- | --- |
| | | | |

Nếu không có điều mới để cập nhật, ghi kết quả rà soát và lý do. Không chép dữ liệu nội bộ vào tài liệu chung.
