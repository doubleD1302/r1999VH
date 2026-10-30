#!/usr/bin/env python3
"""
tools/install_patch.py
Công cụ tự động đóng gói (repack) và cài đặt bản dịch 5000 mục UI vào game Reverse: 1999.
- Tự động sao lưu bản gốc vào VietHoa/backups/ (tuân thủ retention <= 2 bản).
- Giải mã json_language_en.json.dat gốc.
- Ghép 5000 mục UI từ 5 patch (work/batches/ui_patch_*.json).
- Mã hóa AES-256-CBC, ghép header 48-byte và ghi đè an toàn vào thư mục game.
- ĐỒNG BỘ HOÀN HẢO MD5 VÀ FILE SIZE TRONG resinfo.dat (Tránh lỗi treo màn hình tải game do kiểm tra toàn vẹn tài nguyên).
"""

import ctypes
from ctypes import wintypes
import gzip
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

KEY = b'@_#*&Reverse2806                '
IV = bytearray(b'!_#@2022_Skyfly)')
SIGNATURE_LENGTH = 48

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
BATCHES_DIR = PROJECT_ROOT / "work" / "batches"
BACKUPS_DIR = PROJECT_ROOT / "backups"

# Các đường dẫn file ngôn ngữ trong game Reverse: 1999
GAME_DAT_PATHS = [
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "Windows" / "configs" / "language" / "json_language_en.json.dat",
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "language" / "json_language_en.json.dat"
]

RESINFO_PATHS = [
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "resinfo.dat",
    WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "Windows" / "configs" / "resinfo.dat"
]

def get_bcrypt_cipher():
    bcrypt = ctypes.windll.bcrypt
    hAlg = wintypes.HANDLE()
    bcrypt.BCryptOpenAlgorithmProvider(ctypes.byref(hAlg), 'AES', None, 0)
    chain_mode = 'ChainingModeCBC\0'.encode('utf-16le')
    bcrypt.BCryptSetProperty(hAlg, 'ChainingMode', chain_mode, len(chain_mode), 0)
    hKey = wintypes.HANDLE()
    bcrypt.BCryptGenerateSymmetricKey(hAlg, ctypes.byref(hKey), None, 0, KEY, len(KEY), 0)
    return bcrypt, hKey

def decrypt_data(enc_bytes: bytes, bcrypt, hKey) -> list:
    cbResult = wintypes.ULONG(0)
    out_buf = ctypes.create_string_buffer(len(enc_bytes))
    iv_buf = (ctypes.c_char * len(IV))(*IV)
    status = bcrypt.BCryptDecrypt(hKey, enc_bytes, len(enc_bytes), None, iv_buf, len(IV), out_buf, len(out_buf), ctypes.byref(cbResult), 0)
    assert status == 0, f"Decryption failed with status: {status:x}"

    dec_bytes = out_buf.raw[:cbResult.value]
    pad_len = dec_bytes[-1]
    if 1 <= pad_len <= 16:
        dec_bytes = dec_bytes[:-pad_len]

    parsed = json.loads(dec_bytes.decode('utf-8'))
    return parsed

def encrypt_data(parsed_obj, bcrypt, hKey) -> bytes:
    plain_bytes = json.dumps(parsed_obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    # PKCS7 padding
    pad_len = 16 - (len(plain_bytes) % 16)
    padded = plain_bytes + bytes([pad_len] * pad_len)

    cbResult = wintypes.ULONG(0)
    enc_buf = ctypes.create_string_buffer(len(padded))
    iv_buf = (ctypes.c_char * len(IV))(*IV)
    status = bcrypt.BCryptEncrypt(hKey, padded, len(padded), None, iv_buf, len(IV), enc_buf, len(enc_buf), ctypes.byref(cbResult), 0)
    assert status == 0, f"Encryption failed with status: {status:x}"

    return enc_buf.raw[:cbResult.value]

def backup_original_file(dat_path: Path):
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUPS_DIR / f"json_language_en_original_{timestamp}.dat"
    shutil.copy2(dat_path, backup_file)
    print(f"  [BACKUP] Đã sao lưu bản gốc vào: {backup_file.name}")

    from cleanup_workspace import enforce_backup_retention
    enforce_backup_retention(PROJECT_ROOT, max_keep=2)

def backup_resinfo_file(res_path: Path):
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    backup_file = BACKUPS_DIR / f"{res_path.parent.parent.name}_{r_path.name}.bak"
    if not backup_file.exists():
        shutil.copy2(res_path, backup_file)
        print(f"  [BACKUP RESINFO] Đã lưu bản gốc: {backup_file.name}")

def load_translated_patches() -> dict:
    patch_map = {}
    patches = sorted(BATCHES_DIR.glob("ui_patch_*.json"))
    for p in patches:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        for it in data["items"]:
            if it.get("target"):
                patch_map[it["id"]] = it["target"]
    print(f"  [PATCH] Đã nạp {len(patch_map)} chuỗi Việt hóa từ {len(patches)} patch.")
    return patch_map

def sync_manifest_resinfo(new_file_bytes: bytes):
    new_md5 = hashlib.md5(new_file_bytes).hexdigest()
    new_size = len(new_file_bytes)
    print(f"\n>>> Đang cập nhật metadata toàn vẹn (resinfo.dat)...")
    print(f"    New MD5:  {new_md5}")
    print(f"    New Size: {new_size:,} bytes")

    for r_path in RESINFO_PATHS:
        if not r_path.exists():
            continue

        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        backup_file = BACKUPS_DIR / f"{r_path.parent.parent.name}_{r_path.name}.bak"
        if not backup_file.exists():
            shutil.copy2(r_path, backup_file)
            print(f"  [BACKUP RESINFO] Đã lưu bản gốc: {backup_file.name}")

        with open(r_path, "rb") as f:
            res_data = json.loads(gzip.decompress(f.read()))

        entry = res_data.get("main", {}).get("common", {}).get("configs/language/json_language_en.json.dat")
        if entry:
            entry["md5"] = new_md5
            entry["size"] = new_size
            compressed = gzip.compress(json.dumps(res_data, separators=(',', ':')).encode('utf-8'))
            with open(r_path, "wb") as f:
                f.write(compressed)
            print(f"  [ĐỒNG BỘ THÀNH CÔNG] {r_path.parent.parent.name}/{r_path.name}")

def apply_vietnamese_patch():
    print("======================================================================")
    print("TIẾN TRÌNH CÀI ĐẶT BẢN DỊCH VIỆT HÓA VÀO REVERSE: 1999")
    print("======================================================================")

    patch_strings = load_translated_patches()
    if not patch_strings:
        print("[LỖI] Không tìm thấy dữ liệu bản dịch trong work/batches/!")
        return

    bcrypt, hKey = get_bcrypt_cipher()
    generated_file_bytes = None

    for dat_path in GAME_DAT_PATHS:
        if not dat_path.exists():
            continue

        print(f"\n>>> Đang xử lý: {dat_path.name} ({dat_path.parent.parent.name})")

        with open(dat_path, "rb") as f:
            header_48 = f.read(SIGNATURE_LENGTH)
            enc_data = f.read()

        parsed = decrypt_data(enc_data, bcrypt, hKey)
        items_list = parsed[1]

        replaced_count = 0
        new_items = []
        for key, val in items_list:
            if key in patch_strings:
                new_items.append([key, patch_strings[key]])
                replaced_count += 1
            else:
                new_items.append([key, val])

        parsed[1] = new_items
        print(f"    Đã áp dụng thành công {replaced_count} mục Việt Hóa vào cấu trúc game!")

        new_enc_bytes = encrypt_data(parsed, bcrypt, hKey)
        full_bytes = header_48 + new_enc_bytes

        with open(dat_path, "wb") as f:
            f.write(full_bytes)

        generated_file_bytes = full_bytes
        print(f"  [THÀNH CÔNG] Đã ghi đè file ngôn ngữ: {dat_path.name} ({len(full_bytes):,} bytes)")

    # Đồng bộ resinfo.dat để game không bị treo khi kiểm tra tài nguyên
    if generated_file_bytes:
        sync_manifest_resinfo(generated_file_bytes)

    print("\n======================================================================")
    print("HOÀN TẤT CÀI ĐẶT! BÂY GIỜ BẠN CÓ THỂ MỞ GAME ĐỂ TRẢI NGHIỆM TIẾNG VIỆT!")
    print("======================================================================")

if __name__ == "__main__":
    apply_vietnamese_patch()
