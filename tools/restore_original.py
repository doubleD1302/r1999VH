#!/usr/bin/env python3
"""
tools/restore_original.py
Khôi phục game Reverse: 1999 về trạng thái tiếng Anh nguyên bản 100%:
- Gỡ bỏ version.dll (Proxy Hook) và vi_strings.json khỏi thư mục game.
- Đảm bảo các tệp tĩnh .dat và manifest nguyên bản không bị sửa đổi.
"""

import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
BACKUPS_DIR = PROJECT_ROOT / "backups"
GAME_DIR = WORKSPACE_ROOT / "Reverse1999en"

GAME_DAT_PATHS = [
    GAME_DIR / "reverse1999_Data" / "StreamingAssets" / "Windows" / "configs" / "language" / "json_language_en.json.dat",
    GAME_DIR / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "language" / "json_language_en.json.dat"
]

RESINFO_PATHS = [
    GAME_DIR / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "resinfo.dat",
    GAME_DIR / "reverse1999_Data" / "StreamingAssets" / "Windows" / "configs" / "resinfo.dat"
]

def restore_backup(silent: bool = False):
    if not silent:
        print("======================================================================")
        print("KHÔI PHỤC DỮ LIỆU GỐC REVERSE: 1999 (TIẾNG ANH NGUYÊN BẢN)")
        print("======================================================================")

    # 1. Gỡ bỏ runtime hook
    hook_dll = GAME_DIR / "version.dll"
    if hook_dll.exists():
        try:
            hook_dll.unlink()
            if not silent:
                print(f"  [GỠ BỎ HOOK] Đã xoá: {hook_dll.name}")
        except Exception as e:
            if not silent:
                print(f"  [WARN] Không thể xoá {hook_dll.name}: {e}")

    vi_json = GAME_DIR / "vi_strings.json"
    if vi_json.exists():
        try:
            vi_json.unlink()
            if not silent:
                print(f"  [GỠ BỎ] Đã xoá: {vi_json.name}")
        except Exception as e:
            pass

    # 2. Khôi phục tệp ngôn ngữ gốc nếu có bản sao lưu
    backup_files = sorted(BACKUPS_DIR.glob("json_language_en_original_*.dat"), key=lambda x: x.stat().st_mtime, reverse=True)
    if backup_files:
        latest_backup = backup_files[0]
        for dat_path in GAME_DAT_PATHS:
            if dat_path.parent.exists():
                shutil.copy2(latest_backup, dat_path)
                if not silent:
                    print(f"  [HOÀN NGUYÊN] Đã xác nhận file ngôn ngữ gốc: {dat_path.name} ({dat_path.parent.parent.name})")

    # 3. Đồng bộ lại resinfo.dat
    res_persistent = RESINFO_PATHS[0]
    res_windows = RESINFO_PATHS[1]
    if res_persistent.exists() and res_windows.exists():
        shutil.copy2(res_persistent, res_windows)
        if not silent:
            print("  [HOÀN NGUYÊN] Đã đồng bộ manifest resinfo.dat nguyên bản")

    if not silent:
        print("\n[THÀNH CÔNG] Đã khôi phục hoàn toàn file tiếng Anh nguyên bản cho game!")

if __name__ == "__main__":
    restore_backup()
