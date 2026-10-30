# Hướng Dẫn Cài Đặt Font Việt Hóa Cho Reverse: 1999

Dự án sử dụng 2 bộ font Việt hóa chuẩn:
1. **DVN PT Serif** (Bản Việt hóa của DesignerVN - dùng làm font văn bản chính, hội thoại, giao diện, mô tả kỹ năng).
2. **UVF Didot LT Std** (Bản Việt hóa của UVF - dùng làm font tiêu đề số, phong cách thời trang / quý tộc).

---

## 1. Sơ Đồ Ánh Xạ Font Vào Game (Font Mapping)

| Tên file font game yêu cầu | Font nguồn tương ứng | Vị trí sử dụng trong game |
| :--- | :--- | :--- |
| `regular.ttf` | **DVN PT Serif Regular** | Toàn bộ hội thoại cốt truyện, văn bản UI thông thường |
| `bold.ttf` | **DVN PT Serif Bold** | Chữ in đậm, điểm nhấn, tên người nói |
| `italic.ttf` | **DVN PT Serif Italic** | Lời dẫn, suy nghĩ nội tâm, trích dẫn |
| `bolditalic.ttf` | **DVN PT Serif Bold Italic** | Nội tâm in đậm |
| `didot.ttf` | **UVF Didot LT Std Regular** | Tiêu đề chương, chữ số phong cách cổ điển |
| `didot_bold_1.ttf` | **UVF Didot LT Std Bold** | Tiêu đề lớn |
| `didot_italic_2.ttf` | **UVF Didot LT Std Italic** | Tiêu đề phụ, số phụ |

---

## 2. Cách Cài Đặt

1. Đặt các tệp font tải về (`.ttf` hoặc `.otf`) vào thư mục:
   `VietHoa/fonts/raw/`
2. Chạy lệnh tự động chuẩn hóa và nạp font vào AssetBundle:
   ```powershell
   python tools/font_manager.py
   ```
3. Script sẽ tự động:
   * Kiểm tra mức độ bao phủ ký tự tiếng Việt (yêu cầu 100% không thiếu dấu).
   * Chuẩn hóa bảng `name` thành `PT Serif` và `Didot` để Unity nhận diện chính xác.
   * Đóng gói vào bundle `47a282dfe68a42d302e22c4920ed9b5e.dat` và xuất ra `VietHoa/dist/`.
