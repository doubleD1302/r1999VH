#!/usr/bin/env python3
"""
tools/extract_ui_strings.py
Trích xuất 5000 mục UI cốt lõi thực tế của Reverse: 1999 từ json_language_en.json.dat
(Toàn bộ hệ thống Menu, Sự kiện, Thao tác, Cài đặt, Cửa hàng, Nhiệm vụ từ dải language_10).
Chia thành 5 patch (mỗi patch 1000 mục).
"""

import ctypes
import json
from ctypes import wintypes
from pathlib import Path

KEY = b'@_#*&Reverse2806                '
IV = bytearray(b'!_#@2022_Skyfly)')
SIGNATURE_LENGTH = 48

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = PROJECT_ROOT.parent
SOURCE_DAT = WORKSPACE_ROOT / "Reverse1999en" / "reverse1999_Data" / "StreamingAssets" / "PersistentRoot" / "configs" / "language" / "json_language_en.json.dat"
OUTPUT_DIR = PROJECT_ROOT / "work" / "batches"

def decrypt_language_dat(dat_path: Path) -> list:
    bcrypt = ctypes.windll.bcrypt
    hAlg = wintypes.HANDLE()
    bcrypt.BCryptOpenAlgorithmProvider(ctypes.byref(hAlg), 'AES', None, 0)
    chain_mode = 'ChainingModeCBC\0'.encode('utf-16le')
    bcrypt.BCryptSetProperty(hAlg, 'ChainingMode', chain_mode, len(chain_mode), 0)
    hKey = wintypes.HANDLE()
    bcrypt.BCryptGenerateSymmetricKey(hAlg, ctypes.byref(hKey), None, 0, KEY, len(KEY), 0)

    with open(dat_path, 'rb') as f:
        f.seek(SIGNATURE_LENGTH)
        enc_data = f.read()

    cbResult = wintypes.ULONG(0)
    out_buf = ctypes.create_string_buffer(len(enc_data))
    iv_buf = (ctypes.c_char * len(IV))(*IV)
    status = bcrypt.BCryptDecrypt(hKey, enc_data, len(enc_data), None, iv_buf, len(IV), out_buf, len(out_buf), ctypes.byref(cbResult), 0)
    assert status == 0, f"Decryption failed with status: {status:x}"

    dec_bytes = out_buf.raw[:cbResult.value]
    pad_len = dec_bytes[-1]
    if 1 <= pad_len <= 16:
        dec_bytes = dec_bytes[:-pad_len]

    parsed = json.loads(dec_bytes.decode('utf-8'))
    return parsed[1]

def extract_5000_real_ui():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[EXTRACT] Đang giải mã dữ liệu ngôn ngữ từ: {SOURCE_DAT.name}...")
    entries = decrypt_language_dat(SOURCE_DAT)
    print(f"[OK] Giải mã thành công {len(entries)} mục ngôn ngữ tổng thể.")

    # Lọc 5000 mục UI thực tế đầu tiên (dải language_10, không rỗng)
    ui_items = []
    for k, text in entries:
        if k.startswith("language_10") and text.strip():
            ui_items.append({"id": k, "source": text, "target": ""})
            if len(ui_items) >= 5000:
                break

    print(f"[COLLECT] Đã lọc chính xác {len(ui_items)} mục UI thực tế của game.")

    # Chia thành 5 patch (mỗi patch 1000 mục)
    batch_size = 1000
    for i in range(0, len(ui_items), batch_size):
        patch_num = (i // batch_size) + 1
        patch_items = ui_items[i:i+batch_size]
        patch_file = OUTPUT_DIR / f"ui_patch_{patch_num:02d}.json"
        with open(patch_file, "w", encoding="utf-8") as f:
            json.dump({
                "patch_id": f"UI_PATCH_{patch_num:02d}",
                "count": len(patch_items),
                "items": patch_items
            }, f, ensure_ascii=False, indent=2)
        print(f"  [PATCH] Đã tạo {patch_file.name}: {len(patch_items)} mục UI.")

    full_file = PROJECT_ROOT / "work" / "source" / "ui_5000_raw.json"
    full_file.parent.mkdir(parents=True, exist_ok=True)
    with open(full_file, "w", encoding="utf-8") as f:
        json.dump(ui_items, f, ensure_ascii=False, indent=2)
    print(f"[DONE] Đã lưu file tổng 5000 mục UI tại: {full_file.name}")

if __name__ == "__main__":
    extract_5000_real_ui()
