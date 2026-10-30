---
name: r1999-github-sync-and-release
description: Quy chuẩn đồng bộ Git và phát hành GitHub Release cho dự án Reverse: 1999 Việt Hóa (r1999VH). Đảm bảo tiêu đề release chỉ chứa số phiên bản, mô tả dưới 100 từ và tự động push sau khi hoàn thành task.
---

# Reverse: 1999 — Skill Đồng Bộ Git & Phát Hành GitHub Release

Kỹ năng này chịu trách nhiệm kiểm soát quy trình đồng bộ Git và đóng gói bản phát hành GitHub Release cho kho lưu trữ `https://github.com/doubleD1302/r1999VH`.

## 1. Quy Trình Đồng Bộ Sau Mỗi Task
Sau khi hoàn thành một task và đã chạy `tools/cleanup_workspace.py`:
1. Kiểm tra trạng thái Git (`git status`).
2. Soạn thông điệp commit theo chuẩn Conventional Commits (`feat:`, `fix:`, `chore:`).
3. Đẩy lên nhánh `main`:
   ```powershell
   python tools/git_push_release.py "feat(core): hoàn thành thiết lập kịch bản và công cụ"
   ```

## 2. Quy Chuẩn Bắt Buộc Khi Tạo GitHub Release
1. **Tiêu đề Release:** CHỈ CHỨA SỐ PHIÊN BẢN (ví dụ: `0.1.0`). Tuyệt đối không thêm tiền tố `v`, `Release`, emoji hay bất kỳ chữ nào khác.
2. **Mô tả Release:** Viết bằng tiếng Việt có dấu, gạch đầu dòng ngắn gọn, tối đa 100 từ, tập trung vào những thay đổi cốt lõi.
