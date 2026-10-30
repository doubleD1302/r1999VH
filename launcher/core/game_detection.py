"""
launcher/core/game_detection.py
Tự động quét và nhận diện đường dẫn cài đặt game Reverse: 1999 trên máy tính Windows.
"""

import os
from pathlib import Path
from typing import Optional

def detect_reverse1999_installation() -> Optional[Path]:
    """
    Tìm kiếm thư mục chứa game Reverse: 1999 (chứa reverse1999.exe và reverse1999_Data).
    """
    # 1. Kiểm tra vị trí tương đối từ thư mục VietHoa (nếu VietHoa nằm trong thư mục gốc của game)
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent
    candidates = [
        workspace_root / "Reverse1999en",
        workspace_root,
        Path(r"C:\Program Files\Bluepoch\Reverse1999\Reverse1999en"),
        Path(r"D:\Program Files\Bluepoch\Reverse1999\Reverse1999en"),
        Path(r"F:\bluepoch\reverse1999_global\Reverse1999en"),
    ]

    for candidate in candidates:
        if (candidate / "reverse1999.exe").exists() and (candidate / "reverse1999_Data").exists():
            return candidate.resolve()

    # 2. Quét biến môi trường hoặc các ổ đĩa phổ biến
    for drive in ["C", "D", "E", "F"]:
        base_dir = Path(f"{drive}:/bluepoch")
        if base_dir.exists():
            for root_dir, dirs, files in os.walk(base_dir):
                if "reverse1999.exe" in files and "reverse1999_Data" in dirs:
                    return Path(root_dir).resolve()

    return None

if __name__ == "__main__":
    game_path = detect_reverse1999_installation()
    if game_path:
        print(f"[OK] Đã tìm thấy Reverse: 1999 tại: {game_path}")
    else:
        print("[WARN] Chưa tìm thấy thư mục cài đặt game.")
