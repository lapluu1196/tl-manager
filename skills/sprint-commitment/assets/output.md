# Kết quả: Cam kết và baseline sprint

| Thông tin | Giá trị |
| --- | --- |
| Sprint / board / khoảng thời gian / múi giờ | |
| Trạng thái: nháp hoặc đã chốt | |
| Phiên bản / đường dẫn bản baseline bất biến | |
| baseline_at / locked_at / người xác nhận | |
| Nguồn / fetched_at / phân trang | |
| SP baseline đã biết C / số issue thiếu estimate | |
| SP team trên Story/Bug / mapping hai trường SP / DoD | |

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

## Baseline từng issue

| Issue key | SP baseline | Goal | BA / Dev / QA owner | Due date baseline | Label baseline | Status lúc chốt | Bằng chứng |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

## Baseline mục tiêu

| Goal | Acceptance đã thống nhất | Due date | Người nghiệm thu | Điều kiện / rủi ro được chấp nhận |
| --- | --- | --- | --- | --- |
| | | | | |

## Dữ liệu thiếu và giới hạn cam kết

| Nội dung | Ảnh hưởng số liệu / cam kết | Người bổ sung | Hạn |
| --- | --- | --- | --- |
| | | | |

## Change log sau baseline_at

Bảng làm việc này nằm ngoài bản baseline đã chốt. Có thể lưu riêng `change-log.md`; mỗi sự kiện là một dòng mới.

| Event ID | Thời điểm | Issue / goal | Loại thay đổi | Trước | Sau | Lý do / bằng chứng | Người đề nghị / quyết định | Ảnh hưởng mục tiêu / workload |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

## Bàn giao

| Đầu việc | Artifact cần đọc | Owner / thời điểm |
| --- | --- | --- |
| daily-risk | Baseline và change log | |
| sprint-review | Baseline, mapping, DoD và change log | |

## Tự phát triển workflow

| Quy ước đã xác nhận / bài học có bằng chứng | Skill / docs / template đã cập nhật | Kiểm tra / kết quả | Đề xuất còn chờ xác nhận |
| --- | --- | --- | --- |
| | | | |

Nếu không có điều mới để cập nhật, ghi kết quả rà soát và lý do. Không chép dữ liệu nội bộ vào tài liệu chung.
