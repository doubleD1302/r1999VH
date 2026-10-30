# Reverse: 1999 — Dự Án Việt Hóa Phong Cách Light Novel (r1999VH)

Dự án bản địa hóa tiếng Việt cho tựa game **Reverse: 1999 (Global)** theo định hướng văn phong **Light Novel Anime kết hợp màu sắc cổ điển thế kỷ 20**, câu tiếng Việt tự nhiên và hài hước tiết chế.

Kho lưu trữ GitHub chính thức: [doubleD1302/r1999VH](https://github.com/doubleD1302/r1999VH)

---

## 1. Cấu Trúc Dự Án

* `config/`: Cấu hình hệ thống và bảng thuật ngữ chuẩn (`glossary.json`).
* `docs/`: Toàn bộ quy chuẩn biên tập văn phong, quy tắc release và bảo toàn dữ liệu:
  * `LIGHTNOVEL_STYLE_BIBLE_VI.md`: Quy chuẩn văn phong Light Novel Anime.
  * `VI_SENTENCE_EDITING_GUIDE.md`: Hướng dẫn biên tập câu tiếng Việt tự nhiên.
  * `HUMOR_LOCALIZATION_VI.md`: Hướng dẫn hài hước tiết chế, kiên quyết loại bỏ slang/meme đường phố.
  * `MASTER_GLOSSARY.md`: Bảng thuật ngữ Timekeeper, Arcanist, The Storm...
  * `CLEANUP_AND_BACKUP_POLICY.md`: Quy chuẩn dọn dẹp bộ nhớ tạm & giữ tối đa 2 bản sao lưu.
  * `GITHUB_RELEASE_RULES.md`: Quy tắc tạo release (tiêu đề chỉ chứa số phiên bản, mô tả $\le 100$ từ).
* `launcher/`: Mã nguồn Trình khởi chạy Windows (PC EXE) viết bằng PySide6, hỗ trợ tự cập nhật trực tiếp 4 bước (Self-update) và khớp phiên bản wildcard `*`.
* `android/`: Mã nguồn Trình khởi chạy Android (APK) hỗ trợ Local ADB / Shizuku / SAF để nạp patch không cần can thiệp file cài đặt gốc.
* `skills/`: Các kỹ năng AI chuyên biệt cho dự án:
  * `r1999-lightnovel-vi`: Kỹ năng biên tập văn phong Light Novel Anime.
  * `r1999-cleanup-and-backup-retention`: Kỹ năng tự động dọn dẹp & quản lý retention backup $\le 2$ bản.
  * `r1999-github-sync-and-release`: Kỹ năng kiểm tra quy chuẩn và push release lên GitHub.
  * `r1999-launcher-auto-update-assurance`: Kỹ năng đảm bảo tự động cập nhật trực tiếp trong app.
* `tools/`: Các công cụ tự động hóa:
  * `cleanup_workspace.py`: Script dọn dẹp rác, cache và xoá bản backup cũ.
  * `git_push_release.py`: Script kiểm tra quy chuẩn release và push GitHub.
* `dist/`: Nguồn chuẩn độc lập duy nhất (Single Golden Source of Truth) lưu trữ các file bundle và font đã Việt hóa.
* `backups/`: Thư mục lưu snapshot sao lưu (tự động luân chuyển giữ tối đa 2 bản).

---

## 2. Quy Trình Làm Việc Chuẩn Sau Mỗi Task

1. **Thực hiện task:** Dịch thuật, tinh chỉnh font hoặc sửa đổi tính năng.
2. **Dọn dẹp rác & quản lý retention:**
   ```powershell
   python tools/cleanup_workspace.py
   ```
3. **Kiểm tra và đẩy lên GitHub:**
   ```powershell
   python tools/git_push_release.py "feat(scope): mô tả công việc hoàn thành"
   ```
