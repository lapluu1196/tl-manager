# Đầu vào: Cam kết sprint

| Thông tin | Giá trị |
| --- | --- |
| Sprint / board / khoảng thời gian / múi giờ | |
| Kế hoạch và capacity đã xác nhận tại | |
| Người có quyền chốt / xác nhận | |
| baseline_at đo SP / locked_at xác nhận dự kiến | |
| Snapshot / JQL / fetched_at / phân trang đầy đủ | |
| Original story points ưu tiên / Story Points fallback / SP trên Story/Bug | |
| Status Done / hủy / DoD | |
| Bản baseline trước đó nếu có | |

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

## Scope xin chốt

| Issue key / nguồn | SP tại baseline_at | Goal | BA owner | Dev owner | QA owner | Due date | Label | Status | DoR / điểm chưa rõ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | | |

## Cam kết mục tiêu

| Goal | Tiêu chí acceptance | Due date | Người nghiệm thu | Phụ thuộc / điều kiện cam kết |
| --- | --- | --- | --- | --- |
| | | | | |

## Chấp nhận rủi ro hoặc dữ liệu còn thiếu

| Nội dung | Ảnh hưởng | Người quyết định | Quyết định / lúc xác nhận |
| --- | --- | --- | --- |
| | | | |

## Yêu cầu cho trợ lý

Đối chiếu scope với planning, đóng băng estimate tại baseline_at và chỉ ra khác biệt; không thay số thiếu bằng 0 hoặc dùng dữ liệu hiện tại giả làm dữ liệu tại lúc chốt.
