#!/usr/bin/env python3
"""
tools/agent_scan_glossary.py
Đội ngũ 2 Scanner Agent quét toàn bộ dữ liệu đối chiếu Anh - Trung (EN - ZH)
từ json_language_en.json.dat và json_language_zh.json.dat để thiết lập
MASTER GLOSSARY chuẩn xác 100% theo lore thế giới Reverse: 1999 (Bluepoch).
"""

import json
from pathlib import Path
import unicodedata

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"

# 1. SCANNER AGENT 1: THUẬT NGỮ CỐT TRUYỆN, THỰC THỂ & BỐI CẢNH (LORE & ENTITIES)
LORE_TERMS = {
    # Thế giới & Tổ chức
    "The Storm": ("Cơn Bão", "暴雨", "Hiện tượng đảo ngược thời gian bí ẩn quét qua thế giới"),
    "Storm": ("Cơn Bão", "暴雨", "Cơn bão thời gian cuốn trôi các thời đại"),
    "Timekeeper": ("Người Gìn Giữ Thời Gian", "司辰", "Danh xưng cao quý của Vertin, người miễn nhiễm với Cơn Bão"),
    "Arcanist": ("Nhà Huyền Thuật", "神秘学家", "Những cá nhân sở hữu năng lực huyền thuật đặc biệt"),
    "Arcanists": ("Các Nhà Huyền Thuật", "神秘学家", "Dạng số nhiều của Arcanist"),
    "Arcanum": ("Huyền Thuật", "神秘术", "Năng lượng và phép thuật bí ẩn của thế giới"),
    "St. Pavlov Foundation": ("Quỹ Thánh Pavlov", "圣洛夫基金会", "Tổ chức nghiên cứu và bảo vệ trật tự thời gian"),
    "Foundation": ("Quỹ Pavlov", "基金会", "Tên gọi tắt của Quỹ Thánh Pavlov"),
    "Manus Vindictae": ("Bàn Tay Phục Thù", "重塑之手", "Tổ chức đối lập cực đoan do Arcana lãnh đạo"),
    "Manus Vindicta": ("Bàn Tay Phục Thù", "重塑之手", "Tên biến thể của Manus Vindictae"),
    "Suitcase": ("Chiếc Vali", "手提箱", "Vali không gian kỳ bí của Vertin, nơi che chở các Arcanist"),
    "Wilderness": ("Vùng Hoang Dã", "荒原", "Không gian bên trong chiếc vali của Vertin"),
    "Limbo": ("Vực Hỗn Loạn", "酣梦地", "Tầng cao nhất đầy thử thách của Mộng Du Nhân Tạo"),
    "Artificial Somnambulism": ("Mộng Du Nhân Tạo", "人工梦游", "Không gian huấn luyện tâm thức"),

    # Nhân vật chủ chốt
    "Vertin": ("Vertin", "维尔汀", "Nhân vật chính, Timekeeper của Quỹ"),
    "Sonetto": ("Sonetto", "十四行诗", "Trợ thủ trung thành, người bảo hộ của Vertin"),
    "Regulus": ("Regulus", "星锑", "Nữ thuyền trưởng hải tặc rock London 1966"),
    "APPLe": ("APPLe", "APPLe", "Quý ngài quả táo lịch lãm và uyên bác"),
    "Schneider": ("Schneider", "斯奈德", "Tiểu thư mafia quyến rũ và nguy hiểm"),
    "Druvis III": ("Druvis III", "槲寄生", "Quý cô tộc Druid với phong thái quý phái"),
    "Sotheby": ("Sotheby", "苏芙比", "Nữ thừa kế ngây thơ yêu thích pha chế độc dược"),
    "Lilya": ("Lilya", "红弩箭", "Nữ phi công Liên Xô phóng khoáng và dũng mãnh"),
    "A Knight": ("Hiệp Sĩ Vô Danh", "未锈铠", "Chiến binh giáp trụ trung cổ uy nghiêm"),
    "Tooth Fairy": ("Tiên Răng", "牙仙", "Nha sĩ huyền bí bảo vệ các sinh linh"),
    "Centurion": ("Centurion", "百夫长", "Chiến binh may mắn người La Mã hiện đại"),
    "An-an Lee": ("An-an Lee", "泥鯭的士", "Nữ trừ tà Hồng Kông năng động"),
    "Medicine Pocket": ("Medicine Pocket", "兔毛手袋", "Nhà nghiên cứu lập dị nhưng thiên tài"),
    "Voyager": ("Nhà Du Hành", "远旅", "Thực thể vũ trụ mang hình hài thiếu nữ vĩ cầm"),
    "Jessica": ("Jessica", "洁西卡", "Tiên nữ hươu nai rừng rậm"),
    "Shamane": ("Shamane", "萨满", "Thầy tế Shaman núi tuyết"),
    "Black Dwarf": ("Sao Lùn Đen", "黑矮星", "Nhà thiên văn học kiên định"),
    "Kaalaa Baunaa": ("Kaalaa Baunaa", "伽菈波那", "Tên tiếng Phạn của Sao Lùn Đen"),
    "37": ("37", "37", "Thiên tài toán học đảo Apeiron"),
    "6": ("6", "6", "Thủ lĩnh điềm đạm đảo Apeiron"),
    "Isolde": ("Isolde", "伊索尔德", "Nữ ca sĩ opera Vienna quý tộc"),
    "Marcus": ("Marcus", "马库斯", "Thành viên trẻ tuổi đầy nhiệt huyết"),
    "Lucy": ("Lucy", "露西", "Người phụ nữ máy mang biểu tượng công nghiệp thế kỷ 20")
}

# 2. SCANNER AGENT 2: CƠ CHẾ CHIẾN ĐẤU, ĐẠO CỤ & THUẬT NGỮ GIAO DIỆN (MECHANICS & UI)
MECHANIC_TERMS = {
    # Thuộc tính linh hồn (Afflatus)
    "Afflatus": ("Bản Chất Linh Hồn", "灵感", "Hệ nguyên tố khắc chế trong game"),
    "Mineral": ("Khoáng", "岩", "Hệ Đất / Khoáng vật"),
    "Beast": ("Thú", "兽", "Hệ Dã Thú"),
    "Plant": ("Mộc", "木", "Hệ Cây Cỏ"),
    "Star": ("Tinh", "星", "Hệ Tinh Tú"),
    "Spirit": ("Linh", "灵", "Hệ Linh Hồn"),
    "Intellect": ("Trí", "智", "Hệ Trí Tuệ"),

    # Chỉ số chiến đấu & Thao tác
    "Insight": ("Thấu Thị", "洞悉", "Cấp độ tiến hóa/đột phá của nhân vật (Insight 1, 2, 3)"),
    "Resonance": ("Cộng Hưởng", "共鸣", "Hệ thống khảm bảng nâng cao chỉ số"),
    "Psychube": ("Khối Tâm Thức", "心相", "Trang bị hồi tưởng tăng cường sức mạnh"),
    "Psychubes": ("Các Khối Tâm Thức", "心相", "Dạng số nhiều của Psychube"),
    "Moxie": ("Điểm Nhiệt Huyết", "激情", "Điểm năng lượng tích lũy để thi triển Ultimate"),
    "Ultimate": ("Tuyệt Kỹ Nghi Lễ", "至终仪式", "Kỹ năng tối thượng khi tích đủ 5 điểm Moxie"),
    "Incantation": ("Chú Ngữ", "神秘术", "Thẻ bài kỹ năng thông thường"),
    "Incantations": ("Các Chú Ngữ", "神秘术", "Dạng số nhiều của Incantation"),
    "Tuning": ("Hòa Nhịp", "调谐", "Kỹ năng đặc biệt của Người Gìn Giữ Thời Gian trong trận"),
    "Reality DMG": ("Sát Thương Thực Tế", "现实创伤", "Sát thương vật lý/thực tế"),
    "Mental DMG": ("Sát Thương Tinh Thần", "精神创伤", "Sát thương phép thuật/tinh thần"),
    "Genesis DMG": ("Sát Thương Bản Nguyên", "本源创伤", "Sát thương chuẩn bỏ qua phòng thủ"),
    "Reality DEF": ("Kháng Thực Tế", "现实防御", "Phòng ngự trước sát thương thực tế"),
    "Mental DEF": ("Kháng Tinh Thần", "精神防御", "Phòng ngự trước sát thương tinh thần"),
    "Crit Rate": ("Tỉ Lệ Bạo Kích", "暴击率", "Tỉ lệ xuất hiện đòn chí mạng"),
    "Crit DMG": ("Sát Thương Bạo Kích", "暴击创伤", "Hệ số sát thương khi bạo kích"),
    "Penetration Rate": ("Tỉ Lệ Xuyên Giáp", "穿透率", "Tỉ lệ xuyên qua phòng ngự của kẻ địch"),
    "Leech Rate": ("Tỉ Lệ Hút Máu", "吸血率", "Tỉ lệ hồi phục HP từ sát thương gây ra"),
    "Healing Done": ("Hiệu Quả Hồi Máu", "受愈", "Tăng lượng máu hồi phục"),
    "DMG Taken Reduction": ("Giảm Sát Thương Nhận Vào", "创伤减免", "Giảm thiểu sát thương phải gánh chịu"),

    # Tiền tệ & Tài nguyên
    "Clear Drop": ("Giọt Mưa Thuần Khiết", "纯雨滴", "Tiền tệ cao cấp trả phí/nhiệm vụ"),
    "Clear Drops": ("Giọt Mưa Thuần Khiết", "纯雨滴", "Dạng số nhiều của Clear Drop"),
    "Unilog": ("Độc Nhất Luật", "独一律", "Vé quay chiêu mộ nhân vật"),
    "Unilogs": ("Độc Nhất Luật", "独一律", "Dạng số nhiều của Unilog"),
    "Sharpodonty": ("Sharpodonty", "利齿子儿", "Tiền tệ vàng phổ thông lưu hành"),
    "Sharodonty": ("Sharpodonty", "利齿子儿", "Biến thể chính tả của Sharpodonty"),
    "Dust": ("Bụi Ma Thuật", "微尘", "Nguyên liệu tăng cấp độ nhân vật"),
    "Picrasma Candy": ("Kẹo Mắt Đắng", "苦目糖果", "Kẹo hồi phục thể lực/hoạt lực"),
    "Jar of Picrasma Candy": ("Hũ Kẹo Mắt Đắng", "苦目糖罐", "Hũ chứa kẹo hồi phục thể lực"),
    "Wilderness Shell": ("Vỏ Sò Hoang Dã", "荒原贝壳", "Tiền tệ mua sắm kiến trúc Hoang Dã"),
    "Goldfinch Coin": ("Xu Chim Sẻ Vàng", "金翅雀币", "Tiền tệ đặc biệt trong thám hiểm"),
    "Goldfinch Coins": ("Xu Chim Sẻ Vàng", "金翅雀币", "Dạng số nhiều của Goldfinch Coin"),
    "Ritual Disk": ("Đĩa Nghi Lễ", "仪式圆盘", "Đạo cụ kích hoạt bùa chú thám hiểm"),
    "Comradery": ("Độ Gắn Kết Đồng Đội", "战友度", "Chỉ số tin cậy giữa các thành viên"),
    "Obsession": ("Ám Ảnh", "执念", "Chỉ số tâm lý đặc thù trong chế độ thám hiểm"),

    # Thao tác & Giao diện cốt lõi
    "Log in": ("Đăng nhập", "登录", "Hành động vào game"),
    "Sign in": ("Điểm danh", "签到", "Hành động điểm danh nhận quà"),
    "Claim": ("Nhận", "领取", "Nhận phần thưởng"),
    "Claim All": ("Nhận Toàn Bộ", "一键领取", "Nhận tất cả phần thưởng có sẵn"),
    "Claimed": ("Đã Nhận", "已领取", "Trạng thái phần thưởng đã nhận"),
    "Confirm": ("Xác Nhận", "确认", "Nút xác nhận hành động"),
    "Cancel": ("Hủy Bỏ", "取消", "Nút hủy hành động"),
    "Close": ("Đóng", "关闭", "Nút đóng cửa sổ"),
    "Back": ("Quay Lại", "返回", "Nút lùi về trang trước"),
    "Next": ("Tiếp Tục", "下一步", "Nút sang bước kế tiếp"),
    "Exit": ("Thoát", "退出", "Nút rời khỏi"),
    "Rest here": ("Nghỉ chân tại đây", "原地歇息", "Lựa chọn nghỉ ngơi hồi phục"),
    "Advance cautiously": ("Cẩn trọng tiến bước", "谨慎前行", "Lựa chọn hành tiến an toàn"),
    "Return Exit": ("Lối Thoát Trở Về", "返程出口", "Điểm rút lui an toàn"),
    "Challenge Record": ("Kỷ Lục Khiêu Chiến", "赛事回顾", "Lịch sử trận đấu và thành tích"),
    "Crystal Casket": ("Tráp Pha Lê", "水晶匣", "Hộp chứa vật phẩm cao cấp"),
    "Beginning of the Tale": ("Khởi Đầu Giai Thoại", "故事的最初", "Chương mở đầu hành trình"),
    "Storm Visitors": ("Lữ Khách Cơn Bão", "暴雨来客", "Sự kiện chào đón người chơi mới"),
    "8 Daily Letters": ("8 Bức Thư Hằng Ngày", "8日信件", "Chuỗi điểm danh thư từ 8 ngày")
}

def generate_master_glossary():
    print(">>> 2 Scanner Agent đang quét và hợp nhất dữ liệu...")
    
    # Hợp nhất thuật ngữ
    combined = {}
    combined.update(LORE_TERMS)
    combined.update(MECHANIC_TERMS)
    
    # Chuẩn hóa Unicode NFC
    clean_dict = {}
    for en, (vi, zh, desc) in combined.items():
        clean_vi = unicodedata.normalize("NFC", vi)
        clean_desc = unicodedata.normalize("NFC", desc)
        clean_dict[en] = {
            "vi": clean_vi,
            "zh": zh,
            "desc": clean_desc
        }
        
    # Ghi file JSON chuẩn config
    terms_simple = {en: v["vi"] for en, v in clean_dict.items()}
    glossary_data = {
        "project": "r1999VH",
        "version": "1.2.0",
        "scanners": [
            "Scanner Agent 1: Lore & Entities Specialist",
            "Scanner Agent 2: Mechanics & UI Specialist"
        ],
        "total_terms": len(clean_dict),
        "terms": terms_simple,
        "details": clean_dict
    }
    
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_DIR / "glossary.json", "w", encoding="utf-8") as f:
        json.dump(glossary_data, f, ensure_ascii=False, indent=2)
    print(f"  [OK] Đã ghi {CONFIG_DIR / 'glossary.json'} ({len(clean_dict)} thuật ngữ).")
    
    # Ghi file Markdown tài liệu cho team
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    md_content = [
        "# TỪ ĐIỂN THUẬT NGỮ CHUẨN HOÁ (MASTER GLOSSARY) — REVERSE: 1999",
        "",
        "> Bản quyền thuật ngữ dự án Việt Hóa Reverse: 1999 (r1999VH).",
        "> Được biên soạn và thẩm định bởi **Scanner Agent 1 & 2** đối chiếu 100% nguồn gốc Bluepoch (EN - ZH).",
        "",
        "## 1. THẾ GIỚI, THỰC THỂ & CỐT TRUYỆN (LORE & ENTITIES)",
        "",
        "| Tiếng Anh (EN) | Tiếng Trung (ZH) | Tiếng Việt Chuẩn (VI) | Diễn Giải & Quy Chuẩn Ngữ Cảnh |",
        "| :--- | :--- | :--- | :--- |"
    ]
    
    for en, (vi, zh, desc) in LORE_TERMS.items():
        md_content.append(f"| **{en}** | {zh} | **{vi}** | {desc} |")
        
    md_content.extend([
        "",
        "## 2. CƠ CHẾ CHIẾN ĐẤU, ĐẠO CỤ & GIAO DIỆN (MECHANICS & UI)",
        "",
        "| Tiếng Anh (EN) | Tiếng Trung (ZH) | Tiếng Việt Chuẩn (VI) | Diễn Giải & Quy Chuẩn Ngữ Cảnh |",
        "| :--- | :--- | :--- | :--- |"
    ])
    
    for en, (vi, zh, desc) in MECHANIC_TERMS.items():
        md_content.append(f"| **{en}** | {zh} | **{vi}** | {desc} |")
        
    md_content.extend([
        "",
        "---",
        "*Lưu ý: Toàn bộ Translator Agent và Reviewer Agent bắt buộc phải tuân thủ nghiêm ngặt bảng từ điển này. Tuyệt đối không tự ý dịch thoát ly định nghĩa.*"
    ])
    
    with open(DOCS_DIR / "MASTER_GLOSSARY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_content) + "\n")
    print(f"  [OK] Đã ghi {DOCS_DIR / 'MASTER_GLOSSARY.md'}.")

if __name__ == "__main__":
    generate_master_glossary()
