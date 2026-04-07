"""
Tử Vi API using iztro-py for correct calculations.

This module provides Tử Vi chart calculations using the iztro-py library
which implements the correct traditional Vietnamese astrology algorithms.
"""

from typing import Dict, List, Optional
from iztro_py import by_solar
from datetime import datetime
from tu_vi.interpretation_service import get_palace_interpretation, get_palace_meaning_by_name, get_star_interpretation


# Enum mappings for decadal stems/branches
HEAVENLY_STEM_MAP = {
    'jiaHeavenly': '甲', 'yiHeavenly': '乙', 'bingHeavenly': '丙',
    'dingHeavenly': '丁', 'wuHeavenly': '戊', 'jiHeavenly': '己',
    'gengHeavenly': '庚', 'xinHeavenly': '辛', 'renHeavenly': '壬',
    'guiHeavenly': '癸'
}
EARTHLY_BRANCH_MAP = {
    'ziEarthly': '子', 'chouEarthly': '丑', 'yinEarthly': '寅',
    'maoEarthly': '卯', 'chenEarthly': '辰', 'siEarthly': '巳',
    'wuEarthly': '午', 'weiEarthly': '未', 'shenEarthly': '申',
    'youEarthly': '酉', 'xuEarthly': '戌', 'haiEarthly': '亥'
}

# English palace name translations (iztro-py)
ENGLISH_PALACE_TRANSLATIONS = {
    'soulPalace': 'Mệnh',
    'parentsPalace': 'Phụ Mẫu',
    'siblingsPalace': 'Huynh Đệ',
    'childrenPalace': 'Tử Tức',
    'spiritPalace': 'Phúc Đức',
    'propertyPalace': 'Điền Trạch',
    'careerPalace': 'Quan Lộc',
    'surfacePalace': 'Thiên Di',
    'wealthPalace': 'Tài Bạch',
    'healthPalace': 'Tật Ách',
    'friendsPalace': 'Nô Bộc',
    'spousePalace': 'Phu Thê',
}

# English star name translations (iztro-py) - Major stars (Maj) and Minor stars (Min)
ENGLISH_STAR_TRANSLATIONS = {
    # Major stars
    'ziweiMaj': 'Tử Vi',
    'tianjiMaj': 'Thiên Cơ',
    'taiyangMaj': 'Thái Dương',
    'wuquMaj': 'Vũ Khúc',
    'tiantongMaj': 'Thiên Đồng',
    'lianzhenMaj': 'Liêm Trinh',
    'tianfuMaj': 'Thiên Phủ',
    'taiyinMaj': 'Thái Âm',
    'tanlangMaj': 'Tham Lang',
    'jumenMaj': 'Cự Môn',
    'tianxiangMaj': 'Thiên Tướng',
    'tianliangMaj': 'Thiên Lương',
    'qishaMaj': 'Thất Sát',
    'pojunMaj': 'Phá Quân',
    # Minor stars
    'huoxingMin': 'Hỏa Tinh',
    'lucreMin': 'Lộc Tồn',
    'tiankuiMin': 'Thiên Khôi',
    'tianyueMin': 'Thiên Việt',
    'yuekaoMin': 'Nguyệt Khảo',
    'hongyanMin': 'Hồng Yến',
    'tianmaMin': 'Thiên Mã',
    'guashenMin': 'Quả Sao',
    'tiankongMin': 'Thiên Không',
    'bajieMin': 'Bạch Xà',
    'zhongmingMin': 'Trung Minh',
    'tianruiMin': 'Thiên Thọ',
    'jiekuiMin': 'Tiệp Khúc',
    'zuofuMin': 'Tả Phụ',
    'youbiMin': 'Hữu Bật',
    'wenquMin': 'Văn Khúc',
    'wenchangMin': 'Văn Xương',
    'dijieMin': 'Địa Kiếp',
    'dikongMin': 'Địa Không',
    'lucunMin': 'Lộc Tồn',
    'qingyangMin': 'Kình Dương',
    'lingxingMin': 'Linh Tinh',
    'tuoluoMin': 'Đà La',
    # Adjective (Grade B) stars
    'hongluan': 'Hồng Loan', 'tianxi': 'Thiên Hỷ',
    'tianxing': 'Thiên Hình', 'tianyao': 'Thiên Diêu',
    'tianku': 'Thiên Khốc', 'tianxu': 'Thiên Hư',
    'tiankong': 'Tuần Không', 'tiande': 'Thiên Đức',
    'tianguan': 'Thiên Quan', 'tiangui': 'Thiên Quý',
    'tianfuAdj': 'Thiên Phúc', 'tiancai': 'Thiên Tài',
    'tianchu': 'Thiên Trù', 'tianshou': 'Thiên Thọ',
    'tianshang': 'Thiên Thương', 'tianshi': 'Thiên Sứ',
    'tianwu': 'Thiên Vu', 'tianyue': 'Thiên Nguyệt',
    'longchi': 'Long Trì', 'fengge': 'Phượng Các',
    'santai': 'Tam Thai', 'taifu': 'Thai Phụ',
    'enguang': 'Ân Quang', 'tiankongAdj': 'Thiên Không',
    'guchen': 'Cô Thần', 'guasu': 'Quả Tú',
    'posui': 'Phá Toái', 'feilian': 'Phi Liêm',
    'xianchi': 'Hàm Trì', 'huagai': 'Hoa Cái',
    'jieshen': 'Giải Thần', 'nianjie': 'Niên Giải',
    'kongwang': 'Triệt Lộ', 'xunkong': 'Tuần Không',
    'yinsha': 'Âm Sát', 'yuede': 'Nguyệt Đức',
    'jielu': 'Triệt Lộ', 'fenggao': 'Phong Cáo',
    'bazuo': 'Bát Tọa',
}

# ── Stars allowed in adjective_stars per "an sao tu vi.pdf" whitelist ──────────
ALLOWED_ADJ_STARS = {
    # By Địa Chi (from iztro-py — positions correct for VN tradition)
    'Hồng Loan', 'Thiên Hỷ', 'Thiên Khốc', 'Thiên Hư',
    'Thiên Đức', 'Nguyệt Đức', 'Long Trì', 'Phượng Các',
    'Cô Thần', 'Quả Tú', 'Phá Toái', 'Hoa Cái',
    # By Thiên Can (from iztro-py)
    'Tuần Không', 'Triệt Lộ',
    # By giờ (from iztro-py)
    'Thai Phụ', 'Phong Cáo',
    # By tháng (from iztro-py)
    'Thiên Hình', 'Thiên Diêu',
    # NOTE: Giải Thần, Thiên Trù, Thiên Phúc, Thiên Quan, Thiên Không,
    # Ân Quang, Tam Thai, Bát Tọa, Thiên Tài, Thiên Thọ, Thiên Thương,
    # Thiên Sứ, Địa Võng — all computed by VN formula below (not from iztro-py)
}

# ── Lookup tables for stars NOT provided by iztro-py ────────────────────────
# By Thiên Can (year's heavenly stem)
_LUU_HA_BY_CAN = {
    "Giáp":"Dậu", "Ất":"Tuất", "Bính":"Mùi", "Đinh":"Thìn",
    "Mậu":"Tỵ",  "Kỷ":"Ngọ",  "Canh":"Thân","Tân":"Mão",
    "Nhâm":"Hợi","Quý":"Dần",
}
_QUOC_AN_BY_CAN = {
    "Giáp":"Tuất","Ất":"Hợi", "Bính":"Sửu","Đinh":"Dần",
    "Mậu":"Sửu", "Kỷ":"Dần", "Canh":"Thìn","Tân":"Tỵ",
    "Nhâm":"Mùi","Quý":"Thân",
}
_DUONG_PHU_BY_CAN = {
    "Giáp":"Mùi","Ất":"Thân","Bính":"Tuất","Đinh":"Hợi",
    "Mậu":"Tuất","Kỷ":"Hợi","Canh":"Sửu", "Tân":"Dần",
    "Nhâm":"Thìn","Quý":"Tỵ",
}
_VAN_TINH_BY_CAN = {
    "Giáp":"Tỵ","Ất":"Ngọ","Bính":"Thân","Đinh":"Dậu",
    "Mậu":"Thân","Kỷ":"Dậu","Canh":"Hợi","Tân":"Tý",
    "Nhâm":"Dậu","Quý":"Mão",
}

# By Địa Chi (year's earthly branch)
_DAO_HOA_BY_CHI = {
    "Tý":"Dậu","Sửu":"Ngọ","Dần":"Mão","Mão":"Tý",
    "Thìn":"Dậu","Tỵ":"Ngọ","Ngọ":"Mão","Mùi":"Tý",
    "Thân":"Dậu","Dậu":"Ngọ","Tuất":"Mão","Hợi":"Tý",
}
_KIEP_SAT_BY_CHI = {
    "Tý":"Tỵ","Sửu":"Dần","Dần":"Hợi","Mão":"Thân",
    "Thìn":"Tỵ","Tỵ":"Dần","Ngọ":"Hợi","Mùi":"Thân",
    "Thân":"Tỵ","Dậu":"Dần","Tuất":"Hợi","Hợi":"Thân",
}

# By lunar month
_THIEN_Y_BY_MONTH = {
    1:"Sửu",2:"Dần",3:"Mão",4:"Thìn",5:"Tỵ",6:"Ngọ",
    7:"Mùi",8:"Thân",9:"Dậu",10:"Tuất",11:"Hợi",12:"Tý",
}
_THIEN_GIAI_BY_MONTH = {
    1:"Thân",2:"Dậu",3:"Tuất",4:"Hợi",5:"Tý",6:"Sửu",
    7:"Dần",8:"Mão",9:"Thìn",10:"Tỵ",11:"Ngọ",12:"Mùi",
}
_DIA_GIAI_BY_MONTH = {
    1:"Mùi",2:"Thân",3:"Dậu",4:"Tuất",5:"Hợi",6:"Tý",
    7:"Sửu",8:"Dần",9:"Mão",10:"Thìn",11:"Tỵ",12:"Ngọ",
}

# By Thiên Can — stars not correctly placed by iztro-py (§5.24, §5.30)
_THIEN_TRU_BY_CAN = {
    "Giáp":"Tỵ",  "Ất":"Ngọ",  "Bính":"Tý",  "Đinh":"Tỵ",
    "Mậu":"Ngọ",  "Kỷ":"Thân", "Canh":"Dần", "Tân":"Ngọ",
    "Nhâm":"Dậu", "Quý":"Tuất",
}
_THIEN_PHUC_BY_CAN = {
    "Giáp":"Dậu", "Ất":"Thân", "Bính":"Tý",  "Đinh":"Hợi",
    "Mậu":"Mão",  "Kỷ":"Dần",  "Canh":"Ngọ", "Tân":"Tỵ",
    "Nhâm":"Ngọ", "Quý":"Tỵ",
}
_THIEN_QUAN_BY_CAN = {
    "Giáp":"Mùi", "Ất":"Thìn", "Bính":"Tỵ",  "Đinh":"Dần",
    "Mậu":"Mão",  "Kỷ":"Dậu",  "Canh":"Hợi", "Tân":"Dậu",
    "Nhâm":"Tuất","Quý":"Ngọ",
}

# Earthly-branch-based palace position (fixed Thiên Bàn cells)
# Each palace sits at its earthly branch cell regardless of palace name
EARTHLY_BRANCH_POSITION = {
    'ziEarthly':   1,   # Tý
    'chouEarthly': 2,   # Sửu
    'yinEarthly':  3,   # Dần
    'maoEarthly':  4,   # Mão
    'chenEarthly': 5,   # Thìn
    'siEarthly':   6,   # Tỵ
    'wuEarthly':   7,   # Ngọ
    'weiEarthly':  8,   # Mùi
    'shenEarthly': 9,   # Thân
    'youEarthly':  10,  # Dậu
    'xuEarthly':   11,  # Tuất
    'haiEarthly':  12,  # Hợi
}


_CAN_LIST = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
_CHI_LIST = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]

NAP_AM_TABLE = {
    ("Giáp","Tý"):   "Hải Trung Kim",  ("Ất","Sửu"):    "Hải Trung Kim",
    ("Bính","Dần"):  "Lô Trung Hỏa",   ("Đinh","Mão"):   "Lô Trung Hỏa",
    ("Mậu","Thìn"):  "Đại Lâm Mộc",    ("Kỷ","Tỵ"):     "Đại Lâm Mộc",
    ("Canh","Ngọ"):  "Lộ Bàng Thổ",    ("Tân","Mùi"):    "Lộ Bàng Thổ",
    ("Nhâm","Thân"): "Kiếm Phong Kim",  ("Quý","Dậu"):    "Kiếm Phong Kim",
    ("Giáp","Tuất"): "Sơn Đầu Hỏa",    ("Ất","Hợi"):     "Sơn Đầu Hỏa",
    ("Bính","Tý"):   "Giản Hạ Thủy",   ("Đinh","Sửu"):   "Giản Hạ Thủy",
    ("Mậu","Dần"):   "Thành Đầu Thổ",  ("Kỷ","Mão"):     "Thành Đầu Thổ",
    ("Canh","Thìn"): "Bạch Lạp Kim",   ("Tân","Tỵ"):     "Bạch Lạp Kim",
    ("Nhâm","Ngọ"):  "Dương Liễu Mộc", ("Quý","Mùi"):    "Dương Liễu Mộc",
    ("Giáp","Thân"): "Tuyền Trung Thủy",("Ất","Dậu"):    "Tuyền Trung Thủy",
    ("Bính","Tuất"): "Ốc Thượng Thổ",  ("Đinh","Hợi"):   "Ốc Thượng Thổ",
    ("Mậu","Tý"):    "Tích Lịch Hỏa",  ("Kỷ","Sửu"):    "Tích Lịch Hỏa",
    ("Canh","Dần"):  "Tùng Bách Mộc",  ("Tân","Mão"):    "Tùng Bách Mộc",
    ("Nhâm","Thìn"): "Trường Lưu Thủy",("Quý","Tỵ"):    "Trường Lưu Thủy",
    ("Giáp","Ngọ"):  "Sa Trung Kim",   ("Ất","Mùi"):     "Sa Trung Kim",
    ("Bính","Thân"): "Sơn Hạ Hỏa",    ("Đinh","Dậu"):   "Sơn Hạ Hỏa",
    ("Mậu","Tuất"):  "Bình Địa Mộc",   ("Kỷ","Hợi"):    "Bình Địa Mộc",
    ("Canh","Tý"):   "Bích Thượng Thổ",("Tân","Sửu"):   "Bích Thượng Thổ",
    ("Nhâm","Dần"):  "Kim Bạch Kim",   ("Quý","Mão"):   "Kim Bạch Kim",
    ("Giáp","Thìn"): "Phúc Đăng Hỏa", ("Ất","Tỵ"):     "Phúc Đăng Hỏa",
    ("Bính","Ngọ"):  "Thiên Hà Thủy", ("Đinh","Mùi"):  "Thiên Hà Thủy",
    ("Mậu","Thân"):  "Đại Dịch Thổ",  ("Kỷ","Dậu"):   "Đại Dịch Thổ",
    ("Canh","Tuất"): "Thoa Xuyến Kim",("Tân","Hợi"):   "Thoa Xuyến Kim",
    ("Nhâm","Tý"):   "Tang Triết Mộc", ("Quý","Sửu"):  "Tang Triết Mộc",
    ("Giáp","Dần"):  "Đại Khê Thủy",  ("Ất","Mão"):   "Đại Khê Thủy",
    ("Bính","Thìn"): "Sa Trung Thổ",  ("Đinh","Tỵ"):  "Sa Trung Thổ",
    ("Mậu","Ngọ"):   "Thiên Thượng Hỏa",("Kỷ","Mùi"):"Thiên Thượng Hỏa",
    ("Canh","Thân"): "Thạch Lựu Mộc", ("Tân","Dậu"):  "Thạch Lựu Mộc",
    ("Nhâm","Tuất"): "Đại Hải Thủy",  ("Quý","Hợi"):  "Đại Hải Thủy",
}

# Vietnamese Tử Vi brightness table — overrides iztro-py (Chinese) values
# Format: (star_name_vn, dia_chi_vn) -> brightness
VN_BRIGHTNESS_TABLE = {
    # Nguồn: chinh tinh.pdf + mieudia.pdf
    # Miếu địa từ mieudia.pdf ghi đè, các trạng thái khác giữ nguyên theo chinh tinh.pdf

    # TỬ VI — Miếu: Tỵ,Ngọ,Dần,Thân | Vượng: Thìn,Tuất | Đắc: Sửu,Mùi,Hợi,Tý | Bình Hòa: Mão,Dậu
    ("Tử Vi","Tý"):"Đắc",      ("Tử Vi","Sửu"):"Đắc",    ("Tử Vi","Dần"):"Miếu",
    ("Tử Vi","Mão"):"Bình Hòa", ("Tử Vi","Thìn"):"Vượng", ("Tử Vi","Tỵ"):"Miếu",
    ("Tử Vi","Ngọ"):"Miếu",    ("Tử Vi","Mùi"):"Đắc",    ("Tử Vi","Thân"):"Miếu",
    ("Tử Vi","Dậu"):"Bình Hòa", ("Tử Vi","Tuất"):"Vượng", ("Tử Vi","Hợi"):"Đắc",

    # THIÊN CƠ — Miếu: Thìn,Tuất,Mão,Dậu | Vượng: Tỵ,Thân,Mùi | Đắc: Ngọ,Tý,Sửu | Hãm: Dần,Hợi
    ("Thiên Cơ","Tý"):"Đắc",   ("Thiên Cơ","Sửu"):"Đắc",   ("Thiên Cơ","Dần"):"Hãm",
    ("Thiên Cơ","Mão"):"Miếu", ("Thiên Cơ","Thìn"):"Miếu", ("Thiên Cơ","Tỵ"):"Vượng",
    ("Thiên Cơ","Ngọ"):"Đắc",  ("Thiên Cơ","Mùi"):"Vượng", ("Thiên Cơ","Thân"):"Vượng",
    ("Thiên Cơ","Dậu"):"Miếu", ("Thiên Cơ","Tuất"):"Miếu", ("Thiên Cơ","Hợi"):"Hãm",

    # THÁI DƯƠNG — Miếu: Tỵ,Ngọ | Vượng: Dần,Mão,Thìn | Đắc: Sửu,Mùi | Hãm: Thân,Dậu,Tuất,Hợi,Tý
    ("Thái Dương","Tý"):"Hãm",  ("Thái Dương","Sửu"):"Đắc",  ("Thái Dương","Dần"):"Vượng",
    ("Thái Dương","Mão"):"Vượng", ("Thái Dương","Thìn"):"Vượng", ("Thái Dương","Tỵ"):"Miếu",
    ("Thái Dương","Ngọ"):"Miếu", ("Thái Dương","Mùi"):"Đắc", ("Thái Dương","Thân"):"Hãm",
    ("Thái Dương","Dậu"):"Hãm", ("Thái Dương","Tuất"):"Hãm", ("Thái Dương","Hợi"):"Hãm",

    # VŨ KHÚC — Miếu: Thìn,Tuất,Sửu,Mùi | Vượng: Dần,Thân,Tý,Ngọ | Đắc: Mão,Dậu | Hãm: Tỵ,Hợi
    ("Vũ Khúc","Tý"):"Vượng", ("Vũ Khúc","Sửu"):"Miếu",  ("Vũ Khúc","Dần"):"Vượng",
    ("Vũ Khúc","Mão"):"Đắc",  ("Vũ Khúc","Thìn"):"Miếu", ("Vũ Khúc","Tỵ"):"Hãm",
    ("Vũ Khúc","Ngọ"):"Vượng", ("Vũ Khúc","Mùi"):"Miếu", ("Vũ Khúc","Thân"):"Vượng",
    ("Vũ Khúc","Dậu"):"Đắc",  ("Vũ Khúc","Tuất"):"Miếu", ("Vũ Khúc","Hợi"):"Hãm",

    # THIÊN ĐỒNG — Miếu: Dần,Thân | Vượng: Tý | Đắc: Mão,Tỵ,Hợi | Hãm: Ngọ,Dậu,Thìn,Tuất,Sửu,Mùi
    ("Thiên Đồng","Tý"):"Vượng", ("Thiên Đồng","Sửu"):"Hãm",  ("Thiên Đồng","Dần"):"Miếu",
    ("Thiên Đồng","Mão"):"Đắc",  ("Thiên Đồng","Thìn"):"Hãm",  ("Thiên Đồng","Tỵ"):"Đắc",
    ("Thiên Đồng","Ngọ"):"Hãm",  ("Thiên Đồng","Mùi"):"Hãm",  ("Thiên Đồng","Thân"):"Miếu",
    ("Thiên Đồng","Dậu"):"Hãm",  ("Thiên Đồng","Tuất"):"Hãm",  ("Thiên Đồng","Hợi"):"Đắc",

    # LIÊM TRINH — Miếu: Thìn,Tuất | Vượng: Dần,Thân,Tý,Ngọ | Đắc: Sửu,Mùi | Hãm: Tỵ,Hợi,Mão,Dậu
    ("Liêm Trinh","Tý"):"Vượng", ("Liêm Trinh","Sửu"):"Đắc",  ("Liêm Trinh","Dần"):"Vượng",
    ("Liêm Trinh","Mão"):"Hãm",  ("Liêm Trinh","Thìn"):"Miếu", ("Liêm Trinh","Tỵ"):"Hãm",
    ("Liêm Trinh","Ngọ"):"Vượng", ("Liêm Trinh","Mùi"):"Đắc", ("Liêm Trinh","Thân"):"Vượng",
    ("Liêm Trinh","Dậu"):"Hãm",  ("Liêm Trinh","Tuất"):"Miếu", ("Liêm Trinh","Hợi"):"Hãm",

    # THIÊN PHỦ — Miếu: Dần,Thân,Tý,Ngọ | Vượng: Thìn,Tuất | Đắc: Tỵ,Mùi,Hợi | Bình Hòa: Sửu,Mão,Dậu
    ("Thiên Phủ","Tý"):"Miếu",    ("Thiên Phủ","Sửu"):"Bình Hòa", ("Thiên Phủ","Dần"):"Miếu",
    ("Thiên Phủ","Mão"):"Bình Hòa", ("Thiên Phủ","Thìn"):"Vượng",  ("Thiên Phủ","Tỵ"):"Đắc",
    ("Thiên Phủ","Ngọ"):"Miếu",   ("Thiên Phủ","Mùi"):"Đắc",    ("Thiên Phủ","Thân"):"Miếu",
    ("Thiên Phủ","Dậu"):"Bình Hòa", ("Thiên Phủ","Tuất"):"Vượng", ("Thiên Phủ","Hợi"):"Đắc",

    # THÁI ÂM — Miếu: Dậu,Tuất,Hợi | Vượng: Thân,Tý | Đắc: Sửu,Mùi | Hãm: Dần,Mão,Thìn,Tỵ,Ngọ
    ("Thái Âm","Tý"):"Vượng", ("Thái Âm","Sửu"):"Đắc",  ("Thái Âm","Dần"):"Hãm",
    ("Thái Âm","Mão"):"Hãm",  ("Thái Âm","Thìn"):"Hãm",  ("Thái Âm","Tỵ"):"Hãm",
    ("Thái Âm","Ngọ"):"Hãm",  ("Thái Âm","Mùi"):"Đắc",  ("Thái Âm","Thân"):"Vượng",
    ("Thái Âm","Dậu"):"Miếu", ("Thái Âm","Tuất"):"Miếu", ("Thái Âm","Hợi"):"Miếu",

    # THAM LANG — Miếu: Sửu,Mùi | Vượng: Thìn,Tuất | Đắc: Dần,Thân | Hãm: Tỵ,Hợi,Tý,Ngọ,Mão,Dậu
    ("Tham Lang","Tý"):"Hãm",  ("Tham Lang","Sửu"):"Miếu", ("Tham Lang","Dần"):"Đắc",
    ("Tham Lang","Mão"):"Hãm",  ("Tham Lang","Thìn"):"Vượng", ("Tham Lang","Tỵ"):"Hãm",
    ("Tham Lang","Ngọ"):"Hãm",  ("Tham Lang","Mùi"):"Miếu", ("Tham Lang","Thân"):"Đắc",
    ("Tham Lang","Dậu"):"Hãm",  ("Tham Lang","Tuất"):"Vượng", ("Tham Lang","Hợi"):"Hãm",

    # CỰ MÔN — Miếu: Mão,Dậu | Vượng: Tý,Ngọ,Dần | Đắc: Thân,Hợi | Hãm: Tỵ,Thìn,Tuất,Sửu,Mùi
    ("Cự Môn","Tý"):"Vượng", ("Cự Môn","Sửu"):"Hãm",  ("Cự Môn","Dần"):"Vượng",
    ("Cự Môn","Mão"):"Miếu", ("Cự Môn","Thìn"):"Hãm",  ("Cự Môn","Tỵ"):"Hãm",
    ("Cự Môn","Ngọ"):"Vượng", ("Cự Môn","Mùi"):"Hãm",  ("Cự Môn","Thân"):"Đắc",
    ("Cự Môn","Dậu"):"Miếu", ("Cự Môn","Tuất"):"Hãm",  ("Cự Môn","Hợi"):"Đắc",

    # THIÊN TƯỚNG — Miếu: Dần,Thân | Vượng: Tý,Ngọ,Thìn,Tuất | Đắc: Sửu,Mùi,Tỵ,Hợi | Hãm: Mão,Dậu
    ("Thiên Tướng","Tý"):"Vượng", ("Thiên Tướng","Sửu"):"Đắc",  ("Thiên Tướng","Dần"):"Miếu",
    ("Thiên Tướng","Mão"):"Hãm",  ("Thiên Tướng","Thìn"):"Vượng", ("Thiên Tướng","Tỵ"):"Đắc",
    ("Thiên Tướng","Ngọ"):"Vượng", ("Thiên Tướng","Mùi"):"Đắc",  ("Thiên Tướng","Thân"):"Miếu",
    ("Thiên Tướng","Dậu"):"Hãm",  ("Thiên Tướng","Tuất"):"Vượng", ("Thiên Tướng","Hợi"):"Đắc",

    # THIÊN LƯƠNG — Miếu: Thìn,Ngọ,Tuất | Vượng: Dần,Thân,Tý,Mão | Đắc: Sửu,Mùi | Hãm: Tỵ,Hợi,Dậu
    ("Thiên Lương","Tý"):"Vượng", ("Thiên Lương","Sửu"):"Đắc",  ("Thiên Lương","Dần"):"Vượng",
    ("Thiên Lương","Mão"):"Vượng", ("Thiên Lương","Thìn"):"Miếu", ("Thiên Lương","Tỵ"):"Hãm",
    ("Thiên Lương","Ngọ"):"Miếu", ("Thiên Lương","Mùi"):"Đắc",  ("Thiên Lương","Thân"):"Vượng",
    ("Thiên Lương","Dậu"):"Hãm",  ("Thiên Lương","Tuất"):"Miếu", ("Thiên Lương","Hợi"):"Hãm",

    # THẤT SÁT — Miếu: Dần,Thân,Tý,Ngọ | Vượng: Tỵ,Hợi | Đắc: Sửu,Mùi | Hãm: Mão,Dậu,Thìn,Tuất
    ("Thất Sát","Tý"):"Miếu",  ("Thất Sát","Sửu"):"Đắc",  ("Thất Sát","Dần"):"Miếu",
    ("Thất Sát","Mão"):"Hãm",  ("Thất Sát","Thìn"):"Hãm",  ("Thất Sát","Tỵ"):"Vượng",
    ("Thất Sát","Ngọ"):"Miếu", ("Thất Sát","Mùi"):"Đắc",  ("Thất Sát","Thân"):"Miếu",
    ("Thất Sát","Dậu"):"Hãm",  ("Thất Sát","Tuất"):"Hãm",  ("Thất Sát","Hợi"):"Vượng",

    # PHÁ QUÂN — Miếu: Tý,Ngọ | Vượng: Sửu,Mùi | Đắc: Thìn,Tuất | Hãm: Dần,Thân,Tỵ,Hợi,Mão,Dậu
    ("Phá Quân","Tý"):"Miếu",  ("Phá Quân","Sửu"):"Vượng", ("Phá Quân","Dần"):"Hãm",
    ("Phá Quân","Mão"):"Hãm",  ("Phá Quân","Thìn"):"Đắc",  ("Phá Quân","Tỵ"):"Hãm",
    ("Phá Quân","Ngọ"):"Miếu", ("Phá Quân","Mùi"):"Vượng", ("Phá Quân","Thân"):"Hãm",
    ("Phá Quân","Dậu"):"Hãm",  ("Phá Quân","Tuất"):"Đắc",  ("Phá Quân","Hợi"):"Hãm",
    # KÌNH DƯƠNG — Đắc: Thìn,Tuất,Sửu,Mùi | Hãm: các cung còn lại
    ("Kình Dương","Tý"):"Hãm", ("Kình Dương","Sửu"):"Đắc", ("Kình Dương","Dần"):"Hãm",
    ("Kình Dương","Mão"):"Hãm", ("Kình Dương","Thìn"):"Đắc", ("Kình Dương","Tỵ"):"Hãm",
    ("Kình Dương","Ngọ"):"Hãm", ("Kình Dương","Mùi"):"Đắc", ("Kình Dương","Thân"):"Hãm",
    ("Kình Dương","Dậu"):"Hãm", ("Kình Dương","Tuất"):"Đắc", ("Kình Dương","Hợi"):"Hãm",
    # ĐÀ LA — Đắc: Thìn,Tuất,Sửu,Mùi | Hãm: các cung còn lại
    ("Đà La","Tý"):"Hãm", ("Đà La","Sửu"):"Đắc", ("Đà La","Dần"):"Hãm",
    ("Đà La","Mão"):"Hãm", ("Đà La","Thìn"):"Đắc", ("Đà La","Tỵ"):"Hãm",
    ("Đà La","Ngọ"):"Hãm", ("Đà La","Mùi"):"Đắc", ("Đà La","Thân"):"Hãm",
    ("Đà La","Dậu"):"Hãm", ("Đà La","Tuất"):"Đắc", ("Đà La","Hợi"):"Hãm",
    # HỎA TINH — Miếu: Dần,Ngọ,Tuất | Đắc: Tỵ,Dậu,Sửu | Bình Hòa: Hợi,Mão,Mùi | Hãm: Thân,Tý,Thìn
    ("Hỏa Tinh","Tý"):"Hãm", ("Hỏa Tinh","Sửu"):"Đắc", ("Hỏa Tinh","Dần"):"Miếu",
    ("Hỏa Tinh","Mão"):"Bình Hòa", ("Hỏa Tinh","Thìn"):"Hãm", ("Hỏa Tinh","Tỵ"):"Đắc",
    ("Hỏa Tinh","Ngọ"):"Miếu", ("Hỏa Tinh","Mùi"):"Bình Hòa", ("Hỏa Tinh","Thân"):"Hãm",
    ("Hỏa Tinh","Dậu"):"Đắc", ("Hỏa Tinh","Tuất"):"Miếu", ("Hỏa Tinh","Hợi"):"Bình Hòa",
    # LINH TINH — Miếu: Dần,Tuất,Thìn,Tỵ,Mùi | Bình Hòa: Tý,Ngọ,Thân,Mão | Hãm: Dậu,Sửu,Hợi
    ("Linh Tinh","Tý"):"Bình Hòa", ("Linh Tinh","Sửu"):"Hãm", ("Linh Tinh","Dần"):"Miếu",
    ("Linh Tinh","Mão"):"Bình Hòa", ("Linh Tinh","Thìn"):"Miếu", ("Linh Tinh","Tỵ"):"Miếu",
    ("Linh Tinh","Ngọ"):"Bình Hòa", ("Linh Tinh","Mùi"):"Miếu", ("Linh Tinh","Thân"):"Bình Hòa",
    ("Linh Tinh","Dậu"):"Hãm", ("Linh Tinh","Tuất"):"Miếu", ("Linh Tinh","Hợi"):"Hãm",
}


# Vietnamese Hỏa Tinh / Linh Tinh starting-branch by year-branch group
# (0-based: Tý=0, Sửu=1, Dần=2, Mão=3, ..., Hợi=11)
# Source: Tử Vi Thực Hành (book) — table per năm chi
_VN_SAT_TINH = {
    # (year_branch) -> (hoa_tinh_start_idx, linh_tinh_start_idx)
    "Dần": (1, 3),  "Ngọ": (1, 3),  "Tuất": (1, 3),   # Hỏa:Sửu(1), Linh:Mão(3)
    "Thân": (2, 10), "Tý": (2, 10), "Thìn": (2, 10),  # Hỏa:Dần(2), Linh:Tuất(10)
    "Tỵ":  (3, 10), "Dậu": (3, 10), "Sửu":  (3, 10),  # Hỏa:Mão(3), Linh:Tuất(10)
    "Hợi": (9, 10), "Mão": (9, 10), "Mùi":  (9, 10),  # Hỏa:Dậu(9), Linh:Tuất(10)
}
_CHI_IDX = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
_DUONG_CAN = {"Giáp", "Bính", "Mậu", "Canh", "Nhâm"}


def compute_vn_sat_tinh(year_branch: str, iztro_hour: int, year_can: str = "", is_male: bool = True):
    """Return (hoa_tinh_branch, linh_tinh_branch) using Vietnamese tradition.

    Direction rules (Tử Vi Thực Hành):
      Dương Nam / Âm Nữ → Hỏa thuận (CW) + Linh nghịch (CCW)
      Âm Nam / Dương Nữ → Hỏa nghịch (CCW) + Linh thuận (CW)
    """
    hour_idx = iztro_hour if iztro_hour < 12 else 0
    hoa_start, linh_start = _VN_SAT_TINH.get(year_branch, (2, 10))
    is_duong_year = year_can in _DUONG_CAN
    # Dương Nam or Âm Nữ → Hỏa goes forward (thuận)
    hoa_thuan = (is_duong_year == is_male)
    if hoa_thuan:
        hoa_branch = _CHI_IDX[(hoa_start + hour_idx) % 12]
        linh_branch = _CHI_IDX[(linh_start - hour_idx + 12) % 12]
    else:
        hoa_branch = _CHI_IDX[(hoa_start - hour_idx + 12) % 12]
        linh_branch = _CHI_IDX[(linh_start + hour_idx) % 12]
    return hoa_branch, linh_branch


def get_nap_am(birth_year: int) -> str:
    """Return Nạp Âm name for a birth year using 60-year cycle lookup."""
    can = _CAN_LIST[(birth_year - 4) % 10]
    chi = _CHI_LIST[(birth_year - 4) % 12]
    return NAP_AM_TABLE.get((can, chi), "Unknown")


def get_iztro_hour(hour: int) -> int:
    """Convert 24h hour to iztro time_index 0-12.

    0 = early Tý (0-1), 1 = Sửu (2-3), ..., 11 = Hợi (22), 12 = late Tý (23)

    Boundaries follow traditional double-hour system:
      Tý  23:00-01:00, Sửu 01:00-03:00, Dần 03:00-05:00, Mão 05:00-07:00 …
    So hour 5 (5:30 AM) → Mão (index 3), NOT Dần (index 2).
    """
    if hour in (0, 1):
        return 0   # early Tý (23:00-01:00 → treated as 0 and 1 AM still Tý)
    if hour == 23:
        return 12  # late Tý
    return (hour + 1) // 2


def compute_birth_month_can_chi(year_can: str, lunar_month: int) -> str:
    """Compute birth month can_chi using Ngũ Hổ Độn (Vietnamese Tử Vi convention).

    Vietnamese Tử Vi uses the lunar calendar month for the month pillar,
    NOT solar terms as in Chinese Bazi. iztro-py returns solar-term months
    so we override with this correct calculation.
    """
    # Ngũ Hổ Độn: stem index for month 1 (Dần) based on year stem
    _m1_stem = {
        "Giáp": 2, "Kỷ": 2,   # Bính
        "Ất": 4,  "Canh": 4,   # Mậu
        "Bính": 6, "Tân": 6,   # Canh
        "Đinh": 8, "Nhâm": 8,  # Nhâm
        "Mậu": 0,  "Quý": 0,   # Giáp
    }
    m1 = _m1_stem.get(year_can, 0)
    can = _CAN_LIST[(m1 + lunar_month - 1) % 10]
    chi = _CHI_LIST[(2 + lunar_month - 1) % 12]  # month 1 = Dần (index 2)
    return f"{can} {chi}"


def solar_to_lunar_via_library(year: int, month: int, day: int) -> dict:
    """Convert solar date to lunar date using lunarcalendar library (returns integers)."""
    from lunarcalendar import Solar, Converter
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return {
        "year": lunar.year,
        "month": lunar.month,
        "day": lunar.day,
        "is_leap": lunar.isleap,
    }


# Map iztro palace index to our format (0-based to 1-based)
# iztro: 0=子女, 1=夫妻, ... 11=父母
# Our format: 1=Mệnh, 2=Phụ Mẫu, ... 12=Phu Thê
IZTRO_TO_CUNG = {
    0: "Tử Tức",     # Children
    1: "Phu Thê",     # Spouse
    2: "Huynh Đệ",    # Siblings
    3: "Mệnh",        # Life (this is 命宫 in iztro)
    4: "Phụ Mẫu",     # Parents
    5: "Phúc Đức",    # Fortune
    6: "Điền Trạch", # Property
    7: "Quan Lộc",    # Career
    8: "Thiên Di",    # Travel
    9: "Tài Bạch",    # Wealth
    10: "Tật Ách",    # Misc
    11: "Nô Bộc",     # Subordinates
}

# Reverse mapping
CUNG_TO_IZTRO = {v: k for k, v in IZTRO_TO_CUNG.items()}

# Vietnamese translations
VIETNAMESE_NAMES = {
    "子女": "Tử Tức",
    "夫妻": "Phu Thê",
    "兄弟": "Huynh Đệ",
    "命宫": "Mệnh",
    "父母": "Phụ Mẫu",
    "福德": "Phúc Đức",
    "田宅": "Điền Trạch",
    "官禄": "Quan Lộc",
    "迁移": "Thiên Di",
    "疾厄": "Tật Ách",
    "财帛": "Tài Bạch",
    "仆役": "Nô Bộc",
}

# Star translations
STAR_TRANSLATIONS = {
    "紫微": "Tử Vi",
    "天机": "Thiên Cơ",
    "太阳": "Thái Dương",
    "武曲": "Vũ Khúc",
    "天同": "Thiên Đồng",
    "廉贞": "Liêm Trinh",
    "天府": "Thiên Phủ",
    "太阴": "Thái Âm",
    "贪狼": "Tham Lang",
    "巨门": "Cự Môn",
    "天相": "Thiên Tướng",
    "天梁": "Thiên Lương",
    "七杀": "Thất Sát",
    "破军": "Phá Quân",
}

# Element translations
ELEMENT_TRANSLATIONS = {
    "金": "Kim",
    "木": "Mộc",
    "水": "Thủy",
    "火": "Hỏa",
    "土": "Thổ",
}

# Cục names
CUC_NAMES = {
    "水二局": {"value": 2, "name": "Thủy Nhị Cục"},
    "木三局": {"value": 3, "name": "Mộc Tam Cục"},
    "金四局": {"value": 4, "name": "Kim Tứ Cục"},
    "土五局": {"value": 5, "name": "Thổ Ngũ Cục"},
    "火六局": {"value": 6, "name": "Hỏa Lục Cục"},
}

# Star elements
STAR_ELEMENTS = {
    "Tử Vi": "Thổ", "Thiên Phủ": "Thổ", "Thái Dương": "Hỏa", "Thái Âm": "Thủy",
    "Tham Lang": "Thủy", "Cự Môn": "Thủy", "Thiên Tướng": "Thủy", "Thiên Lương": "Mộc",
    "Thất Sát": "Kim", "Phá Quân": "Thủy", "Liêm Trinh": "Hỏa", "Thiên Đồng": "Thủy",
    "Vũ Khúc": "Kim", "Thiên Cơ": "Mộc"
}

# Dia Chi (Earthly Branch) translations
CHI_TRANSLATIONS = {
    "子": "Tý", "丑": "Sửu", "寅": "Dần", "卯": "Mão",
    "辰": "Thìn", "巳": "Tỵ", "午": "Ngọ", "未": "Mùi",
    "申": "Thân", "酉": "Dậu", "戌": "Tuất", "亥": "Hợi"
}

# Can (Heavenly Stem) translations
CAN_TRANSLATIONS = {
    "甲": "Giáp", "乙": "Ất", "丙": "Bính", "丁": "Đinh",
    "戊": "Mậu", "己": "Kỷ", "庚": "Canh", "辛": "Tân",
    "壬": "Nhâm", "癸": "Quý"
}

# Brightness translations
BRIGHTNESS_TRANSLATIONS = {
    "庙": "Miếu",
    "旺": "Vượng",
    "得": "Đắc",
    "利": "Lợi",
    "平": "Bình Hòa",
    "不": "Không",
    "陷": "Hãm"
}

# Tứ Hóa (mutagen) translations
TU_HOA_TRANSLATIONS = {
    "禄": "Hóa Lộc",
    "权": "Hóa Quyền",
    "科": "Hóa Khoa",
    "忌": "Hóa Kỵ"
}

# Extended star translations (including minor stars)
ALL_STAR_TRANSLATIONS = {
    # Main stars
    "紫微": "Tử Vi", "天机": "Thiên Cơ", "太阳": "Thái Dương",
    "武曲": "Vũ Khúc", "天同": "Thiên Đồng", "廉贞": "Liêm Trinh",
    "天府": "Thiên Phủ", "太阴": "Thái Âm", "贪狼": "Tham Lang",
    "巨门": "Cự Môn", "天相": "Thiên Tướng", "天梁": "Thiên Lương",
    "七杀": "Thất Sát", "破军": "Phá Quân",
    # Auxiliary stars
    "左辅": "Tả Phụ", "右弼": "Hữu Bật",
    "文昌": "Văn Xương", "文曲": "Văn Khúc",
    "天魁": "Thiên Khôi", "天钺": "Thiên Việt",
    "禄存": "Lộc Tồn", "擎羊": "Kình Dương", "陀罗": "Đà La",
    "火星": "Hỏa Tinh", "铃星": "Linh Tinh",
    "地空": "Địa Không", "地劫": "Địa Kiếp",
    "天马": "Thiên Mã",
    # Vòng Tràng Sinh (changsheng12)
    "长生": "Tràng Sinh", "沐浴": "Mộc Dục", "冠带": "Quan Đới",
    "临官": "Lâm Quan", "帝旺": "Đế Vượng", "衰": "Suy",
    "病": "Bệnh", "死": "Tử", "墓": "Mộ", "绝": "Tuyệt", "胎": "Thai", "养": "Dưỡng",
    # Vòng Bác Sĩ (boshi12)
    "博士": "Bác Sĩ", "力士": "Lực Sĩ", "青龙": "Thanh Long",
    "小耗": "Tiểu Hao", "将军": "Tướng Quân", "奏书": "Tấu Thư",
    "飞廉": "Phi Liêm", "喜神": "Hỷ Thần", "病符": "Bệnh Phù",
    "大耗": "Đại Hao", "伏兵": "Phục Binh", "官府": "Quan Phủ",
    # Vòng Tướng Tinh (jiangqian12)
    "将星": "Tướng Tinh", "攀鞍": "Ban An", "岁驿": "Tuế Dịch",
    "息神": "Tức Thần", "华盖": "Hoa Cái", "劫煞": "Kiếp Sát",
    "灾煞": "Tai Sát", "天煞": "Thiên Sát", "指背": "Chỉ Bối",
    "咸池": "Hàm Trì", "月煞": "Nguyệt Sát", "亡神": "Vong Thần",
    # Vòng Thái Tuế (suiqian12)
    "岁建": "Tuế Kiến", "晦气": "Hối Khí", "丧门": "Tang Môn",
    "贯索": "Quán Sách", "官符": "Quan Phù", "龙德": "Long Đức",
    "白虎": "Bạch Hổ", "天德": "Thiên Đức", "吊客": "Điếu Khách",
}

# Vietnamese Thái Tuế ring names — iztro-py uses Chinese suiqian12 names; map to Vietnamese
VN_THAI_TUE_MAP = {
    "Tuế Kiến": "Thái Tuế",
    "Hối Khí":  "Thiếu Dương",
    # Tang Môn stays the same: "Tang Môn"
    "Quán Sách": "Thiếu Âm",
    "Quan Phù":  "Quan Phủ",
    # iztro-py omits Tử Phù/Tuế Phá positions; suiqian12 skips them (only 9 entries mapped)
    "Long Đức":  "Long Đức",
    "Bạch Hổ":  "Bạch Hổ",
    "Thiên Đức": "Phúc Đức",
    "Điếu Khách": "Điếu Khách",
    # boshi12 also has Bệnh Phù — only remap when coming from suiqian12
    "Bệnh Phù":  "Trực Phù",
    # suiqian12 positions 6-7: iztro-py emits Tiểu Hao/Đại Hao but VN tradition uses Tử Phù/Tuế Phá
    "Tiểu Hao":  "Tử Phù",
    "Đại Hao":   "Tuế Phá",
}


# Hour translations (after branch)
HOUR_TRANSLATIONS = {
    "时": "",
    "子时": "Tý", "丑时": "Sửu", "寅时": "Dần", "卯时": "Mão",
    "辰时": "Thìn", "巳时": "Tỵ", "午时": "Ngọ", "未时": "Mùi",
    "申时": "Thân", "酉时": "Dậu", "戌时": "Tuất", "亥时": "Hợi"
}

# Can-Chi combinations
CAN_CHI_COMBINATIONS = {
    "庚午": "Canh Ngọ", "辛未": "Tân Mùi", "壬申": "Nhâm Thân", "癸酉": "Quý Dậu",
    "甲戌": "Giáp Tuất", "乙亥": "Ất Hợi", "丙子": "Bính Tý", "丁丑": "Đinh Sửu",
    "戊寅": "Mậu Dần", "己卯": "Kỷ Mão", "庚辰": "Canh Thìn", "辛巳": "Tân Tỵ",
    "壬午": "Nhâm Ngọ", "癸未": "Quý Mùi", "甲申": "Giáp Thân", "乙酉": "Ất Dậu",
    "丙戌": "Bính Tuất", "丁亥": "Đinh Hợi", "戊子": "Mậu Tý", "己丑": "Kỷ Sửu",
    "庚寅": "Canh Dần", "辛卯": "Tân Mão", "壬辰": "Nhâm Thìn", "癸巳": "Quý Tỵ",
    "甲午": "Giáp Ngọ", "乙未": "Ất Mùi", "丙申": "Bính Thân", "丁酉": "Đinh Dậu",
    "戊戌": "Mậu Tuất", "己亥": "Kỷ Hợi", "庚子": "Canh Tý", "辛丑": "Tân Sửu",
    "壬寅": "Nhâm Dần", "癸卯": "Quý Mão", "甲辰": "Giáp Thìn", "乙巳": "Ất Tỵ",
    "丙午": "Bính Ngọ", "丁未": "Đinh Mùi", "戊申": "Mậu Thân", "己酉": "Kỷ Dậu",
    "庚戌": "Canh Tuất", "辛亥": "Tân Hợi", "壬子": "Nhâm Tý", "癸丑": "Quý Sửu",
    "甲寅": "Giáp Dần", "乙卯": "Ất Mão", "丙辰": "Bính Thìn", "丁巳": "Đinh Tỵ",
    "戊午": "Mậu Ngọ", "己未": "Kỷ Mùi", "庚申": "Canh Thân", "辛酉": "Tân Dậu",
    "壬戌": "Nhâm Tuất", "癸亥": "Quý Hợi", "甲子": "Giáp Tý", "乙丑": "Ất Sửu"
}


def translate_chinese(text: str) -> str:
    """Apply all translation maps to convert Chinese to Vietnamese."""
    if not text:
        return text

    result = text

    # First check Can-Chi combinations (before individual chars)
    for cn, vn in CAN_CHI_COMBINATIONS.items():
        if cn in result:
            result = result.replace(cn, vn)

    # Then check hour translations
    for cn, vn in HOUR_TRANSLATIONS.items():
        if cn in result:
            result = result.replace(cn, vn)

    # Then check each translation map — sort by key length desc so multi-char entries match first
    for mapping in [ALL_STAR_TRANSLATIONS, CHI_TRANSLATIONS, CAN_TRANSLATIONS, ELEMENT_TRANSLATIONS, BRIGHTNESS_TRANSLATIONS]:
        for cn, vn in sorted(mapping.items(), key=lambda x: -len(x[0])):
            if cn in result:
                result = result.replace(cn, vn)

    return result


_MENH_CHU = {
    "Tý": "Tham Lang",
    "Sửu": "Cự Môn",   "Hợi": "Cự Môn",
    "Dần": "Lộc Tồn",  "Tuất": "Lộc Tồn",
    "Mão": "Văn Khúc", "Dậu": "Văn Khúc",
    "Thìn": "Liêm Trinh", "Thân": "Liêm Trinh",
    "Tỵ": "Vũ Khúc",   "Mùi": "Vũ Khúc",
    "Ngọ": "Phá Quân",
}
_THAN_CHU = {
    "Tý": "Hỏa Tinh",
    "Ngọ": "Linh Tinh",
    "Sửu": "Thiên Tướng", "Mùi": "Thiên Tướng",
    "Dần": "Thiên Lương",  "Thân": "Thiên Lương",
    "Mão": "Thiên Đồng",  "Dậu": "Thiên Đồng",
    "Thìn": "Văn Xương",  "Tuất": "Văn Xương",
    "Tỵ": "Thiên Cơ",    "Hợi": "Thiên Cơ",
}


def _compute_can_luong(iztro_hour: int, lunar_day: int, lunar_month: int, year_can: str, year_chi: str) -> dict:
    """Tính cân lượng chỉ từ giờ/ngày/tháng/năm âm lịch. Trả về dict {luong, chi, display}."""
    # Giá trị tính theo số chỉ (1 lượng = 10 chỉ)
    _GIO = {"Tý":16,"Sửu":6,"Dần":7,"Mão":10,"Thìn":9,"Tỵ":16,
            "Ngọ":10,"Mùi":8,"Thân":8,"Dậu":9,"Tuất":6,"Hợi":6}
    _NGAY = {1:5,2:10,3:8,4:15,5:16,6:15,7:8,8:16,9:8,10:16,
             11:9,12:17,13:8,14:17,15:10,16:8,17:9,18:18,19:5,
             20:15,21:10,22:9,23:8,24:9,25:15,26:18,27:7,28:8,29:16,30:6}
    _THANG = {1:6,2:7,3:18,4:9,5:5,6:16,7:9,8:15,9:18,10:18,11:9,12:5}
    _NAM = {
        "Giáp Tý":12,"Bính Tý":16,"Mậu Tý":15,"Canh Tý":7,"Nhâm Tý":5,
        "Ất Sửu":9,"Đinh Sửu":8,"Kỷ Sửu":8,"Tân Sửu":7,"Quý Sửu":5,
        "Bính Dần":6,"Mậu Dần":8,"Canh Dần":9,"Nhâm Dần":9,"Giáp Dần":12,
        "Đinh Mão":7,"Kỷ Mão":19,"Tân Mão":12,"Quý Mão":12,"Ất Mão":8,
        "Mậu Thìn":12,"Canh Thìn":12,"Nhâm Thìn":10,"Giáp Thìn":8,"Bính Thìn":8,
        "Kỷ Tỵ":5,"Tân Tỵ":6,"Quý Tỵ":7,"Ất Tỵ":7,"Đinh Tỵ":6,
        "Canh Ngọ":9,"Nhâm Ngọ":8,"Giáp Ngọ":15,"Bính Ngọ":13,"Mậu Ngọ":19,
        "Tân Mùi":8,"Quý Mùi":7,"Ất Mùi":6,"Đinh Mùi":5,"Kỷ Mùi":6,
        "Nhâm Thân":7,"Giáp Thân":5,"Bính Thân":5,"Mậu Thân":14,"Canh Thân":8,
        "Quý Dậu":8,"Ất Dậu":15,"Đinh Dậu":14,"Kỷ Dậu":5,"Tân Dậu":16,
        "Giáp Tuất":5,"Bính Tuất":6,"Mậu Tuất":14,"Canh Tuất":9,"Nhâm Tuất":10,
        "Ất Hợi":9,"Đinh Hợi":16,"Kỷ Hợi":9,"Tân Hợi":17,"Quý Hợi":7,
    }
    _CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
    gio_chi = _CHI[iztro_hour % 12]
    gio_val  = _GIO.get(gio_chi, 0)
    ngay_val = _NGAY.get(lunar_day, 0)
    thang_val= _THANG.get(lunar_month, 0)
    nam_key  = f"{year_can} {year_chi}"
    nam_val  = _NAM.get(nam_key, 0)
    total    = gio_val + ngay_val + thang_val + nam_val
    luong, chi = divmod(total, 10)
    return {"luong": luong, "chi": chi, "display": f"{luong} lượng {chi} chỉ"}


def _compute_luu_stars(palaces: list, nam_xem: int) -> None:
    """Thêm luu_stars vào mỗi cung dựa theo năm xem (năm luận giải)."""
    _CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
    _CAN = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]

    chi_idx = (nam_xem - 4) % 12
    can_idx = (nam_xem - 4) % 10
    nam_xem_chi = _CHI[chi_idx]
    nam_xem_can = _CAN[can_idx]

    chi_to_palace = {p["dia_chi"]: p for p in palaces}
    for p in palaces:
        p["luu_stars"] = []

    def _add(chi, name):
        if chi in chi_to_palace:
            chi_to_palace[chi]["luu_stars"].append(name)

    # L. Thái Tuế: địa chi năm xem
    _add(nam_xem_chi, "L. Thái Tuế")

    # L. Bạch Hổ: Thân = Tý, thuận đến năm xem
    _add(_CHI[(8 + chi_idx) % 12], "L. Bạch Hổ")

    # L. Tang Môn: Dần = Tý, thuận đến năm xem
    _add(_CHI[(2 + chi_idx) % 12], "L. Tang Môn")

    # L. Thiên Hư: Ngọ = Tý, thuận đến năm xem
    _add(_CHI[(6 + chi_idx) % 12], "L. Thiên Hư")

    # L. Thiên Khốc: Ngọ = Tý, nghịch đến năm xem
    _add(_CHI[(6 - chi_idx + 12) % 12], "L. Thiên Khốc")

    # L. Thiên Mã: theo nhóm địa chi năm xem
    _LUU_MA = {
        "Dần":"Thân","Ngọ":"Thân","Tuất":"Thân",
        "Thân":"Dần","Tý":"Dần","Thìn":"Dần",
        "Tỵ":"Hợi","Dậu":"Hợi","Sửu":"Hợi",
        "Hợi":"Tỵ","Mão":"Tỵ","Mùi":"Tỵ",
    }
    if nam_xem_chi in _LUU_MA:
        _add(_LUU_MA[nam_xem_chi], "L. Thiên Mã")

    # L. Lộc Tồn, L. Kình Dương, L. Đà La: theo thiên can năm xem
    _LOC_TON = {
        "Giáp":"Dần","Ất":"Mão","Bính":"Tỵ","Đinh":"Ngọ",
        "Mậu":"Tỵ","Kỷ":"Ngọ","Canh":"Thân","Tân":"Dậu",
        "Nhâm":"Hợi","Quý":"Tý",
    }
    loc_ton_chi = _LOC_TON.get(nam_xem_can)
    if loc_ton_chi:
        _add(loc_ton_chi, "L. Lộc Tồn")
        li = _CHI.index(loc_ton_chi)
        _add(_CHI[(li + 1) % 12], "L. Kình Dương")
        _add(_CHI[(li - 1 + 12) % 12], "L. Đà La")

    # L. Tứ Hóa: bảng giống Tứ Hóa năm sinh nhưng dùng can năm xem
    _TU_HOA_TABLE = {
        "Giáp": {"Lộc":"Liêm Trinh","Quyền":"Phá Quân","Khoa":"Vũ Khúc","Kỵ":"Thái Dương"},
        "Ất":   {"Lộc":"Thiên Cơ","Quyền":"Thiên Lương","Khoa":"Tử Vi","Kỵ":"Thái Âm"},
        "Bính": {"Lộc":"Thiên Đồng","Quyền":"Thiên Cơ","Khoa":"Văn Xương","Kỵ":"Liêm Trinh"},
        "Đinh": {"Lộc":"Thái Âm","Quyền":"Thiên Đồng","Khoa":"Thiên Cơ","Kỵ":"Cự Môn"},
        "Mậu":  {"Lộc":"Tham Lang","Quyền":"Thái Âm","Khoa":"Hữu Bật","Kỵ":"Thiên Cơ"},
        "Kỷ":   {"Lộc":"Vũ Khúc","Quyền":"Tham Lang","Khoa":"Thiên Lương","Kỵ":"Văn Khúc"},
        "Canh": {"Lộc":"Thái Dương","Quyền":"Vũ Khúc","Khoa":"Thái Âm","Kỵ":"Thiên Đồng"},
        "Tân":  {"Lộc":"Cự Môn","Quyền":"Thái Dương","Khoa":"Văn Khúc","Kỵ":"Văn Xương"},
        "Nhâm": {"Lộc":"Thiên Lương","Quyền":"Tử Vi","Khoa":"Tả Phụ","Kỵ":"Vũ Khúc"},
        "Quý":  {"Lộc":"Phá Quân","Quyền":"Cự Môn","Khoa":"Thái Âm","Kỵ":"Tham Lang"},
    }
    # Build star name → dia_chi from all palace stars
    star_to_chi = {}
    for p in palaces:
        for s in p.get("stars", []):
            if s["name"] not in star_to_chi:
                star_to_chi[s["name"]] = p["dia_chi"]

    if nam_xem_can in _TU_HOA_TABLE:
        for hoa_type, star_name in _TU_HOA_TABLE[nam_xem_can].items():
            chi = star_to_chi.get(star_name)
            if chi:
                _add(chi, f"L. Hóa {hoa_type}")


def get_tuvi_chart(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int = 0,
    gender: str = "nam",
    is_leap_month: bool = False,
    nam_xem: int = None,
) -> Dict:
    """
    Get complete Tử Vi chart using iztro-py.

    Args:
        year: Solar year
        month: Solar month
        day: Solar day
        hour: Hour (0-23)
        minute: Minute (0-59)
        gender: "nam" or "nữ"
        is_leap_month: Whether it's a leap month

    Returns:
        Complete chart dict
    """
    # Convert hour 0-23 to iztro time_index 0-12
    iztro_hour = get_iztro_hour(hour)

    # Convert to py-iztro format
    date_str = f"{year}-{month}-{day}"

    # Map gender
    iztro_gender = "男" if gender.lower() in ("nam", "male", "m") else "女"

    # Get chart from iztro-py (pure Python, no singleton needed)
    result = by_solar(date_str, iztro_hour, iztro_gender)

    # Use lunarcalendar library for accurate lunar date (avoids Chinese text parsing bugs)
    lunar_data = solar_to_lunar_via_library(year, month, day)

    birth = {
        "solar": {"year": year, "month": month, "day": day, "hour": hour, "minute": minute},
        "lunar": {
            "year": lunar_data["year"],
            "month": lunar_data["month"],
            "day": lunar_data["day"],
            "is_leap": lunar_data["is_leap"],
        },
        "can_chi": {
            "year": translate_chinese(result.chinese_date.split()[0]) if result.chinese_date else "",
            "month": compute_birth_month_can_chi(
                translate_chinese(result.chinese_date.split()[0]).split()[0] if result.chinese_date else "",
                lunar_data["month"]
            ),
            "day": translate_chinese(result.chinese_date.split()[2]) if len(result.chinese_date.split()) > 2 else "",
            "hour": translate_chinese(result.time)
        }
    }

    # Get Cục
    cuc_info = CUC_NAMES.get(result.five_elements_class, {"value": 4, "name": "Kim Tứ Cục"})

    # Get Cung Mệnh - the earthly branch of the soul palace (命宫)
    # Use EARTHLY_BRANCH_MAP for iztro-py enum values
    cung_menh_dia_chi = translate_chinese(EARTHLY_BRANCH_MAP.get(result.earthly_branch_of_soul_palace, result.earthly_branch_of_soul_palace)) if result.earthly_branch_of_soul_palace else ""
    cung_than_dia_chi = translate_chinese(EARTHLY_BRANCH_MAP.get(result.earthly_branch_of_body_palace, result.earthly_branch_of_body_palace)) if result.earthly_branch_of_body_palace else ""

    # Calculate current age for Đại Hạn/Tiểu Hạn
    current_year = datetime.now().year
    current_age = current_year - year

    # Pre-calculate Vietnamese Hỏa Tinh / Linh Tinh positions (override iztro-py Chinese formula)
    _year_can_chi = birth["can_chi"]["year"]
    _year_can_vn = _year_can_chi.split()[0] if " " in _year_can_chi else ""
    _year_branch_vn = _year_can_chi.split()[1] if " " in _year_can_chi else ""
    _is_male = gender.lower() in ("nam", "male", "m")
    vn_hoa_tinh_branch, vn_linh_tinh_branch = compute_vn_sat_tinh(_year_branch_vn, iztro_hour, _year_can_vn, _is_male)

    # Pre-calculate positions of stars not provided by iztro-py
    _lunar_month = lunar_data["month"]
    _lunar_day = lunar_data["day"]
    _extra_by_branch = {}  # dia_chi -> list of star names
    def _add_extra(branch, name):
        if branch:
            _extra_by_branch.setdefault(branch, []).append(name)

    # By Thiên Can
    _add_extra(_LUU_HA_BY_CAN.get(_year_can_vn), "Lưu Hà")
    _add_extra(_QUOC_AN_BY_CAN.get(_year_can_vn), "Quốc Ấn")
    _add_extra(_DUONG_PHU_BY_CAN.get(_year_can_vn), "Đường Phù")
    _add_extra(_VAN_TINH_BY_CAN.get(_year_can_vn), "Văn Tinh")
    _add_extra(_THIEN_TRU_BY_CAN.get(_year_can_vn), "Thiên Trù")
    _add_extra(_THIEN_PHUC_BY_CAN.get(_year_can_vn), "Thiên Phúc")
    _add_extra(_THIEN_QUAN_BY_CAN.get(_year_can_vn), "Thiên Quan")
    # By Địa Chi
    _add_extra(_DAO_HOA_BY_CHI.get(_year_branch_vn), "Đào Hoa")
    _add_extra(_KIEP_SAT_BY_CHI.get(_year_branch_vn), "Kiếp Sát")
    # Giải Thần = đồng cung với Phượng Các (§5.23)
    # Phượng Các: cung Tuất = Chi Tý, nghịch → (10 - year_branch_idx + 12) % 12
    _year_branch_idx = _CHI_LIST.index(_year_branch_vn) if _year_branch_vn in _CHI_LIST else 0
    _giai_than_chi = _CHI_LIST[(10 - _year_branch_idx + 12) % 12]
    _add_extra(_giai_than_chi, "Giải Thần")
    # Đẩu Quân: từ cung Chi năm = tháng 1, đi nghịch đến tháng sinh,
    #           rồi từ đó = Giờ Tý, đi thuận đến giờ sinh
    _dau_quan_step = (_year_branch_idx - (_lunar_month - 1)) % 12
    _dau_quan_chi = _CHI_LIST[(_dau_quan_step + iztro_hour % 12) % 12]
    _add_extra(_dau_quan_chi, "Đẩu Quân")
    # By tháng
    _add_extra(_THIEN_Y_BY_MONTH.get(_lunar_month), "Thiên Y")
    _add_extra(_THIEN_GIAI_BY_MONTH.get(_lunar_month), "Thiên Giải")
    _add_extra(_DIA_GIAI_BY_MONTH.get(_lunar_month), "Địa Giải")

    # Build palaces with stars
    palaces = []
    stars_dict = {}

    for idx, palace in enumerate(result.palaces):
        # Use English translations for iztro-py (which returns English enum names)
        palace_name_vn = ENGLISH_PALACE_TRANSLATIONS.get(palace.name, palace.name)

        # Get stars in this palace
        palace_stars = []

        # Compute dia chi for this palace (used by VN_BRIGHTNESS_TABLE override)
        palace_dia_chi_for_override = translate_chinese(EARTHLY_BRANCH_MAP.get(palace.earthly_branch, palace.earthly_branch))

        # Major stars
        for star in palace.major_stars:
            # Use English translations for iztro-py
            star_name = ENGLISH_STAR_TRANSLATIONS.get(star.name, star.name)
            _raw_brightness = translate_chinese(star.brightness) if star.brightness else "Bình Hòa"
            brightness = VN_BRIGHTNESS_TABLE.get((star_name, palace_dia_chi_for_override), _raw_brightness)
            star_meaning = get_star_interpretation(star_name, brightness)
            tu_hoa = TU_HOA_TRANSLATIONS.get(star.mutagen, None) if star.mutagen else None

            if star_name not in stars_dict:
                stars_dict[star_name] = {
                    "name": star_name,
                    "element": STAR_ELEMENTS.get(star_name, "Thổ"),
                    "position": idx + 1,
                    "meaning": star_meaning.get("meaning", ""),
                    "brightness": brightness,
                    "brightness_effect": star_meaning.get("brightness_effect", ""),
                    "tu_hoa": tu_hoa
                }
            palace_stars.append({
                "name": star_name,
                "element": STAR_ELEMENTS.get(star_name, "Thổ"),
                "brightness": brightness,
                "meaning": star_meaning.get("meaning", ""),
                "brightness_effect": star_meaning.get("brightness_effect", ""),
                "tu_hoa": tu_hoa
            })

        # Minor stars (add some key ones)
        for star in palace.minor_stars:
            # Skip Hỏa Tinh & Linh Tinh — placed by Vietnamese formula below
            # Skip lucunMin (Lưu Hư) — not a standard Vietnamese Tử Vi star
            if star.name in ('huoxingMin', 'lingxingMin'):
                continue
            # Use English translations for iztro-py
            star_name = ENGLISH_STAR_TRANSLATIONS.get(star.name, star.name)
            _raw_brightness = translate_chinese(star.brightness) if star.brightness else "Bình Hòa"
            brightness = VN_BRIGHTNESS_TABLE.get((star_name, palace_dia_chi_for_override), _raw_brightness)
            star_meaning = get_star_interpretation(star_name, brightness)
            tu_hoa = TU_HOA_TRANSLATIONS.get(star.mutagen, None) if star.mutagen else None

            if star_name not in stars_dict:
                stars_dict[star_name] = {
                    "name": star_name,
                    "element": STAR_ELEMENTS.get(star_name, "Thổ"),
                    "position": idx + 1,
                    "meaning": star_meaning.get("meaning", ""),
                    "brightness": brightness,
                    "brightness_effect": star_meaning.get("brightness_effect", ""),
                    "tu_hoa": tu_hoa
                }
            palace_stars.append({
                "name": star_name,
                "element": STAR_ELEMENTS.get(star_name, "Thổ"),
                "brightness": brightness,
                "meaning": star_meaning.get("meaning", ""),
                "brightness_effect": star_meaning.get("brightness_effect", ""),
                "tu_hoa": tu_hoa
            })

        # Use earthly-branch-based mapping for correct Thiên Bàn cell placement
        our_position = EARTHLY_BRANCH_POSITION.get(palace.earthly_branch, idx + 1)
        # Look up palace meaning by Vietnamese name — position-independent (fixes Mệnh at Tỵ bug)
        palace_meaning = get_palace_meaning_by_name(palace_name_vn)

        # Extract Đại Hạn (decadal) data
        dai_han = None
        if palace.decadal:
            d = palace.decadal
            # Use enum mappings for decadal stems/branches
            stem = HEAVENLY_STEM_MAP.get(d.heavenly_stem, d.heavenly_stem)
            branch = EARTHLY_BRANCH_MAP.get(d.earthly_branch, d.earthly_branch)
            can_chi = translate_chinese(stem + branch) if stem and branch else ""
            is_current = d.range[0] <= current_age <= d.range[1]
            dai_han = {
                "range": list(d.range),
                "can_chi": can_chi,
                "is_current": is_current
            }

        # Extract Tiểu Hạn ages
        tieu_han_ages = list(palace.ages) if palace.ages else []
        is_current_tieu_han = current_age in tieu_han_ages

        # Extract adjective (Grade B) stars — filtered to PDF whitelist
        adj_stars = []
        for star in palace.adjective_stars:
            star_name = ENGLISH_STAR_TRANSLATIONS.get(star.name, star.name)
            if star_name not in ALLOWED_ADJ_STARS:
                continue
            brightness = translate_chinese(star.brightness) if star.brightness else None
            tu_hoa = TU_HOA_TRANSLATIONS.get(star.mutagen, None) if star.mutagen else None
            adj_stars.append({"name": star_name, "brightness": brightness, "tu_hoa": tu_hoa})

        # Include ring-cycle stars in adjective_stars (Bác Sĩ, Tướng Tinh, Thái Tuế rings)
        _adj_names_seen = {s["name"] for s in adj_stars}
        for ring_src, ring_val in [('boshi12', palace.boshi12), ('suiqian12', palace.suiqian12)]:
            if ring_val:
                ring_name = translate_chinese(ring_val)
                if ring_src == 'suiqian12':
                    ring_name = VN_THAI_TUE_MAP.get(ring_name, ring_name)
                if ring_name and ring_name not in _adj_names_seen:
                    _adj_names_seen.add(ring_name)
                    adj_stars.append({"name": ring_name, "brightness": None, "tu_hoa": None})

        # Palace Can Chi: heavenly_stem (enum) → Chinese → Vietnamese, combined with dia_chi
        palace_stem_cn = HEAVENLY_STEM_MAP.get(palace.heavenly_stem, "")
        palace_stem_vn = translate_chinese(palace_stem_cn)
        palace_dia_chi = translate_chinese(EARTHLY_BRANCH_MAP.get(palace.earthly_branch, palace.earthly_branch))
        palace_can_chi = f"{palace_stem_vn} {palace_dia_chi}" if palace_stem_vn else palace_dia_chi

        palaces.append({
            "position": our_position,
            "dia_chi": palace_dia_chi,
            "can_chi": palace_can_chi,
            "cung_name": palace_name_vn,
            "meaning": palace_meaning.get("meaning", ""),
            "stars": palace_stars,
            "adjective_stars": adj_stars,
            "trang_sinh": translate_chinese(palace.changsheng12) if palace.changsheng12 else "",
            "bac_si": translate_chinese(palace.boshi12) if palace.boshi12 else "",
            "thai_tue": VN_THAI_TUE_MAP.get(translate_chinese(palace.suiqian12), translate_chinese(palace.suiqian12)) if palace.suiqian12 else "",
            "is_body_palace": bool(palace.is_body_palace),
            "dai_han": dai_han,
            "tieu_han_ages": tieu_han_ages,
            "is_current_tieu_han": is_current_tieu_han,
            "_orig_index": idx  # Keep for reordering
        })

    # Inject Vietnamese-calculated Hỏa Tinh / Linh Tinh into correct palaces
    for p in palaces:
        dc = p["dia_chi"]
        if dc == vn_hoa_tinh_branch:
            brightness = VN_BRIGHTNESS_TABLE.get(("Hỏa Tinh", dc), "Hãm")
            p["stars"].append({"name": "Hỏa Tinh", "element": "Hỏa", "brightness": brightness, "meaning": "", "brightness_effect": "", "tu_hoa": None})
        if dc == vn_linh_tinh_branch:
            brightness = VN_BRIGHTNESS_TABLE.get(("Linh Tinh", dc), "Hãm")
            p["stars"].append({"name": "Linh Tinh", "element": "Hỏa", "brightness": brightness, "meaning": "", "brightness_effect": "", "tu_hoa": None})

    # Inject missing stars (Lưu Hà, Quốc Ấn, Đường Phù, Văn Tinh, Đào Hoa, Kiếp Sát,
    # Thiên Y, Thiên Giải, Địa Giải, Thiên Trù, Thiên Phúc, Thiên Quan, Giải Thần)
    # computed from year can/chi and lunar month
    for p in palaces:
        dc = p["dia_chi"]
        seen = {s["name"] for s in p["adjective_stars"]}
        for star_name in _extra_by_branch.get(dc, []):
            if star_name not in seen:
                p["adjective_stars"].append({"name": star_name, "brightness": None, "tu_hoa": None})

    # Thiên Thương at Nô Bộc, Thiên Sứ at Tật Ách (§5.29)
    for p in palaces:
        cung = p["cung_name"]
        adj_names = {s["name"] for s in p["adjective_stars"]}
        if cung == "Nô Bộc" and "Thiên Thương" not in adj_names:
            p["adjective_stars"].append({"name": "Thiên Thương", "brightness": None, "tu_hoa": None})
        if cung == "Tật Ách" and "Thiên Sứ" not in adj_names:
            p["adjective_stars"].append({"name": "Thiên Sứ", "brightness": None, "tu_hoa": None})

    # Địa Võng fixed at Tuất; Thiên La fixed at Thìn (§5.10)
    for p in palaces:
        dc = p["dia_chi"]
        adj_set = {s["name"] for s in p["adjective_stars"]}
        if dc == "Tuất" and "Địa Võng" not in adj_set:
            p["adjective_stars"].append({"name": "Địa Võng", "brightness": None, "tu_hoa": None})
        if dc == "Thìn" and "Thiên La" not in adj_set:
            p["adjective_stars"].append({"name": "Thiên La", "brightness": None, "tu_hoa": None})

    # Thiên Tài = (Mệnh_chi_idx + year_branch_idx) % 12 (§5.26)
    # Thiên Thọ = (Thân_chi_idx + year_branch_idx) % 12 (§5.26)
    _menh_chi = None
    _than_chi = None
    for p in palaces:
        if p["cung_name"] == "Mệnh":
            _menh_chi = p["dia_chi"]
        if p.get("is_body_palace"):
            _than_chi = p["dia_chi"]
    if _menh_chi and _menh_chi in _CHI_LIST:
        _tai_idx = (_CHI_LIST.index(_menh_chi) + _year_branch_idx) % 12
        _tai_chi = _CHI_LIST[_tai_idx]
        for p in palaces:
            if p["dia_chi"] == _tai_chi and "Thiên Tài" not in {s["name"] for s in p["adjective_stars"]}:
                p["adjective_stars"].append({"name": "Thiên Tài", "brightness": None, "tu_hoa": None})
    if _than_chi and _than_chi in _CHI_LIST:
        _tho_idx = (_CHI_LIST.index(_than_chi) + _year_branch_idx) % 12
        _tho_chi = _CHI_LIST[_tho_idx]
        for p in palaces:
            if p["dia_chi"] == _tho_chi and "Thiên Thọ" not in {s["name"] for s in p["adjective_stars"]}:
                p["adjective_stars"].append({"name": "Thiên Thọ", "brightness": None, "tu_hoa": None})

    # Day-based stars: Ân Quang, Tam Thai, Bát Tọa, Thiên Quý (§5.21, §5.22)
    # Find reference star positions
    _van_xuong_chi = _ta_phu_chi = _huu_bat_chi = _van_khuc_chi = None
    for p in palaces:
        for s in p["stars"]:
            if s["name"] == "Văn Xương" and _van_xuong_chi is None:
                _van_xuong_chi = p["dia_chi"]
            elif s["name"] == "Tả Phụ" and _ta_phu_chi is None:
                _ta_phu_chi = p["dia_chi"]
            elif s["name"] == "Hữu Bật" and _huu_bat_chi is None:
                _huu_bat_chi = p["dia_chi"]
            elif s["name"] == "Văn Khúc" and _van_khuc_chi is None:
                _van_khuc_chi = p["dia_chi"]
    # Ân Quang = Văn Xương + (lunar_day - 2) thuận (lùi 1 từ ngày sinh)
    if _van_xuong_chi and _van_xuong_chi in _CHI_LIST:
        _aq_chi = _CHI_LIST[(_CHI_LIST.index(_van_xuong_chi) + _lunar_day - 2) % 12]
        for p in palaces:
            if p["dia_chi"] == _aq_chi and "Ân Quang" not in {s["name"] for s in p["adjective_stars"]}:
                p["adjective_stars"].append({"name": "Ân Quang", "brightness": None, "tu_hoa": None})
    # Tam Thai = Tả Phụ + (lunar_day - 1) thuận
    if _ta_phu_chi and _ta_phu_chi in _CHI_LIST:
        _tt_chi = _CHI_LIST[(_CHI_LIST.index(_ta_phu_chi) + _lunar_day - 1) % 12]
        for p in palaces:
            if p["dia_chi"] == _tt_chi and "Tam Thai" not in {s["name"] for s in p["adjective_stars"]}:
                p["adjective_stars"].append({"name": "Tam Thai", "brightness": None, "tu_hoa": None})
    # Bát Tọa = Hữu Bật - (lunar_day - 1) nghịch
    if _huu_bat_chi and _huu_bat_chi in _CHI_LIST:
        _bt_chi = _CHI_LIST[(_CHI_LIST.index(_huu_bat_chi) - (_lunar_day - 1)) % 12]
        for p in palaces:
            if p["dia_chi"] == _bt_chi and "Bát Tọa" not in {s["name"] for s in p["adjective_stars"]}:
                p["adjective_stars"].append({"name": "Bát Tọa", "brightness": None, "tu_hoa": None})
    # Thiên Quý = Văn Khúc - lunar_day (nghịch đến ngày sinh rồi lùi 1 cung) (§5.21)
    if _van_khuc_chi and _van_khuc_chi in _CHI_LIST:
        _tq_chi = _CHI_LIST[(_CHI_LIST.index(_van_khuc_chi) - _lunar_day) % 12]
        for p in palaces:
            if p["dia_chi"] == _tq_chi and "Thiên Quý" not in {s["name"] for s in p["adjective_stars"]}:
                p["adjective_stars"].append({"name": "Thiên Quý", "brightness": None, "tu_hoa": None})

    # Reorder palaces to standard order (1=Mệnh, 2=Phụ Mẫu, ..., 12=Phu Thê)
    palaces.sort(key=lambda p: p["position"])

    # Thiên Không = next palace after Thái Tuế (§5.28)
    for i, p in enumerate(palaces):
        if p.get("thai_tue") == "Thái Tuế":
            next_p = palaces[(i + 1) % 12]
            if "Thiên Không" not in {s["name"] for s in next_p["adjective_stars"]}:
                next_p["adjective_stars"].append({"name": "Thiên Không", "brightness": None, "tu_hoa": None})
            break

    # Build Tứ Hóa summary
    tu_hoa_summary = {}
    for p in palaces:
        for s in p.get("stars", []):
            if s.get("tu_hoa"):
                tu_hoa_key = s["tu_hoa"].replace("Hóa ", "hoa_").lower()
                tu_hoa_summary[tu_hoa_key] = {
                    "star": s["name"],
                    "palace": p["cung_name"]
                }

    nap_am_name = get_nap_am(lunar_data["year"])
    nap_am_element = nap_am_name.split()[-1] if nap_am_name != "Unknown" else ""

    # Build Đại Hạn from iztro-py palace decadal data (already correct)
    dai_han = []
    for p in palaces:
        if p.get("dai_han"):
            dh = p["dai_han"]
            dai_han.append({
                "start_age":   dh["range"][0],
                "end_age":     dh["range"][1],
                "palace_name": p["cung_name"],
                "dia_chi":     p["dia_chi"],
                "palace_index": p["position"],
                "can_chi":     dh["can_chi"],
                "is_current":  dh["is_current"],
                "period":      dh["can_chi"],
            })
    dai_han.sort(key=lambda x: x["start_age"])

    # Build Tiểu Hạn from palace ages
    tieu_han_current = None
    tieu_han_upcoming = None
    for p in palaces:
        ages = p.get("tieu_han_ages", [])
        if current_age in ages:
            tieu_han_current = {
                "palace_name":  p["cung_name"],
                "palace_index": p["position"],
                "stars": [s["name"] for s in p.get("stars", [])[:3]],
            }
        if ages and min(ages) > current_age:
            if tieu_han_upcoming is None or min(ages) < min(tieu_han_upcoming.get("ages", [9999])):
                tieu_han_upcoming = {
                    "palace_name":  p["cung_name"],
                    "palace_index": p["position"],
                    "ages": ages,
                }

    # Mệnh Chủ / Thân Chủ
    year_chi = birth["can_chi"]["year"].split()[1] if birth["can_chi"]["year"] else ""
    menh_chu = _MENH_CHU.get(cung_menh_dia_chi, "")
    than_chu = _THAN_CHU.get(year_chi, "")

    # Sao Lưu Năm
    _effective_nam_xem = nam_xem if nam_xem else current_year
    _compute_luu_stars(palaces, _effective_nam_xem)

    # Cân Lượng Chỉ
    can_luong = _compute_can_luong(iztro_hour, _lunar_day, _lunar_month, _year_can_vn, _year_branch_vn)

    return {
        "birth": birth,
        "gender": gender,
        "nap_am": {
            "name": nap_am_name,
            "ngu_hanh": nap_am_element,
        },
        "cuc": cuc_info,
        "cung_menh": cung_menh_dia_chi,
        "cung_than": cung_than_dia_chi,
        "menh_chu": menh_chu,
        "than_chu": than_chu,
        "can_luong": can_luong,
        "tu_hoa": tu_hoa_summary,
        "palaces": palaces,
        "stars": stars_dict,
        "dai_han": dai_han,
        "tieu_han": tieu_han_current or {},
        "tieu_han_upcoming": tieu_han_upcoming or {},
    }
