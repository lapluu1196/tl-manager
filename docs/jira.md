# Jira Data Center và MCP

Integration dùng [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian), pin `0.23.1`, transport stdio. Jira Server/Data Center dùng `JIRA_PERSONAL_TOKEN`; không dùng mẫu email/API token của Jira Cloud.

## Setup

```bash
python3 scripts/workspace.py bootstrap
python3 scripts/credentials.py set-jira-token --url https://jira.example.com
python3 scripts/jira_check.py --discover
python3 scripts/setup_mcp.py
```

Token được nhập ẩn và lưu `.local/secrets.env`, quyền `0600` trên POSIX. Không truyền token sau tên lệnh. Không dùng `source .local/secrets.env`.

`jira_check.py` chỉ gửi GET để xác minh tài khoản và, với `--discover`, lấy metadata cần cấu hình. Kết quả discovery nằm ở `.local/jira-discovery.json`; stdout chỉ báo trạng thái/tổng số. Lỗi 401 thường do PAT hết hạn hoặc sai; 403 do quyền; lỗi DNS/timeout có thể cần VPN công ty. Với 404 ở Agile API, kiểm tra Jira Software/URL context path. Không coi login HTML/redirect là kết nối thành công.

`setup_mcp.py` tạo `.codex/config.toml` theo đường dẫn tuyệt đối trên máy hiện tại. File này bị Git bỏ qua. Không sửa `~/.codex/config.toml`. Nếu đã có entry Jira khác, xem diff và xử lý xung đột trước, không ghi đè cấu hình không liên quan.

Theo [OpenAI Docs](https://developers.openai.com/codex/mcp), cấu hình MCP project chỉ nạp khi project được trust. Chạy Codex từ root workspace, khởi động lại phiên rồi xem `/mcp`. Bootstrap đăng ký skill qua `.agents/skills/` theo [cơ chế discovery chính thức](https://developers.openai.com/codex/skills).

## Chọn board và mapping

Sửa `.local/workspace.json`, không sửa file example để lưu dữ liệu nội bộ. Tên board và project key không nhất thiết giống nhau; dùng ID từ discovery thay vì suy đoán.

```json
{
  "project_keys": ["EXAMPLE"],
  "board_id": 123,
  "boards": [
    {
      "name": "Example board",
      "board_id": 123,
      "project_keys": ["EXAMPLE"],
      "story_points_field": "customfield_10000",
      "sprint_field": "customfield_10001",
      "done_status_ids": [],
      "cancelled_status_ids": [],
      "mapping_confirmed": false
    }
  ]
}
```

Đây là minh họa phần `jira`, ID và project đều giả. Điền mapping thật sau discovery; các custom field không có ID cố định giữa các Jira instance. Board filter có thể bao gồm nhiều project hoặc chỉ một phần project. Khi lấy issue phải tôn trọng filter/phạm vi board, không chỉ `project = ...`.

Với mỗi board, xác nhận:

1. Sprint ID, thời gian bắt đầu/kết thúc, timezone và board filter.
2. Field estimate thực sự board đang dùng; có thể không phải story point.
3. Trạng thái được tính clear và điều kiện nghiệm thu/QA/release.
4. Trạng thái cancelled và cách xử lý ticket mở lại.
5. Issue type được tính SP, quy tắc parent/subtask và dữ liệu thiếu.

`resolution != null` hoặc status category Done một mình chưa đủ chứng minh đã đạt Definition of Done. Đối chiếu cấu hình board, workflow và team rồi đặt `mapping_confirmed: true`. Nếu chưa rõ, báo "chưa xác nhận" và không đưa ra tổng SP clear như số liệu chính thức.

## Cách đọc dữ liệu

- Bắt đầu bằng danh sách board, sprint và một issue mẫu; xác nhận response có field cần thiết trước khi tổng hợp.
- Lấy đủ trang kết quả. `maxResults`/limit không phải tổng số; ghi rõ nếu quyền truy cập hoặc giới hạn API làm thiếu dữ liệu.
- Luôn lưu `fetched_at`, `cutoff`, nguồn, JQL/phạm vi, field/status mapping cùng snapshot ở `private/`.
- Dùng changelog hoặc snapshot đúng thời điểm để tính cuối sprint. Trạng thái hiện tại không chứng minh trạng thái tại cutoff trong quá khứ.
- Dữ liệu nhiều board: khử trùng issue key khi làm báo cáo bộ phận; không cộng velocity của những team có thang estimate khác nhau.

Ví dụ JQL dưới đây dùng ID giả; thay bằng scope và mapping đã xác nhận:

```jql
sprint = 12345 ORDER BY Rank ASC
sprint = 12345 AND status NOT IN (10001, 10002) ORDER BY priority DESC
```

JQL hiện tại chỉ hỗ trợ lấy dữ liệu nguồn, không thay thế baseline hoặc lịch sử hoàn thành tại cutoff.

## Quyền và phiên bản

Launcher ép `READ_ONLY_MODE=true`, TLS verification và allowlist tool đọc. Credentials chỉ vào environment của tiến trình MCP, không nằm trong config Codex. Chỉ bật Jira, không tự bật Confluence hay auth khác từ environment có sẵn.

Khi cần write tools, tạo thay đổi cấu hình có review, thu hẹp quyền tài khoản và kiểm tra đúng các thao tác đã được leader yêu cầu. Không tắt read-only chỉ để hoàn thành báo cáo.

Thay version đồng bộ ở `config/integrations.json`, launcher và tests; kiểm tra release notes, dependencies và MCP initialize/tools trước khi dùng. Nguồn đối chiếu: [authentication](https://mcp-atlassian.soomiles.com/docs/authentication), [configuration](https://mcp-atlassian.soomiles.com/docs/configuration), [release v0.23.1](https://github.com/sooperset/mcp-atlassian/releases/tag/v0.23.1).

## Quy ước label và due date đề xuất

Team xác nhận danh mục trong `team-setup/output.md` trước khi áp dụng. Dùng chữ thường ASCII và gạch ngang, dạng `[a-z0-9]+(-[a-z0-9]+)*`; một ý nghĩa chỉ có một label chuẩn.

| Nhóm | Ví dụ giả | Quy tắc |
| --- | --- | --- |
| Mục tiêu | `goal-checkout` | Story trong cam kết liên kết ít nhất một goal; mapping goal có phiên bản theo sprint |
| Luồng sản phẩm | `stream-payments` | Chọn theo danh mục đã thống nhất; không dùng tên người |
| Loại công việc | `type-feature`, `type-tech-debt`, `type-support` | Một giá trị chính; nếu Issue Type đã thể hiện đủ thì không tạo label trùng |
| Rủi ro | `risk-dependency`, `risk-capacity` | Chỉ gắn khi có evidence và owner theo dõi; gỡ khi rủi ro được xử lý theo quyền được giao |

Không dùng label thay field Sprint, Assignee, Priority hoặc Status. Giữ label ngoài danh mục nếu chưa xác minh ý nghĩa; đề xuất mapping label cũ → mới và liệt kê diff trước khi sửa, không xóa hàng loạt.

Due date của story là ngày cần clear theo DoD; các mốc BA bàn giao, Dev hoàn tất và QA/retest nằm riêng trong kế hoạch. Deadline mục tiêu phải chừa thời gian tích hợp/nghiệm thu. Jira date field thường chỉ có ngày: ghi rõ timezone và giờ cutoff trong baseline, không tự suy ra từ UTC. Thay deadline sau khi chốt phải có lý do, người quyết định và ảnh hưởng trong change log.
