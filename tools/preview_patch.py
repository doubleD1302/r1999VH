#!/usr/bin/env python3
"""
tools/preview_patch.py
Công cụ tra cứu, kiểm tra trực quan và xem trước (Preview) 5000 mục UI Việt hóa.
Cách dùng:
  python tools/preview_patch.py --search "Cơn Bão"
  python tools/preview_patch.py --id "language_10000004"
  python tools/preview_patch.py --patch 1 --limit 10
"""

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BATCHES_DIR = PROJECT_ROOT / "work" / "batches"

def load_all_batches():
    items = []
    patches = sorted(BATCHES_DIR.glob("ui_patch_*.json"))
    for p in patches:
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
        for it in d["items"]:
            it["patch"] = p.name
            items.append(it)
    return items

def main():
    parser = argparse.ArgumentParser(description="Xem trước bản dịch Reverse: 1999")
    parser.add_argument("--search", "-s", type=str, help="Tìm kiếm theo từ khóa trong nguồn hoặc bản dịch")
    parser.add_argument("--id", type=str, help="Tra cứu chính xác theo ID (ví dụ: language_10000002)")
    parser.add_argument("--patch", "-p", type=int, choices=[1, 2, 3, 4, 5], help="Xem một patch cụ thể (1-5)")
    parser.add_argument("--limit", "-l", type=int, default=15, help="Giới hạn số kết quả hiển thị (mặc định: 15)")
    args = parser.parse_args()

    items = load_all_batches()

    results = []
    if args.id:
        results = [it for it in items if it["id"] == args.id]
    elif args.search:
        kw = args.search.lower()
        results = [it for it in items if kw in it["source"].lower() or kw in it.get("target", "").lower()]
    elif args.patch:
        patch_file = f"ui_patch_{args.patch:02d}.json"
        results = [it for it in items if it["patch"] == patch_file]
    else:
        results = items[:args.limit]

    print("======================================================================")
    print(f"XEM TRƯỚC BẢN DỊCH REVERSE: 1999 (Tìm thấy {len(results)} kết quả)")
    print("======================================================================")

    for i, it in enumerate(results[:args.limit], 1):
        print(f"\n[{i}] {it['id']} (Nằm trong {it['patch']})")
        print(f"    EN: {it['source']}")
        print(f"    VI: {it.get('target', '[CHƯA DỊCH]')}")

    if len(results) > args.limit:
        print(f"\n... Còn {len(results) - args.limit} kết quả nữa (dùng --limit để xem nhiều hơn).")
    print("======================================================================")

if __name__ == "__main__":
    main()
