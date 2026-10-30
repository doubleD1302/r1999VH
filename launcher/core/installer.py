"""
launcher/core/installer.py
Quản lý việc cài đặt (patch) và gỡ bỏ (restore) bản Việt Hóa cho Reverse: 1999 qua Runtime In-Memory Hook:
- Nạp version.dll và vi_strings.json vào thư mục gốc của game (nơi chứa reverse1999.exe).
- Không can thiệp vào các tệp tĩnh .dat trong StreamingAssets để bảo toàn 100% kiểm tra CDN.
"""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .config import DIST_DIR, BACKUPS_DIR, PROJECT_ROOT

def install_patch(game_path: Path) -> bool:
    """
    Cài đặt bản dịch vào game bằng cách nạp version.dll và vi_strings.json.
    """
    exe_file = game_path / "reverse1999.exe"
    if not game_path.exists() or not exe_file.exists():
        print(f"[ERROR] Đường dẫn game không hợp lệ: {game_path}")
        return False

    print(f"[INSTALL] Đang cài đặt bản Việt Hóa (Runtime Hook) vào: {game_path}...")

    # Đảm bảo dist/ đã có sẵn version.dll và vi_strings.json
    dist_dll = DIST_DIR / "version.dll"
    dist_json = DIST_DIR / "vi_strings.json"

    if not dist_dll.exists() or not dist_json.exists():
        print("[BUILD] Chưa có file phân phối trong dist/, đang tạo mới...")
        installer_tool = PROJECT_ROOT / "tools" / "install_patch.py"
        if installer_tool.exists():
            subprocess.run([sys.executable, str(installer_tool)], check=False)

    if not dist_dll.exists() or not dist_json.exists():
        print("[ERROR] Không thể tạo tệp phân phối trong dist/!")
        return False

    # Sao chép vào thư mục game
    shutil.copy2(dist_dll, game_path / "version.dll")
    shutil.copy2(dist_json, game_path / "vi_strings.json")
    print("  [OK] Đã nạp: version.dll ->", game_path)
    print("  [OK] Đã nạp: vi_strings.json ->", game_path)

    print("[SUCCESS] Cài đặt bản Việt Hóa hoàn tất! Tệp game gốc giữ nguyên 100%.")
    return True

def uninstall_patch(game_path: Path) -> bool:
    """
    Gỡ bỏ bản Việt Hóa (tắt hook) bằng cách xoá version.dll và vi_strings.json.
    """
    hook_dll = game_path / "version.dll"
    vi_json = game_path / "vi_strings.json"

    removed = False
    if hook_dll.exists():
        try:
            hook_dll.unlink()
            print(f"  [OK] Đã gỡ bỏ: {hook_dll.name}")
            removed = True
        except Exception as e:
            print(f"  [WARN] Không thể gỡ bỏ {hook_dll.name}: {e}")

    if vi_json.exists():
        try:
            vi_json.unlink()
            print(f"  [OK] Đã gỡ bỏ: {vi_json.name}")
            removed = True
        except Exception as e:
            pass

    if removed:
        print("[SUCCESS] Đã gỡ bỏ bản Việt Hóa thành công, game trở về tiếng Anh nguyên bản!")
    else:
        print("[INFO] Game hiện đang ở trạng thái tiếng Anh nguyên bản.")
    return True
