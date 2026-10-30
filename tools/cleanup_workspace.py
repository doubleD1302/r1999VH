#!/usr/bin/env python3
"""
tools/cleanup_workspace.py
Dọn dẹp triệt để bộ nhớ tạm (cache, bytecode, build temp) và tự động quản lý bản sao lưu (backup retention).
QUY TẮC BẮT BUỘC: Thư mục backups/ CHỈ ĐƯỢC GIỮ TỐI ĐA 2 BẢN MỚI NHẤT. Mọi bản cũ hơn sẽ bị xoá vĩnh viễn.
"""

import os
import shutil
import sys
from pathlib import Path

MAX_BACKUP_RETENTION = 2

def get_project_root() -> Path:
    current = Path(__file__).resolve().parent
    return current.parent

def clean_bytecode_and_caches(root: Path):
    removed_dirs = 0
    removed_files = 0
    total_bytes = 0

    # 1. Clean __pycache__ and build caches
    target_dir_names = {"__pycache__", ".pytest_cache", ".ruff_cache", "build"}
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        dp = Path(dirpath)
        if dp.name in target_dir_names and not any(part.startswith(".venv") for part in dp.parts):
            try:
                size = sum(f.stat().st_size for f in dp.rglob('*') if f.is_file())
                total_bytes += size
                shutil.rmtree(dp)
                removed_dirs += 1
            except Exception as e:
                print(f"[WARN] Không thể xoá thư mục cache {dp}: {e}")

    # 2. Clean temporary files (*.pyc, *.pyo, *.tmp, *.log)
    for p in root.rglob("*"):
        if any(part.startswith(".venv") or part == ".git" for part in p.parts):
            continue
        if p.is_file() and p.suffix in {".pyc", ".pyo", ".tmp"}:
            try:
                total_bytes += p.stat().st_size
                p.unlink()
                removed_files += 1
            except Exception as e:
                print(f"[WARN] Không thể xoá file tạm {p}: {e}")

    print(f"[CLEANUP] Đã dọn dẹp cache: {removed_dirs} thư mục, {removed_files} tệp tạm (Giải phóng ~{total_bytes / 1024:.1f} KB).")

def enforce_backup_retention(root: Path, max_keep: int = MAX_BACKUP_RETENTION):
    backups_dir = root / "backups"
    if not backups_dir.exists():
        return

    # Liệt kê tất cả thư mục hoặc tệp con trong backups/
    items = [p for p in backups_dir.iterdir() if p.name != ".gitkeep"]
    if len(items) <= max_keep:
        print(f"[BACKUP] Số lượng bản sao lưu hiện tại: {len(items)}/{max_keep} (Đạt chuẩn).")
        return

    # Sắp xếp theo thời gian sửa đổi (mtime) giảm dần (mới nhất lên đầu)
    items.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    kept = items[:max_keep]
    to_delete = items[max_keep:]

    print(f"[BACKUP] Phát hiện {len(items)} bản sao lưu. Đang áp dụng quy chuẩn giữ tối đa {max_keep} bản mới nhất:")
    for k in kept:
        print(f"  [GIỮ] {k.name}")

    for old in to_delete:
        try:
            if old.is_dir():
                shutil.rmtree(old)
            else:
                old.unlink()
            print(f"  [XOÁ VĨNH VIỄN] Bản cũ: {old.name}")
        except Exception as e:
            print(f"  [LỖI] Không thể xoá bản cũ {old.name}: {e}")

def main():
    root = get_project_root()
    print(f"=== BẮT ĐẦU DỌN DẸP & QUẢN LÝ RETENTION CHO DỰ ÁN ===")
    print(f"Thư mục gốc: {root}")
    clean_bytecode_and_caches(root)
    enforce_backup_retention(root, MAX_BACKUP_RETENTION)
    print("=== DỌN DẸP HOÀN TẤT AN TOÀN ===")

if __name__ == "__main__":
    main()
