# Danh mục công việc quản lý

Tạo tự động từ `config/workstreams.json`; cập nhật bằng `python3 scripts/workspace.py index`.

Bắt đầu tại [README.md](README.md). Mỗi đầu việc có hướng dẫn, mẫu đầu vào và mẫu kết quả riêng.

| Đầu việc | Tần suất | Hướng dẫn | Đầu vào | Kết quả | Lệnh gọi skill |
| --- | --- | --- | --- | --- | --- |
| Thiết lập team và capacity | Khi onboarding và trước mỗi sprint | [team-setup](skills/team-setup/SKILL.md) | [input.md](skills/team-setup/assets/input.md) | [output.md](skills/team-setup/assets/output.md) | `$team-setup` |
| Lập kế hoạch sprint | Mỗi 2 tuần | [sprint-planning](skills/sprint-planning/SKILL.md) | [input.md](skills/sprint-planning/assets/input.md) | [output.md](skills/sprint-planning/assets/output.md) | `$sprint-planning` |
| Chốt cam kết sprint | Sau planning | [sprint-commitment](skills/sprint-commitment/SKILL.md) | [input.md](skills/sprint-commitment/assets/input.md) | [output.md](skills/sprint-commitment/assets/output.md) | `$sprint-commitment` |
| Theo dõi hằng ngày và rủi ro mục tiêu | Hằng ngày | [daily-risk](skills/daily-risk/SKILL.md) | [input.md](skills/daily-risk/assets/input.md) | [output.md](skills/daily-risk/assets/output.md) | `$daily-risk` |
| Tổng kết sprint và cải tiến | Cuối sprint | [sprint-review](skills/sprint-review/SKILL.md) | [input.md](skills/sprint-review/assets/input.md) | [output.md](skills/sprint-review/assets/output.md) | `$sprint-review` |
| Đánh giá đóng góp và trách nhiệm cá nhân | Cuối sprint hoặc kỳ 1:1 | [individual-review](skills/individual-review/SKILL.md) | [input.md](skills/individual-review/assets/input.md) | [output.md](skills/individual-review/assets/output.md) | `$individual-review` |
| Bổ sung đầu việc và tích hợp | Khi quy trình thay đổi | [workspace-maintenance](skills/workspace-maintenance/SKILL.md) | [input.md](skills/workspace-maintenance/assets/input.md) | [output.md](skills/workspace-maintenance/assets/output.md) | `$workspace-maintenance` |

## Dữ liệu làm việc

Đầu vào và báo cáo thực tế của sprint nằm tại `private/sprints/<sprint-id>/<workstream>/`.
Cập nhật hằng ngày nằm tại `private/sprints/<sprint-id>/daily-risk/daily/`.
Dữ liệu riêng tư và thông tin xác thực trong `.local/` không được đưa vào Git; chuyển chúng qua kênh riêng được phê duyệt.

## Các lệnh quản lý workspace

```sh
python3 scripts/workspace.py bootstrap
python3 scripts/workspace.py validate
python3 scripts/workspace.py new-sprint <sprint-id> --start YYYY-MM-DD --board <board-id>
python3 scripts/workspace.py add-workstream <slug> --title "Tên đầu việc"
```

Chọn mã sprint và ngày bắt đầu thực tế; lệnh bootstrap không tự tạo sprint hiện tại.
Kiểm tra Jira: `python3 scripts/jira_check.py --help`. Thiết lập MCP: `python3 scripts/setup_mcp.py --help`.
