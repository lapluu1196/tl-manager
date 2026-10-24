# Thêm đầu việc và tích hợp

`config/workstreams.json` là registry; `INDEX.md` được sinh từ registry. Mỗi đầu việc có một package trong `skills/`, gồm hướng dẫn và mẫu input/output.

## Thêm đầu việc

```bash
python3 scripts/workspace.py add-workstream release-planning --title "Lập kế hoạch phát hành"
```

Lệnh tạo package, cập nhật registry, chỉ mục và discovery. Hoàn thiện:

- `skills/release-planning/SKILL.md`: khi nào dùng, thông tin cần có, cách thực hiện và tiêu chí hoàn tất.
- `skills/release-planning/assets/input.md`: dữ liệu leader cần cung cấp, nguồn và thời điểm.
- `skills/release-planning/assets/output.md`: quyết định, bằng chứng, rủi ro, owner và hạn hành động.
- Entry registry: cadence, inputs/outputs và integrations thực sự cần.

Thêm template tùy nhu cầu và khai báo trong registry. Chạy lại bootstrap/index khi chỉnh registry thủ công. Sprint đã tạo không tự thay đổi; copy thêm template vào sprint đang làm nếu phù hợp, không ghi đè baseline hay báo cáo đã chốt.

```bash
python3 scripts/workspace.py index
python3 scripts/workspace.py bootstrap
python3 scripts/workspace.py validate
```

Không tạo skill chỉ để phân loại thư mục. Một package cần có một công việc cụ thể, input đủ rõ và đầu ra có thể kiểm tra.

## Thêm tích hợp hoặc credentials khác

Ví dụ GitHub để đối chiếu PR/commit với Jira, Confluence cho đặc tả, hoặc lịch nghỉ cho capacity:

1. Thêm metadata vào `config/integrations.json`: ID, provider, version, runtime, setup/check/launcher, biến môi trường cần dùng và chế độ quyền.
2. Tạo config mẫu chỉ có placeholder. Dùng file riêng trong `.local/` hoặc secret manager; không đặt secret vào registry hay `.codex/config.toml`.
3. Viết launcher/validator riêng hoặc mở rộng parser với allowlist rõ ràng. Parser Jira cố ý không nhận credential tùy ý; không bỏ validation để thêm dịch vụ mới.
4. Pin dependency cần thiết tại cấu hình integration, ghi cách cài và cập nhật. Workspace không cần `package.json` nếu không có công cụ Node; không thêm package manager chỉ để có một manifest.
5. Liên kết integration ID trong các workstream dùng nó. Cập nhật docs, input/output và index nếu luồng công việc thay đổi.
6. Viết tests cho input không hợp lệ, thiếu credential, quyền đọc/ghi, lỗi mạng và không làm lộ dữ liệu; kiểm thử bằng quyền tối thiểu.

Lưu ý: GitHub PAT khác Jira PAT. Không tái sử dụng một token giữa dịch vụ; không tự bật Confluence chỉ vì cùng nhà cung cấp Atlassian.

## Kiểm tra trước commit

```bash
python3 scripts/workspace.py validate
uv run --no-project --with-requirements requirements-dev.txt coverage run --source=scripts -m unittest discover -s tests
uv run --no-project --with-requirements requirements-dev.txt coverage report --fail-under=80
python3 scripts/check_publication.py
```

Nếu chỉ sửa mẫu/hướng dẫn, kiểm tra link, index và ví dụ thực tế là đủ; tests cần bổ sung khi có logic hoặc rủi ro mới. Khi thêm dependency, chạy công cụ audit phù hợp trước commit. Không tạo dữ liệu thật làm fixture public.
