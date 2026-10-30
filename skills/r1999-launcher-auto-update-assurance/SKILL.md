---
name: r1999-launcher-auto-update-assurance
description: Quy chuẩn bắt buộc và tự động hóa đảm bảo Launcher Reverse: 1999 (Windows EXE & Android APK) luôn tự động cập nhật trực tiếp trong ứng dụng, tuyệt đối không bắt người dùng tải lại thủ công.
---

# Reverse: 1999 — Quy Chuẩn Đảm Bảo Tự Động Cập Nhật Trực Tiếp (Seamless In-App Update Assurance)

Tài liệu này là quy chuẩn kỹ thuật bắt buộc cho việc phát triển, bảo trì và phát hành các bản cập nhật cho Reverse: 1999 Launcher (PC Windows EXE & Android APK).

---

## 1. Nguyên Tắc Cốt Lõi (Core Invariants)

1. **Tuyệt đối không bắt người dùng tải lại thủ công:** Mọi bản phát hành mới phải đảm bảo 100% người dùng đang ở phiên bản cũ mở launcher lên là nhận diện được thông báo cập nhật, bấm 1 nút là tự động tải và cài đặt trực tiếp trong launcher.
2. **Không khóa cứng mã tài nguyên (Resource Version Wildcard):** Game thường xuyên có các hotfix nhỏ cập nhật asset bundles từ máy chủ Bluepoch. Launcher không được chặn người dùng chỉ vì `resource_version` thay đổi nếu các tệp dịch không xung đột. Luôn hỗ trợ khớp phiên bản linh hoạt hoặc wildcard `*`.
3. **Độc lập và nguyên tử (Atomic Self-Update):** Quá trình cập nhật launcher phải có cơ chế sao lưu (backup), giải phóng khoá tệp (file lock), đổi tên nguyên tử, và tự phục hồi nếu có sự cố.

---

## 2. Quy Chuẩn Kỹ Thuật Cho PC Launcher (Windows EXE)

### 2.1. Xử lý File Lock trên Windows (Bắt buộc)
Windows cấm hoàn toàn việc ghi đè trực tiếp lên một tệp `.exe` đang chạy (`PermissionError [WinError 5]`). Mọi cơ chế self-update bắt buộc phải tuân theo luồng 4 bước:

1. **Truyền PID tiến trình cha (`parent_pid`):**
   - Khi launcher tạo job cập nhật, bắt buộc ghi `parent_pid = os.getpid()` vào job JSON.
2. **Đợi và kết liễu tiến trình cha:**
   - Trình `helper.exe` kiểm tra tiến trình `parent_pid`. Nếu sau 3 giây cha chưa thoát, helper gửi lệnh kết liễu an toàn (`taskkill /F /PID <parent_pid>`).
3. **Đổi tên trước khi ghi đè (Rename-before-replace):**
   - Windows **cho phép đổi tên** file exe đang chạy sang tên khác (`target.rename(target.old_xyz)`), nhưng **không cho phép ghi đè**.
   - Helper phải đổi tên file exe cũ sang `.old_uuid`, sau đó di chuyển file exe mới vào vị trí `target`, rồi mới xóa file `.old_uuid`.
4. **Khởi chạy bản mới:**
   - Helper khởi chạy launcher mới với `subprocess.Popen([str(target)])` và xác nhận tiến trình mới sống sót trước khi kết thúc.

### 2.2. Kênh phát hành Release Metadata cho PC
- File `patch_manifest.json` trên GitHub Release phải luôn khai báo danh sách phiên bản tài nguyên linh hoạt kèm wildcard:
  ```json
  "client_game_version": "2.3.0",
  "resource_version": "*, 20261031*"
  ```
- File `SHA256SUMS.txt` phải chứa đầy đủ mã băm SHA256 của file `Reverse1999-Windows_v{version}.exe` để hàm `check_for_updates` xác thực tải tự động.

---

## 3. Quy Chuẩn Kỹ Thuật Cho Android APK (Local ADB / Direct SAF)

### 3.1. Bắt buộc tăng `versionCode` mỗi lần phát hành
- File `android/app/build.gradle` phải tăng `versionCode` theo cấp số cộng nguyên dương ($N+1$).
- Cùng Keystore: Mọi bản build phải ký cùng keystore phát hành để Android cho phép cập nhật đè (In-place update) không báo lỗi xung đột chữ ký.

### 3.2. Đồng bộ Release Asset `android_launcher.json`
Mỗi khi phát hành release mới, file metadata trên GitHub Release bắt buộc phải được cập nhật khớp với APK mới:
```json
{
  "platform": "android",
  "variant": "localadb",
  "application_id": "com.r1999.viethoa.localadb",
  "version_name": "0.1.0",
  "version_code": 1,
  "apk_name": "Reverse1999-Android_v0.1.0.apk",
  "apk_url": "https://github.com/doubleD1302/r1999VH/releases/download/0.1.0/Reverse1999-Android_v0.1.0.apk",
  "size": 15000000,
  "sha256": "<Mã SHA256 chính xác>"
}
```
