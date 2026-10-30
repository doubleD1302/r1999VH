# Quy Chuẩn Dọn Dẹp Bộ Nhớ Tạm & Quản Lý Sao Lưu (Cleanup & Backup Retention Policy)

Tài liệu này là quy chuẩn bắt buộc cho mọi Agent và lập trình viên khi tham gia dự án Việt hóa Reverse: 1999 (`r1999VH`).

---

## 1. Nguyên Tắc Cốt Lõi (Core Invariants)

1. **Dọn dẹp triệt để sau mỗi Task:** Kết thúc bất kỳ tác vụ nào (trích xuất dữ liệu, biên tập văn bản, build launcher, hoặc đóng gói patch), toàn bộ bộ nhớ tạm (cache, bytecode, tệp dump trung gian) phải được dọn dẹp sạch sẽ.
2. **Quy tắc Retention Sao lưu (Tối đa 2 bản):** 
   * Thư mục `VietHoa/backups/` **chỉ được phép lưu giữ tối đa 02 bản sao lưu gần nhất**.
   * Khi tạo bản sao lưu thứ 3, hệ thống hoặc agent **bắt buộc phải xoá vĩnh viễn bản sao lưu cũ nhất**, tuyệt đối không để dồn ứ hàng chục GB bản backup gây tràn ổ đĩa.
3. **Không xoá nguồn gốc:** Quy trình dọn dẹp không bao giờ được chạm vào các tệp mã nguồn, tài liệu hướng dẫn `docs/`, cấu hình `config/`, hoặc tệp `dist/` chuẩn vàng.

---

## 2. Danh Mục Các Đối Tượng Cần Dọn Dẹp

### 2.1. Bộ nhớ tạm và Cache (Xoá 100%)
* Thư mục Python bytecode: `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`.
* Thư mục build tạm của PyInstaller/Qt: `build/`, `.pytest_cache/`, `.ruff_cache/`.
* Tệp tạm thời: `*.tmp`, `*.temp`, các file log phát sinh trong quá trình chạy thử nghiệm.
* Thư mục trung gian Android: `android/.gradle/buildOutputCleanup/`, `android/app/build/intermediates/`.

### 2.2. Quản lý Thư mục `backups/`
* Mỗi khi thực hiện một thao tác rủi ro cao (patch file game, ghi đè bundle), tạo thư mục backup theo định dạng: `backups/<tên_tác_vụ>_YYYYMMDD_HHMM/`.
* Sau khi tạo backup hoặc hoàn thành task, thực thi script `python tools/cleanup_workspace.py`.
* Script sẽ tự động liệt kê các bản backup, sắp xếp theo thời gian `mtime`, giữ 2 bản mới nhất và xoá các bản cũ hơn.

---

## 3. Lệnh Thực Thi Tự Động

Chạy lệnh sau tại thư mục gốc `VietHoa`:

```powershell
python tools/cleanup_workspace.py
```
