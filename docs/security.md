# Credentials và dữ liệu quản lý

## Các vùng dữ liệu

| Vùng | Được đưa lên repo public? | Ví dụ |
| --- | --- | --- |
| Hướng dẫn/mẫu trống | Có | Skill, tiêu chí, bảng chưa điền |
| Cấu hình mẫu | Có | Tên biến, ID giả, URL ví dụ |
| `.local/` | Không | PAT, Jira mapping, metadata discovery |
| `private/` | Không | Issue thật, baseline, báo cáo, capacity, ghi chú cá nhân |
| `.codex/config.toml` | Không | Đường dẫn riêng của từng máy |

Tên board, danh sách nhân sự, lịch nghỉ, ticket và kết quả cá nhân là dữ liệu nội bộ dù không phải password. Dùng nguồn giả trong tests/examples, không lấy nội dung thật rồi chỉ xóa tên.

## PAT

Tạo PAT trong profile Jira Data Center, đặt hạn dùng, dùng quyền tối thiểu cần thiết và có thể tách token theo máy. Token kế thừa quyền tài khoản; chế độ read-only của MCP không thay thế phân quyền Jira.

Nhập token bằng `scripts/credentials.py set-jira-token --url ...`. Không đưa token vào prompt, terminal history, `.env.example`, ảnh chụp hay issue GitHub. Không bật debug/log HTTP khi dùng dữ liệu thật.

Nếu token từng xuất hiện trong chat hoặc nơi chia sẻ, thay mới rồi thu hồi token cũ trong Jira. Không chỉ xóa file hay sửa Git commit: lịch sử/nhật ký có thể vẫn lưu giá trị. Việc thu hồi phải do người có quyền thực hiện; script workspace không tự quản lý vòng đời PAT.

Trên Linux/macOS, `.local/` và `private/` dùng quyền `0700`, secrets dùng `0600`. Trên Windows dùng WSL hoặc ACL giới hạn tài khoản; mode POSIX không thay thế Windows ACL. Với máy dùng chung, bật mã hóa ổ đĩa và khóa phiên.

## Publication guard

`.gitignore` chặn thêm file vô tình. `scripts/check_publication.py` kiểm tra Git index, kể cả file bị force-add: đường dẫn cấm, mẫu token phổ biến và giá trị credential đang cấu hình cục bộ. Guard đọc credentials với cùng kiểm tra quyền và symlink như launcher, không in nội dung nhạy cảm khi báo lỗi.

Pre-push và CI chạy `python3 scripts/check_publication.py --history`, kiểm tra thêm mọi commit còn được Git refs tham chiếu. Vì vậy secret hoặc báo cáo private từng được commit rồi xóa ở commit sau vẫn bị chặn. Kiểm tra lịch sử yêu cầu clone đầy đủ; CI dùng `fetch-depth: 0`. Xóa secret khỏi file hiện tại không đủ để an toàn khi push; cần thu hồi secret và xử lý lịch sử trước khi xuất bản.

Hooks và CI giúp giảm lỗi, nhưng regex không nhận diện mọi loại secret hay dữ liệu nhân sự. Review diff trước publish; không xem guard pass là bằng chứng mọi dữ liệu đều được phép công khai. Cập nhật guard/tests nếu có kiểu credential hoặc đường dẫn nhạy cảm mới.

Không mở cổng MCP ra mạng: integration này dùng stdio cục bộ. Giữ TLS verification; nếu công ty dùng CA riêng, cấu hình certificate bundle tin cậy thay vì bỏ xác minh chứng chỉ.
