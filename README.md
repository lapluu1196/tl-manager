# TL Manager

Workspace quản lý bộ phận BA, Dev và QA theo sprint 2 tuần. Mỗi đầu việc có hướng dẫn, input và output riêng để làm cùng AI hoặc điền thủ công.

**Bắt đầu ở [INDEX.md](INDEX.md)**: chỉ mục tất cả đầu việc và prompt tương ứng.

## Cách làm việc

1. **Thiết lập team**: capacity theo vai trò, lịch nghỉ, quy ước Jira và Definition of Done.
2. **Planning**: mục tiêu, estimate, dependencies, workload BA/Dev/QA, due date và label.
3. **Chốt cam kết**: lưu phạm vi và story point tại thời điểm chốt làm baseline.
4. **Theo dõi mỗi ngày**: cập nhật risk, blocker, người xử lý và quyết định cần leader hỗ trợ.
5. **Kết thúc sprint**: đối chiếu cam kết với kết quả, giải thích carryover và mục tiêu chưa đạt.
6. **Đánh giá cá nhân**: xem đóng góp, trách nhiệm và tác động có bằng chứng; thống nhất hành động cải thiện.

"Commit" trong workspace này nghĩa là **cam kết sprint**. Git commit chỉ dùng để lưu thay đổi workspace.

## Khởi tạo trên máy mới

Cần Git, Python 3.11+ và [uv](https://docs.astral.sh/uv/getting-started/installation/) để chạy MCP. MCP dùng Python 3.12 do uv quản lý. Jira integration chạy trên Linux, macOS hoặc WSL.

```bash
git clone https://github.com/lapluu1196/tl-manager.git
cd tl-manager
python3 scripts/workspace.py bootstrap
python3 scripts/credentials.py set-jira-token --url https://jira.example.com
python3 scripts/jira_check.py --discover
python3 scripts/setup_mcp.py
python3 scripts/workspace.py validate
```

Thay URL bằng Jira Data Center của bạn. Lệnh nhập PAT không hiện token trên màn hình. Mỗi máy nhập token riêng hoặc lấy từ password manager; Git không đồng bộ credentials.

Mở Codex tại thư mục này và trust project để nạp `.codex/config.toml`. Khởi động lại phiên nếu MCP chưa xuất hiện; dùng `/mcp` để kiểm tra. Đọc [hướng dẫn Jira](docs/jira.md) để chọn board, field story point và trạng thái clear.

## Bắt đầu một sprint

```bash
python3 scripts/workspace.py new-sprint sprint-001 --start 2026-11-02
```

Lệnh tạo `private/sprints/sprint-001/`, metadata và các mẫu theo từng đầu việc. Nếu có nhiều board, dùng ID sprint nội bộ phân biệt board, ví dụ `board-a-sprint-001`, và tùy chọn `--board <Jira board ID>`.

Điền `team-setup/input.md`, `sprint-planning/input.md`, rồi yêu cầu:

> Dùng $sprint-planning cho private/sprints/sprint-001. Đọc capacity và mục tiêu đã điền, đối chiếu Jira, đề xuất phạm vi, label và due date; ghi các điểm còn thiếu dữ liệu vào output.

> Dùng $sprint-commitment để chốt phương án đã thống nhất. Giữ baseline tại thời điểm chốt, ghi scope change riêng.

> Dùng $daily-risk rà soát mục tiêu của sprint-001 hôm nay; nêu bằng chứng, mức rủi ro và hành động cần tôi quyết định.

> Dùng $sprint-review và $individual-review tổng kết sprint-001 dựa trên baseline, cutoff cuối sprint và lịch sử thay đổi.

Các skill hướng dẫn AI thực hiện công việc. Workspace chưa phải dashboard tự chạy hay job báo cáo theo lịch; dữ liệu cần được đọc từ Jira và bổ sung thông tin capacity/mục tiêu trước mỗi lần phân tích.

## Báo cáo tập trung cho manager

Dùng [management-reporting](skills/management-reporting/SKILL.md) để công bố báo cáo sprint trên một Google Sheet tập trung: Tổng quan dễ đọc, chi tiết theo sprint, link Jira và lịch sử các lần cập nhật. File có link ổn định lưu trong cấu hình private; Markdown và dữ liệu nguồn vẫn giữ ở `private/`. Bản nháp, cam kết đầu sprint và kết quả hiện tại được ghi rõ để tránh hiểu nhầm số liệu.

> Dùng `$management-reporting` cập nhật sprint `<id>` vào Google Sheet tập trung đã cấu hình; giữ lịch sử và ghi chú manager, nêu nguồn, cutoff và dữ liệu còn thiếu.

Đọc [hướng dẫn kết nối Google Workspace](docs/google-workspace.md#báo-cáo-tập-trung-cho-quản-lý) để tạo file, đăng nhập và chia sẻ. Quyền xem/comment qua link phải được người dùng yêu cầu cụ thể cho từng file; không tự áp dụng cho đánh giá cá nhân hoặc các Sheet khác.

## Cấu trúc

| Vị trí | Nội dung |
| --- | --- |
| [INDEX.md](INDEX.md) | Điểm vào tất cả đầu việc |
| `skills/<đầu-việc>/` | `SKILL.md` và `assets/input.md`, `assets/output.md` |
| `config/workstreams.json` | Registry tạo ra chỉ mục |
| `config/integrations.json` | Tích hợp, phiên bản, biến credentials cần dùng |
| `docs/` | Quy tắc đo lường, Jira, đồng bộ và mở rộng |
| `scripts/`, `tests/` | Công cụ hỗ trợ và kiểm thử |
| `.local/` | Credentials và mapping thực tế, chỉ lưu trên máy |
| `private/` | Dữ liệu sprint, Jira, đánh giá cá nhân, chỉ lưu trên máy |
| `.agents/skills/` | Liên kết discovery do bootstrap tạo |
| `.codex/config.toml` | Cấu hình MCP theo đường dẫn máy, do setup tạo |

Repository này public. Chỉ đồng bộ quy trình, công cụ và mẫu trống. Dữ liệu công việc thực tế cần kênh riêng có quyền truy cập phù hợp: [làm việc nhiều máy](docs/multi-machine.md).

## Mở rộng và kiểm tra

```bash
python3 scripts/workspace.py add-workstream release-planning --title "Lập kế hoạch phát hành"
python3 scripts/workspace.py validate
python3 -m unittest discover -s tests -v
python3 scripts/check_publication.py
```

[Thêm đầu việc/tích hợp](docs/extending.md) · [Định nghĩa chỉ số](docs/metrics.md) · [Bảo vệ dữ liệu](docs/security.md)

Đầu việc bổ sung: [đánh giá năng lực sử dụng AI theo L1–L5](skills/ai-capability-review/SKILL.md), với [hướng dẫn kết nối Google Sheets/Drive](docs/google-workspace.md). Cần đăng nhập OAuth trước khi thao tác Sheet thực tế.
