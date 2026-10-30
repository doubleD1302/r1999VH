# Quy Tắc Đặt Tiêu Đề và Mô Tả Bản Phát Hành GitHub — r1999VH

Áp dụng cho mọi hoạt động commit, push và tạo GitHub Release trên kho lưu trữ `https://github.com/doubleD1302/r1999VH`.

---

## 1. Hai Yêu Cầu Bắt Buộc Khi Tạo GitHub Release

1. **Tiêu đề Release CHỈ ghi số phiên bản:**
   * Định dạng chuẩn: `X.Y.Z` (ví dụ: `0.1.0`, `1.0.0`).
   * **Tuyệt đối KHÔNG** thêm tiền tố `v`, `Release`, tên game, ngày tháng, emoji hay chú thích trạng thái (như `hotfix`, `beta`).
   * *Đúng:* `0.1.0`
   * *Sai:* `v0.1.0`, `Release 0.1.0`, `r1999VH 0.1.0 - Bản thử nghiệm 🎉`

2. **Mô tả Release không vượt quá 100 từ:**
   * Viết bằng tiếng Việt có dấu đầy đủ, súc tích và ngắn gọn nhất có thể.
   * Tập trung trực tiếp vào các tính năng mới hoặc lỗi đã sửa bằng gạch đầu dòng.
   * Bỏ qua lời chào, quảng cáo hay quá trình phát triển dài dòng.

---

## 2. Quy Chuẩn Commit Message

Tuân thủ định dạng Conventional Commits:
* `feat(...)`: Thêm tính năng mới, kịch bản dịch mới hoặc launcher mới.
* `fix(...)`: Sửa lỗi hiển thị font, sửa chính tả hoặc lỗi code.
* `chore(...)`: Cập nhật cấu hình, dọn dẹp bộ nhớ hoặc tài liệu.
* `docs(...)`: Cập nhật tài liệu kỹ thuật, hướng dẫn.
