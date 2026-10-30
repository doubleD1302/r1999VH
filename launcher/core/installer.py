"""
launcher/core/installer.py
Quản lý việc cài đặt (patch) và gỡ bỏ (restore) bản Việt Hóa cho Reverse: 1999.
Tuân thủ nghiêm ngặt quy tắc:
1. Sao lưu tự động trước khi ghi đè.
2. Tự động gọi cleanup_workspace để đảm bảo giữ tối đa 2 bản backup.
"""

import datetime
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .config import DIST_DIR, BACKUPS_DIR, PROJECT_ROOT

def create_backup(target_file: Path) -> Path:
    """Tạo bản sao lưu và lưu vào thư mục backups/"""
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = BACKUPS_DIR / f"backup_{timestamp}"
    backup_folder.mkdir(parents=True, exist_ok=True)
    
    dest = backup_folder / target_file.name
    shutil.copy2(target_file, dest)
    print(f"[BACKUP] Đã sao lưu {target_file.name} sang: {dest}")
    
    # Thực hiện dọn dẹp retention (chỉ giữ tối đa 2 bản sao lưu)
    cleaner_script = PROJECT_ROOT / "tools" / "cleanup_workspace.py"
    if cleaner_script.exists():
        subprocess.run([sys.executable, str(cleaner_script)], check=False)
        
    return dest

def install_patch(game_path: Path) -> bool:
    """
    Cài đặt bản dịch vào game từ thư mục dist/.
    """
    if not game_path.exists() or not (game_path / "reverse1999.exe").exists():
        print(f"[ERROR] Đường dẫn game không hợp lệ: {game_path}")
        return False

    print(f"[INSTALL] Đang cài đặt bản Việt Hóa vào: {game_path}...")
    
    # Kiểm tra dist/ có các file cần nạp hay không
    if not DIST_DIR.exists():
        DIST_DIR.mkdir(parents=True, exist_ok=True)

    patched_files = list(DIST_DIR.glob("*.*"))
    if not patched_files:
        print("[WARN] Chưa có file patch nào trong dist/. Vui lòng tạo bản dịch trước.")
        return False

    # Thực hiện copy các file từ dist/ sang game (kèm backup)
    # Ví dụ: file bundle, font bundle, hoặc language config
    for src in patched_files:
        # Giả định nạp vào thư mục StreamingAssets tương ứng
        rel_dest = game_path / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "bundles" / src.name
        if rel_dest.parent.exists():
            if rel_dest.exists():
                create_backup(rel_dest)
            shutil.copy2(src, rel_dest)
            print(f"[OK] Đã nạp: {src.name} -> {rel_dest}")

    print("[SUCCESS] Cài đặt bản Việt Hóa hoàn tất thành công!")
    return True
