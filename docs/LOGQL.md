# Truy vấn trong Grafana → Explore → Loki
Chọn Last 15 minutes, truy cập website và tạo/hủy một đơn trước khi thử.

```logql
{job="nginx", filename="/var/log/nginx/access.log"}
```
Toàn bộ access log Nginx.

```logql
{job="nginx", filename="/var/log/nginx/access.log"} | json | status >= 400
```
Lỗi HTTP. Truy cập http://localhost:8080/khong-ton-tai để tạo 404.

```logql
{job="hotel"} |= "booking_created"
```
Sự kiện đặt phòng. Không ghi tên/điện thoại vào log ứng dụng.

```logql
sum(count_over_time({job="nginx",filename="/var/log/nginx/access.log"} | json | status >= 400 [5m]))
```
Đếm phản hồi lỗi trong 5 phút.

```logql
{job="hotel"} |= "booking_cancelled"
```
Sự kiện hủy phòng. Positions nằm trong tmpfs: khi tạo lại Promtail có thể đọc lại log cũ; chấp nhận cho lab, triển khai thực cần persistent positions và log rotation.
