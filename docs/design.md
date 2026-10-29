# Thiết kế API: Canteen API

API quản lý thực đơn căng tin trường, xây dựng bằng FastAPI. Dữ liệu lưu trong bộ nhớ (khởi động lại server sẽ về 4 món mẫu).

## 1. Quy tắc nghiệp vụ

| Mã | Quy tắc | Mã lỗi khi vi phạm |
|---|---|---|
| BR1 | Tên món không được trùng (không phân biệt hoa thường) | 409 Conflict |
| BR2 | Giá là số nguyên, lớn hơn 0, tối đa 200.000, chia hết cho 1.000 | 422 |
| BR3 | Loại món chỉ gồm: `com`, `bun_pho`, `do_uong`, `an_vat` | 422 |
| BR4 | Món mới mặc định `available = true` | (không có) |

## 2. Bảng 2: Các trường của MenuItem

| Trường | Kiểu | Bắt buộc | Ràng buộc |
|---|---|---|---|
| `id` | int | Tự sinh | Server tự tăng, bắt đầu từ 1 |
| `name` | string | Có | Dài 2 đến 100 ký tự, không trùng (BR1) |
| `category` | string | Có | Một trong: `com`, `bun_pho`, `do_uong`, `an_vat` (BR3) |
| `price` | int | Có | 0 < giá ≤ 200000, chia hết cho 1000 (BR2) |
| `available` | bool | Không | Mặc định `true` (BR4) |
| `updated_at` | datetime | Tự sinh | Server cập nhật mỗi khi thêm hoặc sửa |

## 3. Bảng 3: Các endpoint

| Phương thức | Đường dẫn | Mục đích | Mã thành công | Mã lỗi có thể gặp |
|---|---|---|---|---|
| GET | `/menu-items` | Xem thực đơn (lọc `category`, `available`, `max_price`; sắp xếp `sort`, `order`) | 200 | 422 (tham số sai) |
| GET | `/menu-items/{id}` | Xem chi tiết một món | 200 | 404 (không có món), 422 (id không hợp lệ, ví dụ 0) |
| POST | `/menu-items` | Thêm món mới | 201 (kèm header `Location`) | 409 (trùng tên), 422 (dữ liệu sai) |
| PUT | `/menu-items/{id}` | Thay thế toàn bộ thông tin món | 200 | 404, 409 (trùng tên món khác), 422 |
| PATCH | `/menu-items/{id}` | Sửa một phần (chỉ các trường gửi lên) | 200 | 404, 409, 422 |
| DELETE | `/menu-items/{id}` | Xóa món | 204 (không có body) | 404, 422 |

Ngoài ra có `GET /health` trả `{"status": "ok"}` (200) để kiểm tra server đang chạy.

## 4. Giải thích các mã trạng thái

- **200 OK**: xử lý thành công, có dữ liệu trả về.
- **201 Created**: tạo mới thành công, header `Location` trỏ tới tài nguyên mới.
- **204 No Content**: xóa thành công, không trả nội dung.
- **404 Not Found**: id hợp lệ nhưng không có món tương ứng.
- **409 Conflict**: dữ liệu mâu thuẫn trạng thái hiện tại (trùng tên, BR1).
- **422 Unprocessable Entity**: yêu cầu đúng cú pháp nhưng sai quy tắc dữ liệu (BR2, BR3, id không phải số dương, thiếu trường).

## 5. Phân biệt PUT và PATCH

- **PUT** yêu cầu gửi đủ các trường bắt buộc (`name`, `category`, `price`) và thay thế toàn bộ món.
- **PATCH** chỉ gửi trường cần đổi, các trường còn lại giữ nguyên (ví dụ `{"available": false}`).
