#!/usr/bin/env python3
"""
tools/restore_original.py
Khôi phục file ngôn ngữ gốc và manifest resinfo.dat của game Reverse: 1999 từ thư mục VietHoa/backups/.
"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
BACKUPS_DIR = PROJECT_ROOT / "backups"

GAME_DAT_PATHS = [
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "Windows" / "configs" / "language" / "json_language_en.json.dat",
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "language" / "json_language_en.json.dat"
]

RESINFO_PATHS = [
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "resinfo.dat",
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "Windows" / "configs" / "resinfo.dat"
]

def restore_backup():
    print("======================================================================")
    print("KHÔI PHỤC DỮ LIỆU GỐC REVERSE: 1999 (TIẾNG ANH NGUYÊN BẢN)")
    print("======================================================================")

    backup_files = sorted(BACKUPS_DIR.glob("json_language_en_original_*.dat"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not backup_files:
        print("[LỖI] Không tìm thấy bản sao lưu gốc nào trong thư mục backups/!")
        return

    latest_backup = backup_files[0]
    print(f">>> Sử dụng bản sao lưu: {latest_backup.name}")

    for dat_path in GAME_DAT_PATHS:
        if dat_path.parent.exists():
            shutil.copy2(latest_backup, dat_path)
            print(f"  [HOÀN NGUYÊN] Đã khôi phục file ngôn ngữ: {dat_path}")

    # Khôi phục resinfo.dat nếu có bản backup
    for r_path in RESINFO_PATHS:
        bak_file = BACKUPS_DIR / f"{r_path.parent.parent.name}_{r_path.name}.bak"
        if bak_file.exists():
            shutil.copy2(bak_file, r_path)
            print(f"  [HOÀN NGUYÊN] Đã khôi phục manifest: {r_path.name} ({r_path.parent.parent.name})")

    print("\n[THÀNH CÔNG] Đã khôi phục hoàn toàn file tiếng Anh nguyên bản cho game!")

if __name__ == "__main__":
    restore_backup()
