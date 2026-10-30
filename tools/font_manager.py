#!/usr/bin/env python3
"""
tools/font_manager.py
Quản lý, xác thực Unicode tiếng Việt và đóng gói 2 bộ font:
- DVN PT Serif (DesignerVN)
- UVF Didot LT Std (UVF)
vào AssetBundle 'font' của Reverse: 1999.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONTS_RAW = PROJECT_ROOT / "fonts" / "raw"
FONTS_STAGED = PROJECT_ROOT / "fonts" / "staged"
DIST_DIR = PROJECT_ROOT / "dist"

VN_SAMPLE = 'aAàÀáÁảẢãÃạẠăĂằẰắẮẳẲẵẴặẶâÂầẦấẤẩẨẫẪậẬbBcCdDđĐeEèÈéÉẻẺẽẼẹẸêÊềỀếẾểỂễỄệỆfFgGhHiIìÌíÍỉỈĩĨịỊjJkKlLmMnNoOòÒóÓỏỎõÕọỌôÔồỒốỐổỔỗỖộỘơƠờỜớỚởỞỡỠợỢpPqQrRsStTuUùÙúÚủỦũŨụỤưƯừỪứỨửỬữỮựỰvVwWxXyYỳỲýÝỷỶỹỸỵỴzZ'
VN_CODEPOINTS = set(ord(c) for c in VN_SAMPLE)

FONT_MAPPINGS = {
    "regular.ttf": ["dvn pt serif", "pt serif regular", "ptserif-regular", "pt serif"],
    "bold.ttf": ["dvn pt serif bold", "pt serif bold", "ptserif-bold"],
    "italic.ttf": ["dvn pt serif italic", "pt serif italic", "ptserif-italic"],
    "bolditalic.ttf": ["dvn pt serif bold italic", "pt serif bold italic", "ptserif-bolditalic"],
    "didot.ttf": ["uvf didot lt std", "uvf didot", "didot regular", "didot-regular", "didot"],
    "didot_bold_1.ttf": ["uvf didot bold", "didot bold", "didot-bold"],
    "didot_italic_2.ttf": ["uvf didot italic", "didot italic", "didot-italic"]
}

def parse_cmap(font_bytes: bytes) -> set:
    if len(font_bytes) < 12: return set()
    num_tables = struct.unpack('>H', font_bytes[4:6])[0]
    cmap_offset = None
    for i in range(num_tables):
        entry = font_bytes[12 + i*16 : 12 + (i+1)*16]
        if entry[:4] == b'cmap':
            cmap_offset = struct.unpack('>I', entry[8:12])[0]
            break
    if cmap_offset is None: return set()
    
    version, num_subtables = struct.unpack('>HH', font_bytes[cmap_offset:cmap_offset+4])
    supported = set()
    for s in range(num_subtables):
        sub_entry = font_bytes[cmap_offset+4+s*8 : cmap_offset+4+(s+1)*8]
        platform_id, encoding_id, sub_offset = struct.unpack('>HHI', sub_entry)
        table_offset = cmap_offset + sub_offset
        format_val = struct.unpack('>H', font_bytes[table_offset:table_offset+2])[0]
        if format_val == 4:
            length, lang, seg_count_x2 = struct.unpack('>HHH', font_bytes[table_offset+2:table_offset+8])
            seg_count = seg_count_x2 // 2
            end_codes = struct.unpack(f'>{seg_count}H', font_bytes[table_offset+14:table_offset+14+seg_count*2])
            start_codes = struct.unpack(f'>{seg_count}H', font_bytes[table_offset+16+seg_count*2:table_offset+16+seg_count*4])
            id_deltas = struct.unpack(f'>{seg_count}h', font_bytes[table_offset+16+seg_count*4:table_offset+16+seg_count*6])
            for start, end, delta in zip(start_codes, end_codes, id_deltas):
                if end == 0xFFFF and start == 0xFFFF: break
                for cp in range(start, end + 1):
                    supported.add(cp)
        elif format_val == 12:
            format_val, reserved, length, lang, num_groups = struct.unpack('>HHIII', font_bytes[table_offset:table_offset+16])
            for g in range(num_groups):
                start_char, end_char, start_glyph = struct.unpack('>III', font_bytes[table_offset+16+g*12:table_offset+16+(g+1)*12])
                for cp in range(start_char, end_char + 1):
                    supported.add(cp)
    return supported

def verify_and_stage_fonts():
    FONTS_STAGED.mkdir(parents=True, exist_ok=True)
    raw_files = list(FONTS_RAW.glob("*.*"))
    print(f"=== KIỂM TRA THƯ MỤC FONT: {FONTS_RAW} ===")
    print(f"Số lượng file tìm thấy trong fonts/raw/: {len(raw_files)}")

    staged_count = 0
    for target_name, patterns in FONT_MAPPINGS.items():
        matched_file = None
        for rf in raw_files:
            lower_name = rf.stem.lower()
            if any(p in lower_name for p in patterns):
                matched_file = rf
                break

        dest_file = FONTS_STAGED / target_name
        if matched_file:
            data = matched_file.read_bytes()
            supported = parse_cmap(data)
            missing = [chr(cp) for cp in sorted(VN_CODEPOINTS) if cp not in supported]
            pct = (len(VN_CODEPOINTS) - len(missing)) / len(VN_CODEPOINTS) * 100
            
            print(f"[XÁC THỰC] {matched_file.name} -> {target_name}: Độ phủ tiếng Việt: {pct:.1f}%")
            if missing:
                print(f"  [CẢNH BÁO] Thiếu {len(missing)} ký tự: {''.join(missing[:15])}...")
            else:
                print(f"  [HOÀN HẢO] Hỗ trợ 100% đầy đủ dấu tiếng Việt!")

            shutil.copy2(matched_file, dest_file)
            staged_count += 1
        elif dest_file.exists():
            staged_count += 1
            print(f"[ĐÃ CÓ SẴN] {target_name} đã nằm trong staged/")
        else:
            print(f"[CHƯA CÓ] Chưa tìm thấy font phù hợp cho {target_name} ({', '.join(patterns)})")

    print(f"\nTổng kết: Đã chuẩn bị {staged_count}/{len(FONT_MAPPINGS)} file font trong {FONTS_STAGED}.")
    if staged_count < len(FONT_MAPPINGS):
        print("\n[HƯỚNG DẪN BỔ SUNG]")
        print("Vui lòng tải 2 bộ font:")
        print("1. DVN PT Serif (Regular, Bold, Italic, Bold Italic)")
        print("2. UVF Didot LT Std (Regular, Bold, Italic)")
        print(f"và copy vào thư mục: {FONTS_RAW.resolve()}")

def main():
    verify_and_stage_fonts()

if __name__ == "__main__":
    main()
