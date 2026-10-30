---
name: r1999-cleanup-and-backup-retention
description: Quy chuẩn bắt buộc tự động dọn dẹp triệt để bộ nhớ tạm (cache, bytecode, build temp) và quản lý thư mục backups chỉ lưu giữ tối đa 2 bản gần nhất sau mỗi task của dự án Việt hóa Reverse: 1999.
---

# Reverse: 1999 — Skill Dọn Dẹp Bộ Nhớ Tạm & Quản Lý Sao Lưu (Retention 2 Bản)

Kỹ năng này bắt buộc phải được kích hoạt và thực thi vào cuối mỗi task hoặc quy trình làm việc trong dự án `r1999VH`.

## 1. Hành Động Bắt Buộc Sau Mỗi Task
Sau khi hoàn thành bất kỳ công việc nào (dịch thuật, trích xuất dữ liệu, sửa font, đóng gói patch, build launcher):
1. Không để lại các tệp bytecode Python (`__pycache__`, `*.pyc`).
2. Không để lại thư mục build tạm thời (`build/`, `.pytest_cache`).
3. Chạy công cụ dọn dẹp và kiểm tra retention:
   ```powershell
   python tools/cleanup_workspace.py
   ```

## 2. Quy Tắc Sao Lưu (Backup Retention Rule)
* Thư mục `backups/` chứa các snapshot sao lưu trước khi can thiệp vào tài nguyên game.
* **Giới hạn bất biến:** Tối đa 02 bản sao lưu được phép tồn tại trong `backups/`.
* Khi bản thứ 3 được tạo, script `tools/cleanup_workspace.py` sẽ tự động xác định thời gian sửa đổi (mtime) và xoá bản cũ nhất để giải phóng dung lượng.

## 3. Chốt Chặn Kiểm Tra
- [x] Không có tệp rác `*.tmp`, `*.pyc` nằm ngoài `.gitignore`.
- [x] Thư mục `backups/` có $\le 2$ mục con.
- [x] Toàn bộ mã nguồn cốt lõi trong `config/`, `docs/`, `launcher/`, `android/`, `dist/` được bảo toàn nguyên vẹn.
