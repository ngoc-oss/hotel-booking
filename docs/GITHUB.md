# Nộp GitHub
1. Tự tạo tài khoản GitHub theo mã SV nếu giảng viên yêu cầu. Không cung cấp mật khẩu/PAT cho người khác.
2. Tạo repo rỗng tên `MSSV-Hotel-Booking`, không tích README trên GitHub.
3. Gói có lịch sử Git ba mốc; nếu giải nén ẩn file .git thì `git log` phải thấy ba commit.
```bash
git log --oneline
git status
git config user.name "HO TEN SINH VIEN"
git config user.email "EMAIL_CUA_BAN"
git remote add origin https://github.com/TAI_KHOAN/MSSV-Hotel-Booking.git
git push -u origin main
```
Nếu dùng PAT, nhập qua trình xác thực Git khi được hỏi, không ghi PAT vào URL hoặc file.
Ba commit đóng gói là các mốc cấu hình do Project Builder chuẩn bị, không phải bằng chứng sinh viên đã chạy. Sau khi chạy thật, thêm thông tin SV, screenshot đã che bí mật và kết quả kiểm tra rồi tạo commit riêng có nội dung rõ ràng.
Nếu `.git` bị mất: khôi phục lịch sử từ `history.bundle` trong thư mục ngoài project bằng `git clone history.bundle hotel-restored`, sau đó làm việc trong hotel-restored. File bundle chứa cùng lịch sử ba mốc.
