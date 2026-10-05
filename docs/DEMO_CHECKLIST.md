# Kịch bản demo và ảnh cần nộp
Điền tên, MSSV, lớp, giảng viên, URL GitHub ở bìa báo cáo trước khi nộp.

| STT | Thao tác / ảnh | Tiêu chí đạt |
|---|---|---|
| 01 | GitHub source, README, lịch sử | Có tối thiểu 3 commit có ý nghĩa |
| 02 | docker compose ps -a | Service chạy; migrate Exited 0 |
| 03 | Website qua :8080 | Có phòng và form đăng ký |
| 04 | Đơn đặt chỗ 2 đêm | Đúng tổng tiền, không trùng phòng |
| 05 | pgAdmin bảng booking_booking | Có dòng đúng đơn vừa tạo |
| 06 | curl -I http://localhost:8080 | Có security headers |
| 07 | Prometheus /targets | 5 target UP; pg_up, nginx_up bằng 1 |
| 08 | Grafana Hotel Operations | CPU, RAM, web, DB có dữ liệu |
| 09 | Explore Loki | Chạy 3 query trong LOGQL.md, có kết quả |
| 10 | Hardening | UID, mạng, quyền DB, không lộ 5432 |

Lệnh minh chứng hardening:
```bash
docker compose exec web id
docker compose exec nginx id
docker network inspect hotel-booking_data
docker compose exec db psql -U postgres -d hotel -c "SELECT rolname,rolsuper,rolcreatedb,rolcreaterole FROM pg_roles WHERE rolname LIKE 'hotel_%';"
docker compose port db 5432
```
Lệnh cuối không in mapping là kết quả mong đợi. Không chụp `docker compose config` đầy đủ vì có secret đã được nội suy.

Lưu ảnh vào docs/evidence (mặc định gitignore ảnh; chỉ `git add -f` sau khi che bí mật). Chèn screenshot thực vào cuối báo cáo ở các mục tương ứng. Ảnh minh họa giao diện nếu có là chạy local SQLite, không thay cho ảnh Compose/PostgreSQL.

Demo 8–10 phút: kiến trúc (1), nghiệp vụ và pgAdmin (3), metrics (2), LogQL (2), hardening và GitHub (2). Người trình bày phải giải thích được reverse proxy, exporter, scrape, datasource, label và volume.
