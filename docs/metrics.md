# Quy ước đo lường sprint

Áp dụng cùng một quy ước cho planning, commitment, daily, review và đánh giá cá nhân. Các trường Jira thực tế được xác nhận trong `.local/workspace.json`; `config/workspace.example.json` chỉ là mẫu, không phải mapping đã được xác minh.

## Thời điểm và bằng chứng

- Ghi sprint ID, thời gian bắt đầu/kết thúc, mốc đo baseline `baseline_at`, thời điểm xác nhận cam kết `locked_at`, thời điểm cắt số liệu `cutoff_at` và thời điểm lấy dữ liệu `fetched_at`. Dùng ISO 8601 kèm múi giờ, ví dụ `2026-10-26T09:00:00+07:00`.
- Phân biệt trạng thái **tại cutoff** với trạng thái hiện tại. Dùng changelog/snapshot nếu lấy dữ liệu sau cutoff. Không có lịch sử thì ghi `không xác định tại cutoff` và giới hạn kết luận.
- Mỗi kết quả có nguồn Jira/JQL, bộ lọc, ID trường, phạm vi truy xuất, thời gian và trạng thái phân trang đầy đủ. Không ghi token hoặc header xác thực vào báo cáo.
- Issue key là khóa chống đếm trùng. Lưu bằng chứng được phép truy cập vào `private/`; liên kết công khai của workspace không chứa dữ liệu nội bộ.

## Nhiều board trong một bộ phận

Mỗi sprint phải chọn board và project/filter tương ứng từ danh sách `jira.boards` trong cấu hình local; `jira.board_id` mặc định chỉ dùng khi đã xác nhận đúng phạm vi. Board có thể dùng mapping SP, Done, DoD hoặc thang estimate khác nhau: ghi quy ước theo board trước khi so sánh.

Filter nhiều board có thể chứa cùng issue. Khi tổng hợp bộ phận, khử trùng theo issue key; không cộng lại SP của một issue chỉ vì nó xuất hiện trên nhiều board. Chỉ định board sở hữu dùng cho baseline/mapping khi có giao nhau và ghi rõ cách phân bổ. Nếu SP/DoD giữa các board không so sánh được, trình bày kết quả riêng từng board; không công bố một velocity gộp như thể chúng cùng hệ đo.

## Clear, resolve và mục tiêu

`Resolved` không mặc nhiên là `clear`. Một issue được clear khi đồng thời: trạng thái tại cutoff thuộc `done_status_ids` đã xác minh; đạt Definition of Done; có bằng chứng acceptance/QA và điều kiện phát hành theo quy ước của team. Trạng thái hủy trong `cancelled_status_ids` không phải giao hàng thành công.

Issue thiếu bằng chứng DoD có thể báo riêng là `resolved, chưa xác nhận clear`. Một issue từng Done rồi reopened trước cutoff được xem là chưa clear nếu chưa đạt lại DoD trước cutoff. Reopened sau cutoff được ghi thành thông tin chất lượng sau sprint, không âm thầm viết lại báo cáo đã chốt.

Mục tiêu có tiêu chí nghiệm thu, người xác nhận và due date riêng. Tỷ lệ SP hoàn tất không thay thế mức đạt mục tiêu. Một mục tiêu chỉ `đạt` khi có bằng chứng nghiệm thu; dùng `đạt một phần`, `không đạt` hoặc `chưa đủ dữ liệu` khi phù hợp. Nếu có trọng số mục tiêu, chốt trước sprint; không thêm trọng số sau khi đã biết kết quả.

## Tổng hợp planning và cam kết đầu sprint

Khi tổng hợp SP đầu sprint, dùng mốc `sprint_started_at` thực tế trên Jira và trạng thái **ngay sau sự kiện start** (`cutoff_at` của baseline đầu sprint). Ghi `baseline_at` là mốc đo này; giữ riêng `locked_at` là lúc xác nhận/lưu bản chốt và `fetched_at` là lúc lấy dữ liệu; không lấy hai mốc này thay cho mốc start. Nếu chưa start, chỉ xuất planning draft theo snapshot hiện tại, chưa có SP đầu sprint hoặc baseline đầu sprint. Planning draft vẫn được báo SP dự kiến khi đủ bằng chứng, ghi rõ đó là estimate hiện tại.

Đối chiếu thời điểm kích hoạt sprint (`activatedDate` nếu API cung cấp) với `startDate` được cấu hình; hai mốc có thể khác nhau. Ghi cả hai và nguồn, kiểm tra thay đổi scope/SP/QA trong khoảng chênh lệch trước khi kết luận; không âm thầm dùng ngày dự kiến hoặc ngày đã chỉnh sửa thay sự kiện start thực tế.

- Phạm vi tổng hợp là **Bug + Story**; SP trên chính Story/Bug là điểm của cả team Dev + QA, không phải điểm cá nhân. Loại issue Designer/BA riêng; không chia SP parent theo assignee, không cộng SP task/subtask vào parent. Xác minh issue type và membership tại mốc đo.
- Tất cả board dùng **Original story points** ưu tiên. Nếu trường này `null` hoặc không có giá trị thì fallback **Story Points**. Original bằng **0** là giá trị hợp lệ, không fallback. Cả hai thiếu thì ghi `chưa estimate`, không ghi 0. Mapping field ID thực tế giữ trong `.local/`; không lấy trường estimate mặc định của board thay quy tắc team. Truy xuất đủ cả hai trường: không đánh đồng lỗi quyền/truy xuất với giá trị rỗng.
- Mỗi dòng issue lưu hai giá trị gốc tại mốc đo, SP được chọn, tên trường nguồn, lý do fallback nếu có và bằng chứng snapshot/changelog. Áp dụng cùng thứ tự field khi đo baseline, lúc nhận thêm và hiện tại; không lấy giá trị mới điền ngược vào lịch sử.
- Tách **tổng SP Bug + Story đầu sprint** khỏi **SP cam kết clear**. Bug trong scope đầu sprint tự thuộc cam kết phải clear, không cần task QA. Story có task QA đã bóc tại mốc đầu sprint là tín hiệu thuộc cam kết clear; task QA phải thuộc **chính sprint đang tính**, có liên kết/subtask tới Story tại `baseline_at`, và có bằng chứng vai trò QA. Task QA của sprint trước không đủ. Story chưa có bằng chứng hợp lệ được báo riêng, không âm thầm đưa vào cam kết clear.
- Task QA đã bóc là căn cứ **cam kết sẽ clear**, không phải bằng chứng đã clear thực tế. Kết quả clear vẫn theo DoD/acceptance và trạng thái tại cutoff đánh giá. Task Done riêng lẻ không đủ để kết luận Story clear. Task QA mới được tạo, đưa vào sprint hoặc liên kết sau start phải vào change log, không viết ngược vào baseline đầu sprint.
- Khi tái dựng sau start, cần lịch sử đủ để xác định membership sprint, estimate, role/link và task QA tại mốc đầu sprint, gồm cả issue/task đã removed sau đó. Snapshot hiện tại hoặc danh sách issue hiện còn trong sprint không đủ để chứng minh baseline quá khứ. Ghi nguồn lịch sử, mức đầy đủ và giới hạn; thiếu dữ liệu thì giữ trạng thái chưa xác minh.

## Baseline và scope thay đổi

- Baseline là tập issue được cam kết tại `baseline_at`, với SP tại cùng mốc. Với tổng hợp đầu sprint, đó là ngay sau sprint start; với quy ước chốt khác phải ghi rõ mốc đã được xác nhận. `locked_at` là lúc xác nhận/lưu bản chốt, có thể muộn hơn `baseline_at`. Giữ bản chốt bất biến; sửa sai bằng bản đính chính có lý do và tham chiếu bản gốc.
- `B`: tập issue thuộc baseline. `C`: tổng SP **đã biết** của B tại `baseline_at`. Báo cả số issue thiếu estimate trong B; thiếu estimate không tương đương 0 SP.
- `D`: tổng SP baseline **đã biết tại baseline_at** của những issue trong B đạt clear tại cutoff. Issue clear thiếu SP baseline được đếm riêng, không cộng vào D như 0 SP. Chỉ tính một lần mỗi issue; không dùng SP hiện tại để thay thế SP baseline.
- `U = C - D`: SP baseline đã biết chưa clear. Phân loại nguyên nhân và cờ removed/reopened; không cộng các cờ này như những tập loại trừ nhau.
- Tỷ lệ hoàn thành cam kết là `D / C × 100%` khi C > 0 và baseline có đủ estimate. Nếu thiếu estimate, chỉ báo tỷ lệ trên phần đã biết, gắn `chưa đầy đủ`, kèm số issue còn thiếu. Nếu C = 0, ghi `N/A`, không ghi 0% hoặc 100%.
- Issue bị removed sau `baseline_at` vẫn nằm trong B và mẫu số C. Ghi lý do/ai quyết định; không biến scope bị bỏ thành clear. Nếu issue removed vẫn thỏa đầy đủ định nghĩa clear tại cutoff, SP baseline đã biết của nó được tính vào D như mọi issue khác trong B; cờ removed chỉ ghi lại thay đổi scope. Nếu không thỏa hoặc thiếu bằng chứng, không tính vào D. Áp dụng cùng quy tắc cho mọi issue, không lựa chọn sau khi biết kết quả.
- Issue thêm sau `baseline_at` thuộc scope added, báo riêng estimate tại thời điểm được nhận thêm. Không tăng C. Issue vừa added rồi removed vẫn giữ cả hai sự kiện trong log.
- Thay đổi SP sau `baseline_at` chỉ ảnh hưởng báo cáo estimate hiện tại. Ghi SP trước/sau và lý do, không cải thiện lại tỷ lệ cam kết bằng cách giảm estimate.
- Log scope có issue key, thời điểm, loại thay đổi, giá trị trước/sau, lý do, người đề nghị và người quyết định. Nếu tái lập baseline theo quyết định chính thức, vẫn báo kết quả theo baseline gốc và bản mới riêng biệt.

## Khối lượng giao thực tế và tránh đếm trùng

Khối lượng giao theo estimate đã chốt = D + SP tại lúc nhận thêm của các issue added đã clear. Tách rõ hai thành phần. Nếu baseline hoặc added có issue clear nhưng thiếu estimate tại thời điểm tương ứng, tổng này chỉ là phần SP đã biết: gắn `chưa đầy đủ` và báo riêng số issue clear chưa có estimate. Không lấy estimate bổ sung sau đó giả làm estimate đã biết lúc chốt. Có thể báo thêm tổng SP hiện tại của issue clear, nhưng phải đặt tên khác và chỉ rõ thời điểm estimate; không so hai hệ đo như một chuỗi velocity.

Tính SP trên **Story/Bug** theo quy tắc field ở trên; không cộng đồng thời SP parent và task/subtask. Epic, mục tiêu và nhóm label là chiều phân loại, không phải SP bổ sung. Một issue đóng góp nhiều mục tiêu vẫn chỉ xuất hiện một lần trong tổng team. Khi báo SP theo mục tiêu, đánh dấu phần giao nhau hoặc có một quy tắc phân bổ đã chốt.

Ví dụ với dữ liệu đủ: C = 20 SP, D = 13 SP, U = 7 SP, trong U có 5 SP removed. Added đã clear = 2 SP. Hoàn thành cam kết = 65%; giao thực tế theo estimate đã chốt = 15 SP. Không giảm mẫu số xuống 15 vì removed và không dùng 15/20 làm tỷ lệ hoàn thành cam kết.

## Capacity và workload BA / Dev / QA

Capacity theo từng người/vai trò = thời gian làm việc trong sprint - nghỉ lễ/phép - việc cố định/được phân bổ ngoài sprint - phần dự phòng. Xác nhận đơn vị giờ hoặc ngày và cách trừ; không trừ cùng một phần hai lần. Hai tuần lịch không mặc nhiên là 10 ngày làm việc: dùng `working_days`, lịch nghỉ và ngày bắt đầu/kết thúc thực tế.

Buffer mặc định tham khảo `planning.capacity_buffer_percent`, điều chỉnh có lý do trước khi chốt. Một người kiêm nhiều vai trò phải chia capacity, tổng không vượt thời gian có thật. Workload theo vai trò chỉ so với capacity khi cùng đơn vị. Tỷ lệ tải = nhu cầu / capacity; capacity bằng 0 thì báo `N/A` và cảnh báo nếu nhu cầu > 0.

SP đo độ lớn tương đối của công việc theo quy ước của team; không quy đổi máy móc sang giờ, không chia SP story thành điểm sản lượng từng BA/Dev/QA. SP Story/Bug đã đại diện cả team Dev + QA; không phân bổ số này thành thước đo sản lượng cá nhân. Dùng phần việc, effort dự kiến cùng đơn vị, lịch phụ thuộc và WIP để phát hiện QA dồn cuối sprint hoặc BA thiếu đầu vào.

## Đọc xu hướng và trách nhiệm

Velocity chỉ có ý nghĩa khi cùng team, cách estimate, cấp issue, DoD và độ dài sprint. Ghi thay đổi nhân sự, capacity, scope và gián đoạn trước khi so sánh; dùng nhiều sprint, không suy luận từ một điểm. Velocity là tín hiệu lập kế hoạch, không phải chỉ tiêu bắt buộc tăng.

Đánh giá cá nhân dựa trên cam kết cụ thể, chất lượng, báo rủi ro đúng lúc, phối hợp, hỗ trợ và bằng chứng tác động. Phân biệt yếu tố cá nhân kiểm soát được với quyết định scope, phụ thuộc, thiếu capacity hoặc yêu cầu đổi của hệ thống. Issue assignee không chứng minh toàn bộ công lao hoặc lỗi thuộc về người đó. Không xếp hạng BA/Dev/QA bằng SP, số bug thô hoặc số issue đóng.

Kết luận trách nhiệm cần chuỗi bằng chứng: kỳ vọng được thống nhất → hành động/sự kiện → tác động xác minh được → cơ hội hỗ trợ/cảnh báo → phản hồi của người liên quan. Thiếu mắt xích thì ghi giả thuyết hoặc chưa kết luận. Ghi mức trách nhiệm, hành động cải thiện, hỗ trợ của leader và ngày kiểm tra; cho phép bổ sung hoặc phản hồi bằng chứng.
