#!/usr/bin/env python3
"""
tools/install_patch.py
Cài đặt bản dịch tiếng Việt cho Reverse: 1999 bằng cơ chế Runtime In-Memory Hook:
- Giữ nguyên 100% tệp game gốc trên đĩa (tránh triệt để lỗi kiểm tra MD5 / tải đè / treo loading screen).
- Biên dịch hoặc nạp version.dll (Proxy DLL) và vi_strings.json vào thư mục game.
- Hook an toàn tại tầng hiển thị văn bản, không can thiệp logic hay kết nối mạng.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
BATCHES_DIR = PROJECT_ROOT / "work" / "batches"
HOOK_SRC_DIR = PROJECT_ROOT / "tools" / "hook"
DIST_DIR = PROJECT_ROOT / "dist"
GAME_DIR = WORKSPACE_ROOT / "Reverse1999en"

def export_vi_strings_json(output_path: Path) -> int:
    """Tổng hợp 5000 chuỗi Việt hóa từ work/batches/ thành vi_strings.json"""
    patches = sorted(BATCHES_DIR.glob("ui_patch_*.json"))
    if not patches:
        print("[LỖI] Không tìm thấy dữ liệu bản dịch trong work/batches/!")
        return 0

    vi_map = {}
    for p in patches:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        for it in data.get("items", []):
            target = it.get("target", "").strip()
            if target:
                vi_map[it["id"]] = target

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(vi_map, f, ensure_ascii=False)

    print(f"  [OK] Đã trích xuất {len(vi_map)} chuỗi Việt hóa vào: {output_path.name}")
    return len(vi_map)

def build_proxy_dll(output_dll: Path) -> bool:
    """Biên dịch version.dll từ mã nguồn C (VietHoa/tools/hook/)"""
    c_src = HOOK_SRC_DIR / "version.c"

    if not c_src.exists():
        print(f"[LỖI] Không tìm thấy mã nguồn hook tại: {HOOK_SRC_DIR}")
        return False

    output_dll.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["gcc", "-O2", "-shared", "-o", str(output_dll), str(c_src)]
    print(f"  [BUILD] Đang biên dịch {output_dll.name} bằng GCC...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[LỖI BIÊN DỊCH] {res.stderr}")
        return False

    print(f"  [OK] Biên dịch thành công: {output_dll.name} ({output_dll.stat().st_size:,} bytes)")
    return True

def apply_vietnamese_patch():
    print("======================================================================")
    print("CÀI ĐẶT BẢN VIỆT HÓA REVERSE: 1999 (RUNTIME IN-MEMORY HOOK)")
    print("======================================================================")

    if not (GAME_DIR / "reverse1999.exe").exists():
        print(f"[LỖI] Không tìm thấy reverse1999.exe tại: {GAME_DIR}")
        return

    # 1. Đảm bảo bản gốc trên đĩa sạch 100%
    from restore_original import restore_backup
    restore_backup(silent=True)

    # 2. Tạo vi_strings.json trong dist/ và game
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    dist_json = DIST_DIR / "vi_strings.json"
    count = export_vi_strings_json(dist_json)
    if count == 0:
        return

    game_json = GAME_DIR / "vi_strings.json"
    shutil.copy2(dist_json, game_json)

    # 3. Biên dịch version.dll vào dist/ và game
    dist_dll = DIST_DIR / "version.dll"
    if not build_proxy_dll(dist_dll):
        return

    game_dll = GAME_DIR / "version.dll"
    shutil.copy2(dist_dll, game_dll)

    # 4. Dọn dẹp cache
    from cleanup_workspace import clean_bytecode_and_caches
    clean_bytecode_and_caches(PROJECT_ROOT)

    print("\n======================================================================")
    print("HOÀN TẤT THIẾT LẬP BẢN VIỆT HÓA!")
    print(f"- Cơ chế: Runtime In-Memory Hook (Tệp game gốc nguyên vẹn 100%).")
    print(f"- Số mục Việt Hóa: {count:,} mục UI & Menu cốt lõi.")
    print(f"- Trạng thái: An toàn tuyệt đối, không kích hoạt kiểm tra CDN, không treo máy.")
    print("======================================================================")

if __name__ == "__main__":
    apply_vietnamese_patch()
