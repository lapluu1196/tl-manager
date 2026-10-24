# Làm việc trên nhiều máy

GitHub đồng bộ workspace: quy trình, mẫu, công cụ và cấu hình không chứa thông tin nội bộ. Repository `lapluu1196/tl-manager` hiện public; dữ liệu Jira và đánh giá cá nhân không được tự đưa lên đây.

## Máy mới

Clone repository, cài Python 3.11+ và uv, chạy các lệnh setup trong [README](../README.md). Bootstrap không ghi đè cấu hình hoặc secrets đã có. Chạy lại `setup_mcp.py` trên mỗi máy vì đường dẫn tuyệt đối khác nhau.

Lấy credentials từ password manager hoặc tạo PAT riêng cho từng máy với quyền/expiry phù hợp. Không đồng bộ `.local/secrets.env` bằng Git, email hay tài liệu chia sẻ. Không copy `.codex/config.toml` từ máy khác.

```bash
git pull --ff-only
python3 scripts/workspace.py bootstrap
python3 scripts/workspace.py validate
```

Trước khi pull, lưu thay đổi của mình bằng commit hoặc stash có chủ đích; không reset để xóa công việc chưa lưu. Jira integration cần Linux, macOS hoặc WSL để bảo vệ credentials bằng quyền POSIX. Bootstrap có thể dùng bản copy discovery khi symlink không khả dụng; chạy lại bootstrap sau khi sửa/cập nhật skill. `.agents/skills/` là dữ liệu sinh trên từng máy, không commit các bản copy vào Git.

## Dữ liệu đang làm dở

`.local/` và `private/` không đi theo `git pull`. Chỉ clone repo sẽ không mang theo báo cáo sprint hoặc mapping Jira. Chọn một kênh được công ty cho phép:

- Repository **private riêng** cho dữ liệu quản lý, giới hạn người được xem; credentials vẫn ở password manager. Copy hoặc liên kết working data vào `private/` và đồng bộ bằng quy trình riêng của repository dữ liệu.
- Kho tài liệu nội bộ có phân quyền và lịch sử phiên bản cho báo cáo đã được chia sẻ; ghi chú nhân sự dùng quyền riêng.
- Kho đồng bộ được mã hóa có kiểm soát truy cập cho `private/` và bản cấu hình `.local/workspace.json` không chứa secrets.

Không đổi visibility của repo hiện tại một cách ngầm định. Không thêm `private/` vào Git chỉ vì cần làm tiếp trên máy khác. Nếu muốn dùng một repository private duy nhất, cần quyết định quyền truy cập và phạm vi dữ liệu trước; kiểm tra lại guard/ignore theo chính sách mới và vẫn cấm mọi credentials.

Mỗi snapshot/báo cáo cần timestamp, sprint/board ID và nguồn để tránh ghi đè bản mới hơn. Giữ baseline đã chốt bất biến, ghi thay đổi vào bản ghi mới.

## Đẩy thay đổi workspace

```bash
python3 scripts/workspace.py validate
python3 -m unittest discover -s tests -v
git diff
git add README.md INDEX.md AGENTS.md config docs skills scripts tests .github .githooks .gitignore requirements-dev.txt
python3 scripts/check_publication.py
git diff --cached --stat
git commit -m "docs: update management workflow"
git push
```

Chỉ stage các file thực sự cần; danh sách trên là các vùng public dự kiến, không phải yêu cầu stage toàn bộ mỗi lần. Guard đọc nội dung trong Git index để phát hiện credential đã stage và đường dẫn private. Nó không thay thế review dữ liệu con người.

Có thể bật hooks cục bộ bằng `git config core.hooksPath .githooks`. Hooks chạy guard trước commit/push; CI cũng kiểm tra độc lập.
