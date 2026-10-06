# LOTUS STAY — Đề 6: Hệ thống đặt phòng khách sạn

Django + PostgreSQL + pgAdmin + Nginx + Prometheus + Grafana + cAdvisor + Loki + Promtail. Toàn bộ dịch vụ chạy bằng Docker Compose. Giao diện tiếng Việt, 6 phòng mẫu, đăng ký/đăng nhập, lọc phòng trống, đặt/hủy phòng, quản trị phòng/khách hàng/đặt chỗ.

## 1. Môi trường
Khuyến nghị **Ubuntu 22.04/24.04 trong VMware**, Docker Engine và Docker Compose v2.20+, Python 3, Git. Cấp VM 4 CPU, RAM 6–8 GB, đĩa trống 15 GB. cAdvisor dùng host mounts Linux và `/dev/kmsg`; cấu hình này ưu tiên Ubuntu Docker Engine, không cam kết tương đương trên Docker Desktop Windows.

## 2. Chạy lần đầu (Terminal Ubuntu)
```bash
cd hotel-booking
python3 scripts/setup.py
docker compose config --quiet
docker compose pull
docker compose up -d --build
docker compose ps -a
docker compose logs --tail=80 migrate web
curl -i http://localhost:8080/health/
python3 scripts/verify.py
```
`migrate` kết thúc với **Exited (0)** là bình thường: tạo bảng, admin, phòng mẫu và static. Các service còn lại phải Running; đợi 1–2 phút để có metrics/log.
Nếu lệnh docker thiếu quyền, dùng sudo hoặc cấu hình Docker group theo tài liệu chính thức; không chạy chmod 777 Docker socket.

## 3. Địa chỉ và tài khoản
| Thành phần | URL trên Windows | Tài khoản |
|---|---|---|
| Website | http://192.168.168.129:8080 | Tự đăng ký |
| Quản trị website | http://192.168.168.129:8080/admin/ | admin / giá trị ADMIN_PASSWORD trong .env |
| pgAdmin | http://127.0.0.1:15050 | giá trị PGADMIN_EMAIL / PGADMIN_PASSWORD trong .env |
| Grafana | http://127.0.0.1:13001 | admin / giá trị GRAFANA_PASSWORD trong .env |
| Prometheus | http://127.0.0.1:19090/targets | Không yêu cầu đăng nhập |

Mật khẩu thực nằm trong `.env`; `cat .env` để xem riêng, không chụp hoặc đưa lên GitHub. Mỗi mật khẩu do setup sinh ngẫu nhiên 48 ký tự hex. File mẫu không chứa tài khoản đăng nhập thật.
Trong pgAdmin mở **Servers → Hotel → Hotel PostgreSQL**, nhập OWNER_PASSWORD. Host là `db`, port 5432, DB `hotel`, user `hotel_owner`. Xem Schemas → public → Tables → booking_room / booking_booking / auth_user. Không dùng superuser cho ứng dụng.

## 4. Truy cập từ Windows vào máy Ubuntu

IP Ubuntu hiện tại: `192.168.168.129`. Kiểm tra IP trên Ubuntu bằng:

```bash
hostname -I
```

Nếu IP thay đổi, cập nhật `ALLOWED_HOSTS` và `CSRF_TRUSTED_ORIGINS` trong `.env` theo IP mới. Sau đó chạy trên Ubuntu, tại thư mục dự án:

```bash
sudo docker compose -f compose.yaml -f compose.override.yaml up -d --force-recreate web
```

Truy cập website từ trình duyệt Windows:
- Website: http://192.168.168.129:8080
- Quản trị website: http://192.168.168.129:8080/admin/

Grafana, pgAdmin và Prometheus chỉ mở cổng trên localhost của Ubuntu. Để truy cập từ Windows, mở PowerShell Windows và chạy:

```powershell
ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -L 127.0.0.1:13001:127.0.0.1:3000 -L 127.0.0.1:15050:127.0.0.1:5050 -L 127.0.0.1:19090:127.0.0.1:9090 ngoc26@192.168.168.129
```

Nhập mật khẩu tài khoản Ubuntu `ngoc26`. Khi nhập mật khẩu, terminal không hiển thị ký tự. Sau khi kết nối, cửa sổ đứng yên là bình thường.

Giữ cửa sổ PowerShell này mở, không nhấn Ctrl+C trong lúc sử dụng:
- Grafana: http://127.0.0.1:13001
- pgAdmin: http://127.0.0.1:15050
- Prometheus: http://127.0.0.1:19090/targets

Ubuntu cần có SSH server đang hoạt động. Nếu các cổng trên đang được tunnel cũ sử dụng, đóng tunnel cũ trước khi chạy lệnh mới. Khi IP Ubuntu thay đổi, cập nhật IP trong các URL website và lệnh SSH.

## 5. Demo nghiệp vụ
1. Đăng ký hai tài khoản, đăng nhập tài khoản thứ nhất.
2. Chọn ngày tương lai, xem phòng và đặt phòng 2 đêm. Tổng tiền = giá phòng × số đêm; server tự tính.
3. Tài khoản thứ hai đặt cùng phòng, cùng lịch: bị từ chối. Ngày trả của lượt trước được phép là ngày nhận của lượt sau.
4. Xem “Đặt chỗ của tôi”, hủy đơn bằng POST; phòng trống trở lại.
5. Admin quản lý phòng (thêm, sửa, ngừng kinh doanh), khách hàng trong Users và xem/hủy đặt chỗ. Không cho sửa tùy tiện lịch/tổng tiền trong admin. Phòng có lịch sử đặt không xóa được do PROTECT.

## 6. Giám sát và log
Grafana đã provision sẵn hai datasource và dashboard **Hotel / Hotel · Operations**. Có CPU/RAM container, Nginx request/kết nối, PostgreSQL khả dụng/kết nối, số đặt phòng và log Nginx. Prometheus `/targets` cần 5 target UP; đồng thời `pg_up=1`, `nginx_up=1` mới chứng minh exporter kết nối thành công. Xem `docs/LOGQL.md` cho 5 truy vấn.

## 7. Hardening
- Web chạy UID 10001, Nginx UID 101, Promtail UID 10001; web/Nginx root filesystem read-only, tmpfs /tmp.
- Web không publish cổng 8000, PostgreSQL không publish 5432; data/observe là mạng internal, proxy dùng mạng edge.
- DB tách owner (migration), app (DML), monitor (pg_monitor); runtime app không được CREATE TABLE/ROLE/DATABASE.
- no-new-privileges, drop ALL capabilities ở web/proxy/exporter; pgAdmin/Grafana/Prometheus chỉ bind 127.0.0.1.
- Mật khẩu ngẫu nhiên, .env bị gitignore; CSRF, session HttpOnly/SameSite, ORM chống SQL injection; Nginx có CSP, X-Frame-Options, nosniff, Referrer-Policy.
- cAdvisor là **ngoại lệ có quyền cao** để đọc host metrics; chỉ dùng trong VM lab tin cậy, không publish port. Mount socket read-only không biến Docker API thành read-only. Không tuyên bố mọi container đều non-root hoặc không đặc quyền.
- Bản này dùng HTTP + security headers (đúng phương án đề cho phép). Khi đưa lên Internet cần TLS, cookie Secure, rate limiting và rà soát cập nhật phiên bản.

## 8. GitHub và lịch sử commit
Repository: https://github.com/ngoc-oss/hotel-booking

- Commit 1: Triển khai website, PostgreSQL, pgAdmin và Nginx.
- Commit 2: Tích hợp Prometheus, Grafana và dashboard giám sát.
- Commit 3: Tích hợp Loki, Promtail, LogQL và hardening.
- Commit bổ sung: Sửa cấu hình truy cập Grafana và Prometheus qua localhost.
File .env chứa mật khẩu được gitignore và không đưa lên GitHub.

## 9. Dừng, mở lại, sao lưu
```bash
docker compose stop
docker compose start
# Hoặc khi vừa bật VM:
docker compose up -d
# Sao lưu DB trên Ubuntu:
mkdir -p backups
docker compose exec -T db pg_dump -U postgres hotel > backups/hotel.sql
```
`docker compose down` giữ named volumes. **Không dùng down -v** nếu muốn giữ dữ liệu. Sao lưu có dữ liệu cá nhân, không commit. Khôi phục chỉ vào DB lab đích đã chuẩn bị, tránh ghi đè dữ liệu đang dùng.

## 10. Kiểm thử và giới hạn xác minh
```bash
# Bộ test nghiệp vụ, dùng SQLite tách biệt dữ liệu triển khai:
docker compose run --rm -e TEST_SQLITE=1 web python manage.py test -v 2
# Test hệ thống đã chạy trên host:
python3 scripts/verify.py
# Kiểm tra đồng thời trên PostgreSQL thật đang chạy:
python3 scripts/concurrency.py
```
15 test nghiệp vụ đã chạy đạt trong môi trường tạo gói. SQLite không xác minh row lock PostgreSQL. Docker stack, PostgreSQL và exporter cần xác minh trên VM bằng các script đi kèm. Không sử dụng báo cáo để tuyên bố các bước chưa thực hiện đã đạt.
Promtail đã EOL 02/03/2026; giữ để đúng yêu cầu môn học, không khuyến nghị cho production. Loki giữ log 30 ngày (720h); cần tạo log mới trước demo nếu báo cáo sau thời gian này. Log file nguồn dùng volume riêng; cần xoay/dọn theo kế hoạch ở môi trường dài hạn.

## 11. Xử lý lỗi
- `manifest unknown`: kiểm tra tên/tag trong compose và mạng registry; không sửa thành tag tự đoán. Không dùng latest để che lỗi.
- `migrate` fail: xem log và DB health. init.sh chỉ chạy khi pgdata rỗng; sửa .env không đổi password của DB đã tồn tại. Đổi mật khẩu bằng SQL có quản lý hoặc tạo một project lab mới nếu không cần dữ liệu cũ.
- 502: xem `docker compose logs --tail=100 web migrate nginx`.
- CSRF 403 khi dùng IP VM: sửa hai biến host/origin và recreate web.
- Grafana No data: kiểm tra /targets, chọn Last 15 minutes, tạo traffic; cAdvisor cần Linux host mounts đúng Docker root directory.
- Loki không có log: truy cập web, đặt/hủy đơn, xem `docker compose logs promtail loki`; chỉ query đúng label trong docs.

Tài liệu: https://docs.docker.com/compose/ ; https://docs.djangoproject.com/en/5.2/topics/db/transactions/ ; https://github.com/prometheus-community/postgres_exporter ; https://github.com/nginx/nginx-prometheus-exporter ; https://github.com/google/cadvisor ; https://grafana.com/docs/loki/latest/send-data/promtail/
