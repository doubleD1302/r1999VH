#!/usr/bin/env python3
"""
tools/git_push_release.py
Tự động kiểm tra quy chuẩn Release (tiêu đề chỉ chứa số phiên bản, mô tả <= 100 từ),
thực hiện commit và push lên kho lưu trữ GitHub https://github.com/doubleD1302/r1999VH.
"""

import re
import subprocess
import sys
from pathlib import Path

def validate_release_meta(title: str, body: str) -> None:
    # 1. Kiểm tra tiêu đề: CHỈ chứa số phiên bản (X.Y.Z)
    title = title.strip()
    if not re.fullmatch(r"^[0-9]+(?:\.[0-9]+)*$", title):
        raise ValueError(
            f"LỖI TIÊU ĐỀ RELEASE: '{title}' không hợp lệ!\n"
            "Tiêu đề BẮT BUỘC CHỈ được chứa số phiên bản (ví dụ: '0.1.0' hoặc '1.0.0'). "
            "Tuyệt đối không kèm chữ 'v', 'Release', tên dự án hay emoji!"
        )

    # 2. Kiểm tra mô tả: Tối đa 100 từ
    words = body.strip().split()
    word_count = len(words)
    if word_count > 100:
        raise ValueError(
            f"LỖI MÔ TẢ RELEASE: Độ dài {word_count} từ vượt quá giới hạn tối đa 100 từ!\n"
            "Vui lòng rút gọn nội dung súc tích hơn."
        )

    print(f"[OK] Xác thực Release Meta hợp lệ: Tiêu đề = '{title}', Độ dài mô tả = {word_count}/100 từ.")

def run_git_push(commit_msg: str, project_dir: Path):
    print(f"[GIT] Đang kiểm tra trạng thái git tại: {project_dir}")
    
    # 1. git add .
    subprocess.run(["git", "add", "."], cwd=project_dir, check=True)
    
    # 2. Check if anything to commit
    status = subprocess.run(["git", "status", "--porcelain"], cwd=project_dir, capture_output=True, text=True, check=True)
    if not status.stdout.strip():
        print("[GIT] Không có thay đổi mới nào cần commit.")
        return

    # 3. git commit
    print(f"[GIT] Đang commit với thông điệp: {commit_msg}")
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=project_dir, check=True)

    # 4. git push origin main
    print("[GIT] Đang push lên remote origin main...")
    subprocess.run(["git", "push", "origin", "main"], cwd=project_dir, check=True)
    print("[GIT] Push thành công lên https://github.com/doubleD1302/r1999VH!")

def main():
    root = Path(__file__).resolve().parent.parent
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    else:
        commit_msg = "chore: update localization core assets and workspace tools"
        
    run_git_push(commit_msg, root)

if __name__ == "__main__":
    main()
