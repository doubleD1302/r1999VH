#!/usr/bin/env python3
"""
tools/install_patch.py
Công cụ tự động đóng gói (repack) và cài đặt bản dịch 5000 mục UI vào game Reverse: 1999.
- Tự động sao lưu bản gốc vào VietHoa/backups/ (tuân thủ retention <= 2 bản).
- Giải mã json_language_en.json.dat gốc.
- Ghép 5000 mục UI từ 5 patch (work/batches/ui_patch_*.json).
- Mã hóa AES-256-CBC, ghép header 48-byte và ghi đè an toàn vào thư mục game.
"""

import ctypes
from ctypes import wintypes
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

    # Enforce retention <= 2
    from cleanup_workspace import enforce_backup_retention
    enforce_backup_retention(PROJECT_ROOT, max_keep=2)

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

def apply_vietnamese_patch():
    print("======================================================================")
    print("TIẾN TRÌNH CÀI ĐẶT BẢN DỊCH VIỆT HÓA VÀO REVERSE: 1999")
    print("======================================================================")

    # 1. Thu thập chuỗi bản dịch
    patch_strings = load_translated_patches()
    if not patch_strings:
        print("[LỖI] Không tìm thấy dữ liệu bản dịch trong work/batches/!")
        return

    bcrypt, hKey = get_bcrypt_cipher()

    # 2. Xử lý từng file language dat trong game
    for dat_path in GAME_DAT_PATHS:
        if not dat_path.exists():
            print(f"[BỎ QUA] Không tìm thấy tệp: {dat_path}")
            continue

        print(f"\n>>> Đang xử lý: {dat_path.name}")
        print(f"    Vị trí: {dat_path}")

        # Sao lưu
        backup_original_file(dat_path)

        # Đọc dữ liệu gốc
        with open(dat_path, "rb") as f:
            header_48 = f.read(SIGNATURE_LENGTH)
            enc_data = f.read()

        # Giải mã
        parsed = decrypt_data(enc_data, bcrypt, hKey)
        items_list = parsed[1]
        print(f"    Tổng số mục gốc trong file: {len(items_list)}")

        # Ghép patch
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

        # Mã hóa lại
        new_enc_bytes = encrypt_data(parsed, bcrypt, hKey)

        # Ghi đè vào game
        with open(dat_path, "wb") as f:
            f.write(header_48)
            f.write(new_enc_bytes)

        print(f"  [THÀNH CÔNG] Đã ghi đè file ngôn ngữ đã Việt Hóa: {dat_path.name} ({len(header_48) + len(new_enc_bytes):,} bytes)")

    print("\n======================================================================")
    print("HOÀN TẤT CÀI ĐẶT! BÂY GIỜ BẠN CÓ THỂ MỞ GAME ĐỂ TRẢI NGHIỆM TIẾNG VIỆT!")
    print("======================================================================")

if __name__ == "__main__":
    apply_vietnamese_patch()
