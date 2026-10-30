# Kết nối Google Workspace

Workspace dùng OAuth 2.0 để đăng nhập tài khoản Google và gọi API qua [Google Workspace CLI](https://github.com/googleworkspace/cli/tree/v0.22.5), pin `@googleworkspace/cli@0.22.5`. Công cụ được phát triển trong repository googleworkspace, chưa phải sản phẩm được Google hỗ trợ chính thức.

Workspace dùng Sheets phục vụ [đánh giá năng lực AI](../skills/ai-capability-review/SKILL.md) và [báo cáo tập trung cho quản lý](../skills/management-reporting/SKILL.md). Hai đầu việc có đối tượng xem khác nhau; không tự gộp dữ liệu vào cùng một file. Có thể thêm Drive, Docs, Calendar và Gmail theo nhu cầu. Chỉ cấp scope cho ứng dụng đang dùng.

## 1. Tạo OAuth client trên Google Cloud

Trong [Google Cloud Console](https://console.cloud.google.com/):

1. Chọn project được công ty cho phép sử dụng, hoặc tạo project riêng nếu bạn có quyền.
2. **APIs & Services → Library**: bật **Google Sheets API**. Khi cần tìm file hoặc quản lý chia sẻ trong Drive, bật thêm **Google Drive API**.
3. **Google Auth Platform → Branding / Audience**: cấu hình tên app, ví dụ `TL Manager`. Dùng Internal nếu phù hợp tổ chức; nếu External/Testing, thêm tài khoản đăng nhập vào **Test users**.
4. **Clients → Create client → Desktop app**: tạo client. Nếu giao diện có lựa chọn client dùng cho AI agent, chọn đúng mục đích sử dụng.
5. Download JSON client. Lưu file vào `.local/google/client_secret.json` trên máy; không gửi nội dung file vào chat, không commit lên Git.

Đây là file định danh ứng dụng OAuth, chưa phải phiên đăng nhập. Người dùng vẫn phải mở trình duyệt và duyệt quyền. Không dùng API key để sửa một Sheet riêng tư.

## 2. Đăng nhập trên máy làm việc

Chạy từ root workspace. Cần Node.js 18+ và npm; không bắt buộc cài gcloud cho quy trình tạo client thủ công ở trên.

```bash
python3 scripts/workspace.py bootstrap
mkdir -p .local/google
chmod 700 .local/google
# Copy JSON đã tải về thành .local/google/client_secret.json trước bước tiếp theo.
chmod 600 .local/google/client_secret.json
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR="$PWD/.local/google"
npx --yes @googleworkspace/cli@0.22.5 auth login --scopes https://www.googleapis.com/auth/spreadsheets
npx --yes @googleworkspace/cli@0.22.5 auth status
```

Mở URL đăng nhập do công cụ cung cấp, chọn đúng tài khoản và kiểm tra quyền trước khi đồng ý. Tài khoản phải có quyền Editor trên Sheet để cập nhật. Lệnh này không thay đổi nội dung Sheet.

`GOOGLE_WORKSPACE_CLI_CONFIG_DIR` phải được đặt trong terminal chạy lệnh. Với các phiên terminal/tool độc lập, truyền biến này mỗi lần chạy; không giả định `export` ở một tiến trình sẽ tồn tại trong tiến trình khác. Codex có thể truyền biến này khi thực thi CLI, không cần đưa token vào `.codex/config.toml`.

Login dùng callback localhost. Trình duyệt và CLI cần chạy trên cùng máy; nếu chạy CLI qua SSH, cần cấu hình port forwarding phù hợp callback thực tế. Bản 0.22.5 không có cờ `--no-browser` hoặc `--port` cho login.

## 3. Kiểm tra Sheet đã có

Với link `https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit?gid=<SHEET_ID>`, ID sau `/d/` là file; `gid` là tab. Đọc metadata trước để xác định đúng tab:

```bash
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR="$PWD/.local/google"
npx --yes @googleworkspace/cli@0.22.5 sheets spreadsheets get \
  --params '{"spreadsheetId":"SPREADSHEET_ID","fields":"spreadsheetId,sheets.properties"}'
```

Thay ID giả bằng ID thật. Kết quả metadata có thể chứa tên tab nội bộ; không chép lên Git public. Cấu hình file đang làm có thể lưu trong `.local/google-workspace.json`.

Khi đã xác thực, yêu cầu cụ thể ví dụ: “Đọc tab đã chỉ định, tạo bảng đánh giá AI theo L1–L5, giữ dữ liệu cũ và để trống điểm cá nhân.” Đọc vùng hiện có và xác định phạm vi trước khi cập nhật; không ghi đè cả workbook để tạo mẫu.

## Báo cáo tập trung cho quản lý

Dùng [management-reporting](../skills/management-reporting/SKILL.md) cho một file Google Sheet có link ổn định, tab Tổng quan và các tab/snapshot theo sprint. Manager xem số liệu, giới hạn dữ liệu và quyết định cần xử lý trên Sheet; Markdown và raw vẫn lưu private để truy nguyên. Mỗi lần cập nhật giữ lại lịch sử công bố, baseline đã khóa và ghi chú của manager. Không đưa đường dẫn file cục bộ lên Sheet; dùng link Jira/nguồn trực tuyến có quyền truy cập phù hợp.

Lưu file đã chọn trong `.local/google-workspace.json` dưới khóa `management_reporting`, tách khỏi cấu hình file đánh giá AI. Cấu hình này chứa `spreadsheet_id`, URL, tab Tổng quan, vị trí lịch sử snapshot, vùng do hệ thống quản lý và quyền chia sẻ đã xác minh; không lưu token tại đây. Hồ sơ công việc trong `private/` giữ snapshot ID, cutoff, diff và kết quả xác minh. File ID và URL thực tế không đưa vào mẫu public.

Tạo file mới và thay quyền chia sẻ là các hành động riêng, phải nằm trong yêu cầu đã được người dùng cho phép. Nếu người dùng yêu cầu “ai có link có thể view và comment”, đặt quyền Drive trên đúng file là `type=anyone`, `role=commenter` (không phải editor), rồi đọc lại permissions để xác minh. Không gửi email/thông báo cho người khác nếu chưa được yêu cầu. Quyền qua link áp dụng cho toàn bộ file, gồm cả các tab; không thể dùng tab ẩn để bảo vệ đánh giá nhân sự. Tổ chức có thể chặn chia sẻ qua link; báo giới hạn thực tế nếu bị chặn, không tự đổi chính sách hoặc báo chia sẻ thành công.

Với file do app tạo, quyền chia sẻ cần **Google Drive API** và scope `drive.file` bên cạnh scope Sheets. Khi có nhu cầu này, người dùng đăng nhập lại để duyệt đúng hai scope:

```bash
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR="$PWD/.local/google"
npx --yes @googleworkspace/cli@0.22.5 auth login \
  --scopes https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/drive.file
```

Chỉ thêm `drive.file` khi cần, không dùng Drive full. Nếu đang dùng các scope khác cho đầu việc đã được phép, giữ tập scope cần thiết khi login lại. `drive.file` quản lý các file app đã tạo hoặc được cấp truy cập; chỉ dán URL của một file có sẵn chưa tự cấp truy cập Drive cho app. Nếu token hiện tại thiếu scope, chuẩn bị nội dung/diff cục bộ, hướng dẫn người dùng duyệt Google consent rồi tiếp tục trong phạm vi đã được ủy quyền; không yêu cầu nhập token vào chat. Không coi đăng nhập thành công là bằng chứng file đã được chia sẻ.

Khi cập nhật: đọc metadata và đúng range hiện có, so sánh diff, ghi đúng vùng đã định rồi đọc lại. Không ghi đè workbook hoặc baseline để thay mẫu. Mỗi lần công bố dùng snapshot ID mới; Tổng quan trỏ tới bản phù hợp mới nhất, còn lịch sử giữ bản cũ. Nếu lệnh lỗi hoặc timeout, kiểm tra file/tab/snapshot đã tồn tại trước khi thử lại để tránh tạo trùng.

## Quyền cho ứng dụng khác

### Đọc SRS/module tài liệu trong Drive

Link folder không tự cấp quyền cho OAuth app. Phiên có Sheets scope có thể đọc Sheet nhưng vẫn nhận `403 insufficientPermissions` khi gọi Drive list/export. Phân biệt lỗi thiếu scope này với tài khoản chưa được chia sẻ folder; sau khi đủ scope vẫn phải kiểm tra quyền trên đúng nguồn.

Với tài liệu có sẵn, scope `drive.metadata.readonly` chỉ giúp tìm metadata, chưa đủ đọc/export nội dung. `drive.file` cũng không tự cho phép đọc mọi file chỉ vì đã dán URL. Khi cần list, tải hoặc export SRS từ folder được tài khoản truy cập, dùng `https://www.googleapis.com/auth/drive.readonly` nếu phù hợp chính sách công ty; scope này đọc được các file Drive tài khoản có quyền, không giới hạn trong một folder. Người dùng phải duyệt Google consent; không tự thay phiên đăng nhập để mở rộng scope.

Nếu người dùng chọn cấp quyền này, giữ các scope đang cần cho đầu việc hiện có khi đăng nhập lại. Ví dụ phiên đang dùng Sheets và cần thêm đọc Drive:

```bash
export GOOGLE_WORKSPACE_CLI_CONFIG_DIR="$PWD/.local/google"
npx --yes @googleworkspace/cli@0.22.5 auth login \
  --scopes https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/drive.readonly
```

Đây là bước người dùng đăng nhập và duyệt quyền, không phải thao tác sửa tài liệu hay chia sẻ file. Sau consent, kiểm tra auth status và một lệnh list/get chỉ đọc trên đúng folder; không ghi token vào chat/log. Nếu chưa cấp quyền, ghi nguồn `chưa đọc do quyền`; tiếp tục phần code/Jira độc lập hoặc dùng bản SRS cục bộ đã được cung cấp. Với SRS lớn có module tách, đọc module liên quan trước và giữ file ID/modified time làm provenance trong hồ sơ private.

| Nhu cầu | API / scope cần xem xét |
| --- | --- |
| Đọc/sửa Sheet được tài khoản truy cập | Sheets API / `https://www.googleapis.com/auth/spreadsheets` |
| Quản lý chia sẻ file do app tạo hoặc được cấp truy cập | Drive API / `https://www.googleapis.com/auth/drive.file` |
| Tìm file theo tên/metadata | Drive API / `https://www.googleapis.com/auth/drive.metadata.readonly` |
| Tạo/sửa Docs | Docs API / `https://www.googleapis.com/auth/documents` |
| Đọc lịch | Calendar API / `https://www.googleapis.com/auth/calendar.readonly` |
| Đọc email | Gmail API / `https://www.googleapis.com/auth/gmail.readonly` |

Thêm scope khi có nhu cầu thực tế rồi login lại với tập scope cần giữ. Ví dụ Sheets + metadata Drive:

```bash
npx --yes @googleworkspace/cli@0.22.5 auth login \
  --scopes https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/drive.metadata.readonly
```

`--scopes` nhận URL đầy đủ, phân tách bằng dấu phẩy. `-s sheets,drive` chỉ giới hạn danh sách scope trong trình chọn tương tác, không tương đương tập scope tối thiểu. Tránh `--full` khi không cần.

Scope `spreadsheets` áp dụng cho tất cả file Sheet tài khoản được phép truy cập, không giới hạn ở `gid` hoặc một file duy nhất. Link không tự cấp quyền. `drive.file` chỉ áp dụng cho các file app được cấp truy cập; chỉ dán URL của file có sẵn chưa tự cấp quyền đó. Nếu chỉ muốn ứng dụng được truy cập một vài file cố định, có thể dùng service account và share từng file cho email service account, theo chính sách công ty.

Scope và quyền Google không thay thế phạm vi công việc: đọc email không cho phép gửi; đánh giá AI trên một Sheet không cho phép sửa file khác hoặc chia sẻ cho người khác.

## MCP và nhiều máy

Phiên bản CLI 0.22.5 đang dùng không cung cấp lệnh `gws mcp`; không cấu hình lệnh đó làm MCP stdio. Codex thao tác qua CLI bằng công cụ terminal. [MCP Sheets chính thức](https://developers.google.com/workspace/sheets/api/guides/configure-mcp-server) hiện có điều kiện Developer Preview, cần cấu hình OAuth/client riêng; chỉ bật sau khi xác nhận tổ chức đủ điều kiện và client tương thích.

Trên máy mới: clone repo, đặt client JSON ở thư mục private, đặt `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` và login lại. Không đồng bộ thư mục chứa refresh token/keys qua repo public; không export token vào chat để chuyển máy. Ghi chú lỗi đăng nhập theo loại, không in access token/refresh token.

Nếu thiếu Test users hoặc bị `admin_policy_enforced`, xử lý tại OAuth app/quản trị viên Workspace. External/Testing có thể cần đăng nhập lại do hạn dùng refresh token; không tự chuyển app sang Production hay mở rộng quyền để vượt chính sách.

Nguồn: [credentials của Google](https://developers.google.com/workspace/guides/create-credentials), [Sheets scopes](https://developers.google.com/workspace/sheets/api/scopes), [OAuth Desktop](https://developers.google.com/identity/protocols/oauth2/native-app), [CLI v0.22.5](https://github.com/googleworkspace/cli/blob/v0.22.5/README.md).
