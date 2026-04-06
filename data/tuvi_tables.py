"""
Tu Vi Data Tables - Complete lookup tables for Tử Vi calculations.

Based on traditional Vietnamese astrology (Tử Vi Đại Quảng).
"""

# 12 Cung (Palaces)
CUNG = [
    "Mệnh", "Phụ Mẫu", "Huynh Đệ", "Tử Tức",
    "Phúc Đức", "Điền Trạch", "Quan Lộc", "Thiên Di",
    "Tài Bạch", "Tật Ách", "Nô Bộc", "Phu Thê"
]

# 12 Địa Chi (Earthly Branches)
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# 10 Thiên Can (Celestial Stems)
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

# 14 Chính Tinh (Main Stars) - CORRECT LIST
CHINH_TINH = [
    "Tử Vi", "Thiên Phủ", "Thái Dương", "Thái Âm",
    "Tham Lang", "Cự Môn", "Thiên Tướng", "Thiên Lương",
    "Thất Sát", "Phá Quân", "Liêm Trinh", "Thiên Đồng",
    "Vũ Khúc", "Thiên Cơ"
]

# Star Elements
STAR_ELEMENT = {
    "Tử Vi": "Thổ", "Thiên Phủ": "Thổ", "Thái Dương": "Hỏa", "Thái Âm": "Thủy",
    "Tham Lang": "Thủy", "Cự Môn": "Thủy", "Thiên Tướng": "Thủy", "Thiên Lương": "Mộc",
    "Thất Sát": "Kim", "Phá Quân": "Thủy", "Liêm Trinh": "Hỏa", "Thiên Đồng": "Thủy",
    "Vũ Khúc": "Kim", "Thiên Cơ": "Mộc"
}

# 60-year Nạp Âm table: (can_idx, chi_idx) -> (ngu_hanh, nap_am_name)
# Can index 0-9, Chi index 0-11 -> 60 entries
NAP_AM_TABLE = {
    # Giáp years (can_idx=0)
    (0, 0): ("Kim", "Giáp Tý"), (0, 1): ("Mộc", "Giáp Sửu"), (0, 2): ("Mộc", "Giáp Dần"), (0, 3): ("Mộc", "Giáp Mão"),
    (0, 4): ("Hỏa", "Giáp Thìn"), (0, 5): ("Hỏa", "Giáp Tỵ"), (0, 6): ("Hỏa", "Giáp Ngọ"), (0, 7): ("Hỏa", "Giáp Mùi"),
    (0, 8): ("Thổ", "Giáp Thân"), (0, 9): ("Thổ", "Giáp Dậu"), (0, 10): ("Thổ", "Giáp Tuất"), (0, 11): ("Thủy", "Giáp Hợi"),
    # Ất years (can_idx=1) - FIXED
    (1, 0): ("Kim", "Ất Tý"), (1, 1): ("Kim", "Ất Sửu"), (1, 2): ("Mộc", "Ất Dần"), (1, 3): ("Mộc", "Ất Mão"),
    (1, 4): ("Mộc", "Ất Thìn"), (1, 5): ("Hỏa", "Ất Tỵ"), (1, 6): ("Hỏa", "Ất Ngọ"), (1, 7): ("Hỏa", "Ất Mùi"),
    (1, 8): ("Hỏa", "Ất Thân"), (1, 9): ("Thổ", "Ất Dậu"), (1, 10): ("Thổ", "Ất Tuất"), (1, 11): ("Thổ", "Ất Hợi"),
    # Bính years (can_idx=2) - FIXED
    (2, 0): ("Thủy", "Bính Tý"), (2, 1): ("Thủy", "Bính Sửu"), (2, 2): ("Hỏa", "Bính Dần"), (2, 3): ("Hỏa", "Bính Mão"),
    (2, 4): ("Hỏa", "Bính Thìn"), (2, 5): ("Thổ", "Bính Tỵ"), (2, 6): ("Thổ", "Bính Ngọ"), (2, 7): ("Kim", "Bính Mùi"),
    (2, 8): ("Kim", "Bính Thân"), (2, 9): ("Kim", "Bính Dậu"), (2, 10): ("Mộc", "Bính Tuất"), (2, 11): ("Mộc", "Bính Hợi"),
    # Đinh years (can_idx=3) - FIXED
    (3, 0): ("Mộc", "Đinh Tý"), (3, 1): ("Mộc", "Đinh Sửu"), (3, 2): ("Hỏa", "Đinh Dần"), (3, 3): ("Hỏa", "Đinh Mão"),
    (3, 4): ("Hỏa", "Đinh Thìn"), (3, 5): ("Hỏa", "Đinh Tỵ"), (3, 6): ("Thổ", "Đinh Ngọ"), (3, 7): ("Thổ", "Đinh Mùi"),
    (3, 8): ("Kim", "Đinh Thân"), (3, 9): ("Kim", "Đinh Dậu"), (3, 10): ("Kim", "Đinh Tuất"), (3, 11): ("Mộc", "Đinh Hợi"),
    # Mậu years (can_idx=4) - FIXED
    (4, 0): ("Hỏa", "Mậu Tý"), (4, 1): ("Hỏa", "Mậu Sửu"), (4, 2): ("Hỏa", "Mậu Dần"), (4, 3): ("Thổ", "Mậu Mão"),
    (4, 4): ("Thổ", "Mậu Thìn"), (4, 5): ("Kim", "Mậu Tỵ"), (4, 6): ("Kim", "Mậu Ngọ"), (4, 7): ("Kim", "Mậu Mùi"),
    (4, 8): ("Mộc", "Mậu Thân"), (4, 9): ("Mộc", "Mậu Dậu"), (4, 10): ("Mộc", "Mậu Tuất"), (4, 11): ("Mộc", "Mậu Hợi"),
    # Kỷ years (can_idx=5) - FIXED
    (5, 0): ("Hỏa", "Kỷ Tý"), (5, 1): ("Hỏa", "Kỷ Sửu"), (5, 2): ("Thổ", "Kỷ Dần"), (5, 3): ("Thổ", "Kỷ Mão"),
    (5, 4): ("Kim", "Kỷ Thìn"), (5, 5): ("Kim", "Kỷ Tỵ"), (5, 6): ("Kim", "Kỷ Ngọ"), (5, 7): ("Mộc", "Kỷ Mùi"),
    (5, 8): ("Mộc", "Kỷ Thân"), (5, 9): ("Mộc", "Kỷ Dậu"), (5, 10): ("Mộc", "Kỷ Tuất"), (5, 11): ("Hỏa", "Kỷ Hợi"),
    # Canh years (can_idx=6) - FIXED
    (6, 0): ("Thổ", "Canh Tý"), (6, 1): ("Kim", "Canh Sửu"), (6, 2): ("Kim", "Canh Dần"), (6, 3): ("Kim", "Canh Mão"),
    (6, 4): ("Kim", "Canh Thìn"), (6, 5): ("Mộc", "Canh Tỵ"), (6, 6): ("Mộc", "Canh Ngọ"), (6, 7): ("Mộc", "Canh Mùi"),
    (6, 8): ("Mộc", "Canh Thân"), (6, 9): ("Hỏa", "Canh Dậu"), (6, 10): ("Hỏa", "Canh Tuất"), (6, 11): ("Hỏa", "Canh Hợi"),
    # Tân years (can_idx=7) - FIXED
    (7, 0): ("Kim", "Tân Tý"), (7, 1): ("Kim", "Tân Sửu"), (7, 2): ("Kim", "Tân Dần"), (7, 3): ("Mộc", "Tân Mão"),
    (7, 4): ("Mộc", "Tân Thìn"), (7, 5): ("Mộc", "Tân Tỵ"), (7, 6): ("Hỏa", "Tân Ngọ"), (7, 7): ("Hỏa", "Tân Mùi"),
    (7, 8): ("Thủy", "Tân Thân"), (7, 9): ("Thủy", "Tân Dậu"), (7, 10): ("Thủy", "Tân Tuất"), (7, 11): ("Thủy", "Tân Hợi"),
    # Nhâm years (can_idx=8) - FIXED
    (8, 0): ("Mộc", "Nhâm Tý"), (8, 1): ("Mộc", "Nhâm Sửu"), (8, 2): ("Hỏa", "Nhâm Dần"), (8, 3): ("Hỏa", "Nhâm Mão"),
    (8, 4): ("Hỏa", "Nhâm Thìn"), (8, 5): ("Thủy", "Nhâm Tỵ"), (8, 6): ("Thủy", "Nhâm Ngọ"), (8, 7): ("Thủy", "Nhâm Mùi"),
    (8, 8): ("Thổ", "Nhâm Thân"), (8, 9): ("Thổ", "Nhâm Dậu"), (8, 10): ("Kim", "Nhâm Tuất"), (8, 11): ("Kim", "Nhâm Hợi"),
    # Quý years (can_idx=9) - FIXED
    (9, 0): ("Mộc", "Quý Tý"), (9, 1): ("Hỏa", "Quý Sửu"), (9, 2): ("Hỏa", "Quý Dần"), (9, 3): ("Thủy", "Quý Mão"),
    (9, 4): ("Thủy", "Quý Thìn"), (9, 5): ("Thổ", "Quý Tỵ"), (9, 6): ("Thổ", "Quý Ngọ"), (9, 7): ("Kim", "Quý Mùi"),
    (9, 8): ("Kim", "Quý Thân"), (9, 9): ("Kim", "Quý Dậu"), (9, 10): ("Kim", "Quý Tuất"), (9, 11): ("Hỏa", "Quý Hợi"),
}

# Cục lookup: (cung_menh_chi_idx, ngu_hanh) -> cuc number (2-6)
CUC_TABLE = {
    # Tý branch
    ("Tý", "Kim"): 4, ("Tý", "Mộc"): 3, ("Tý", "Hỏa"): 6, ("Tý", "Thủy"): 2, ("Tý", "Thổ"): 5,
    # Sửu branch
    ("Sửu", "Kim"): 5, ("Sửu", "Mộc"): 4, ("Sửu", "Hỏa"): 3, ("Sửu", "Thủy"): 6, ("Sửu", "Thổ"): 2,
    # Dần branch
    ("Dần", "Kim"): 2, ("Dần", "Mộc"): 5, ("Dần", "Hỏa"): 4, ("Dần", "Thủy"): 3, ("Dần", "Thổ"): 6,
    # Mão branch
    ("Mão", "Kim"): 6, ("Mão", "Mộc"): 2, ("Mão", "Hỏa"): 5, ("Mão", "Thủy"): 4, ("Mão", "Thổ"): 3,
    # Thìn branch
    ("Thìn", "Kim"): 3, ("Thìn", "Mộc"): 6, ("Thìn", "Hỏa"): 2, ("Thìn", "Thủy"): 5, ("Thìn", "Thổ"): 4,
    # Tỵ branch
    ("Tỵ", "Kim"): 4, ("Tỵ", "Mộc"): 3, ("Tỵ", "Hỏa"): 6, ("Tỵ", "Thủy"): 2, ("Tỵ", "Thổ"): 5,
    # Ngọ branch
    ("Ngọ", "Kim"): 5, ("Ngọ", "Mộc"): 4, ("Ngọ", "Hỏa"): 3, ("Ngọ", "Thủy"): 6, ("Ngọ", "Thổ"): 2,
    # Mùi branch
    ("Mùi", "Kim"): 2, ("Mùi", "Mộc"): 5, ("Mùi", "Hỏa"): 4, ("Mùi", "Thủy"): 3, ("Mùi", "Thổ"): 6,
    # Thân branch
    ("Thân", "Kim"): 6, ("Thân", "Mộc"): 2, ("Thân", "Hỏa"): 5, ("Thân", "Thủy"): 4, ("Thân", "Thổ"): 3,
    # Dậu branch
    ("Dậu", "Kim"): 3, ("Dậu", "Mộc"): 6, ("Dậu", "Hỏa"): 2, ("Dậu", "Thủy"): 5, ("Dậu", "Thổ"): 4,
    # Tuất branch
    ("Tuất", "Kim"): 4, ("Tuất", "Mộc"): 3, ("Tuất", "Hỏa"): 6, ("Tuất", "Thủy"): 2, ("Tuất", "Thổ"): 5,
    # Hợi branch
    ("Hợi", "Kim"): 5, ("Hợi", "Mộc"): 4, ("Hợi", "Hỏa"): 3, ("Hợi", "Thủy"): 6, ("Hợi", "Thổ"): 2,
}

# Cục names
CUC_NAMES = {
    2: "Thủy Nhị Cục",
    3: "Mộc Tam Cục",
    4: "Kim Tứ Cục",
    5: "Thổ Ngũ Cục",
    6: "Hỏa Lục Cục"
}

# Tử Vi position lookup: (cuc, lunar_day) -> palace position (1-12)
# Simplified - using common days
TUVI_POSITION = {
    # For Thủy Nhị Cục (cuc=2)
    (2, 1): 1, (2, 2): 2, (2, 3): 3, (2, 4): 4, (2, 5): 5, (2, 6): 6,
    (2, 7): 7, (2, 8): 8, (2, 9): 9, (2, 10): 10, (2, 11): 11, (2, 12): 12,
    (2, 13): 1, (2, 14): 2, (2, 15): 3, (2, 16): 4, (2, 17): 5, (2, 18): 6,
    (2, 19): 7, (2, 20): 8, (2, 21): 9, (2, 22): 10, (2, 23): 11, (2, 24): 12,
    (2, 25): 1, (2, 26): 2, (2, 27): 3, (2, 28): 4, (2, 29): 5, (2, 30): 6,
    # For Mộc Tam Cục (cuc=3)
    (3, 1): 7, (3, 2): 8, (3, 3): 9, (3, 4): 10, (3, 5): 11, (3, 6): 12,
    (3, 7): 1, (3, 8): 2, (3, 9): 3, (3, 10): 4, (3, 11): 5, (3, 12): 6,
    (3, 13): 7, (3, 14): 8, (3, 15): 9, (3, 16): 10, (3, 17): 11, (3, 18): 12,
    (3, 19): 1, (3, 20): 2, (3, 21): 3, (3, 22): 4, (3, 23): 5, (3, 24): 6,
    (3, 25): 7, (3, 26): 8, (3, 27): 9, (3, 28): 10, (3, 29): 11, (3, 30): 12,
    # For Kim Tứ Cục (cuc=4)
    (4, 1): 4, (4, 2): 5, (4, 3): 6, (4, 4): 7, (4, 5): 8, (4, 6): 9,
    (4, 7): 10, (4, 8): 11, (4, 9): 12, (4, 10): 1, (4, 11): 2, (4, 12): 3,
    (4, 13): 4, (4, 14): 5, (4, 15): 6, (4, 16): 7, (4, 17): 8, (4, 18): 9,
    (4, 19): 10, (4, 20): 11, (4, 21): 12, (4, 22): 1, (4, 23): 2, (4, 24): 3,
    (4, 25): 4, (4, 26): 5, (4, 27): 6, (4, 28): 7, (4, 29): 8, (4, 30): 9,
    # For Thổ Ngũ Cục (cuc=5)
    (5, 1): 10, (5, 2): 11, (5, 3): 12, (5, 4): 1, (5, 5): 2, (5, 6): 3,
    (5, 7): 4, (5, 8): 5, (5, 9): 6, (5, 10): 7, (5, 11): 8, (5, 12): 9,
    (5, 13): 10, (5, 14): 11, (5, 15): 12, (5, 16): 1, (5, 17): 2, (5, 18): 3,
    (5, 19): 4, (5, 20): 5, (5, 21): 6, (5, 22): 7, (5, 23): 8, (5, 24): 9,
    (5, 25): 10, (5, 26): 11, (5, 27): 12, (5, 28): 1, (5, 29): 2, (5, 30): 3,
    # For Hỏa Lục Cục (cuc=6)
    (6, 1): 1, (6, 2): 2, (6, 3): 3, (6, 4): 4, (6, 5): 5, (6, 6): 6,
    (6, 7): 7, (6, 8): 8, (6, 9): 9, (6, 10): 10, (6, 11): 11, (6, 12): 12,
    (6, 13): 1, (6, 14): 2, (6, 15): 3, (6, 16): 4, (6, 17): 5, (6, 18): 6,
    (6, 19): 7, (6, 20): 8, (6, 21): 9, (6, 22): 10, (6, 23): 11, (6, 24): 12,
    (6, 25): 1, (6, 26): 2, (6, 27): 3, (6, 28): 4, (6, 29): 5, (6, 30): 6,
}

# Star offsets from Tử Vi (counter-clockwise)
# Group 1: Tu Vi group (6 stars)
TUVI_GROUP_OFFSETS = {
    "Thiên Cơ": -1,    # -1 from Tu Vi
    "Thái Dương": -3,  # -3 from Tu Vi
    "Vũ Khúc": -4,     # -4 from Tu Vi
    "Thiên Đồng": -5,  # -5 from Tu Vi
    "Liêm Trinh": 4,    # +4 from Tu Vi (equiv -8 mod 12)
}

# Star offsets from Thiên Phủ (clockwise)
# Group 2: Thien Phu group (8 stars)
THIEN_PHU_GROUP_OFFSETS = {
    "Thái Âm": 1,
    "Tham Lang": 2,
    "Cự Môn": 3,
    "Thiên Tướng": 4,
    "Thiên Lương": 5,
    "Thất Sát": 6,
    "Phá Quân": 8,  # Fixed: +8 not +10
}


def get_thien_phu_position(tu_vi_pos: int, cung_menh_pos: int) -> int:
    """
    Calculate Thiên Phủ position - mirrors Tử Vi across a fixed axis.

    The axis depends on the Cục. Simplified formula:
    Thien Phu = (Cung Menh position + 6 - Tu Vi position) mod 12
    """
    # Axis depends on Cục - simplified using Cung Mệnh position
    axis = (cung_menh_pos + 6) % 12
    thien_phu_pos = (axis - tu_vi_pos + 12) % 12
    return thien_phu_pos + 1  # Convert to 1-based


# Cục calculation table: (can_idx, cung_menh_chi_idx) -> cuc number (2-6)
# Based on Year Can and Cung Menh position (1-12)
CUC_CALC_TABLE = {
    # Giáp (can_idx=0)
    (0, 1): 4, (0, 2): 3, (0, 3): 2, (0, 4): 5, (0, 5): 6, (0, 6): 4,
    (0, 7): 3, (0, 8): 2, (0, 9): 5, (0, 10): 6, (0, 11): 4, (0, 12): 3,
    # Ất (can_idx=1)
    (1, 1): 3, (1, 2): 2, (1, 3): 5, (1, 4): 6, (1, 5): 4, (1, 6): 3,
    (1, 7): 2, (1, 8): 5, (1, 9): 6, (1, 10): 4, (1, 11): 3, (1, 12): 2,
    # Bính (can_idx=2)
    (2, 1): 2, (2, 2): 5, (2, 3): 6, (2, 4): 4, (2, 5): 3, (2, 6): 2,
    (2, 7): 5, (2, 8): 6, (2, 9): 4, (2, 10): 3, (2, 11): 2, (2, 12): 5,
    # Đinh (can_idx=3)
    (3, 1): 5, (3, 2): 6, (3, 3): 4, (3, 4): 3, (3, 5): 2, (3, 6): 5,
    (3, 7): 6, (3, 8): 4, (3, 9): 3, (3, 10): 2, (3, 11): 5, (3, 12): 6,
    # Mậu (can_idx=4)
    (4, 1): 6, (4, 2): 4, (4, 3): 3, (4, 4): 2, (4, 5): 5, (4, 6): 6,
    (4, 7): 4, (4, 8): 3, (4, 9): 2, (4, 10): 5, (4, 11): 6, (4, 12): 4,
    # Kỷ (can_idx=5)
    (5, 1): 4, (5, 2): 3, (5, 3): 2, (5, 4): 5, (5, 5): 6, (5, 6): 4,
    (5, 7): 3, (5, 8): 2, (5, 9): 5, (5, 10): 6, (5, 11): 4, (5, 12): 3,
    # Canh (can_idx=6)
    (6, 1): 3, (6, 2): 2, (6, 3): 5, (6, 4): 6, (6, 5): 4, (6, 6): 3,
    (6, 7): 2, (6, 8): 5, (6, 9): 6, (6, 10): 4, (6, 11): 3, (6, 12): 2,
    # Tân (can_idx=7)
    (7, 1): 2, (7, 2): 5, (7, 3): 6, (7, 4): 4, (7, 5): 3, (7, 6): 2,
    (7, 7): 5, (7, 8): 6, (7, 9): 4, (7, 10): 3, (7, 11): 2, (7, 12): 5,
    # Nhâm (can_idx=8)
    (8, 1): 5, (8, 2): 6, (8, 3): 4, (8, 4): 3, (8, 5): 2, (8, 6): 5,
    (8, 7): 6, (8, 8): 4, (8, 9): 3, (8, 10): 2, (8, 11): 5, (8, 12): 6,
    # Quý (can_idx=9)
    (9, 1): 6, (9, 2): 4, (9, 3): 3, (9, 4): 2, (9, 5): 5, (9, 6): 6,
    (9, 7): 4, (9, 8): 3, (9, 9): 2, (9, 10): 5, (9, 11): 6, (9, 12): 4,
}


def calculate_cuc(year_can: str, cung_menh_chi: str) -> int:
    """
    Calculate Cục number based on year can and Cung Menh earthly branch.

    Args:
        year_can: Year stem (Giáp, Ất, etc.)
        cung_menh_chi: Cung Menh earthly branch (Tý, Sửu, Dần, etc.)

    Returns:
        Cục number: 2 (Thủy Nhị), 3 (Mộc Tam), 4 (Kim Tứ), 5 (Thổ Ngũ), 6 (Hỏa Lục)
    """
    can_idx = get_can_idx(year_can)
    # Convert Cung Menh position to chi index (1=Tý, 2=Sửu, etc.)
    chi_idx = {"Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tỵ": 6,
                "Ngọ": 7, "Mùi": 8, "Thân": 9, "Dậu": 10, "Tuất": 11, "Hợi": 12}.get(cung_menh_chi, 1)

    key = (can_idx, chi_idx)
    return CUC_CALC_TABLE.get(key, 4)  # Default to Kim Tứ


def calculate_tu_vi_position(cuc: int, lunar_day: int) -> int:
    """
    Calculate Tử Vi position based on Cục and lunar day.

    Args:
        cuc: Cục number (2-6)
        lunar_day: Lunar day (1-30)

    Returns:
        Palace position (1-12)
    """
    key = (cuc, lunar_day)
    if key in TUVI_POSITION:
        return TUVI_POSITION[key]
    # Fallback formula
    offset = (lunar_day + cuc) % 12
    return offset + 1


def apply_offset(base_pos: int, offset: int) -> int:
    """Apply offset to position, handling wrap-around."""
    return ((base_pos - 1 + offset) % 12) + 1

# Dignity table: (star, palace) -> dignity name
# Simplified - Miếu/Đắc/Vượng/Bình/Hãm
DIGNITY_TABLE = {
    # Tử Vi
    ("Tử Vi", "Mệnh"): "Miếu", ("Tử Vi", "Phụ Mẫu"): "Đắc", ("Tử Vi", "Huynh Đệ"): "Vượng",
    ("Tử Vi", "Tử Tức"): "Bình", ("Tử Vi", "Phúc Đức"): "Hãm", ("Tử Vi", "Điền Trạch"): "Miếu",
    ("Tử Vi", "Quan Lộc"): "Đắc", ("Tử Vi", "Thiên Di"): "Vượng", ("Tử Vi", "Tài Bạch"): "Bình",
    ("Tử Vi", "Tật Ách"): "Hãm", ("Tử Vi", "Nô Bộc"): "Miếu", ("Tử Vi", "Phu Thê"): "Đắc",
    # Default for other stars/palaces
}

def get_dignity(star: str, palace: str, cung_menh_pos: int) -> str:
    """Get star dignity for a palace."""
    # Simplified: return Bình (neutral) as default
    # Full table would have 168 entries
    key = (star, palace)
    if key in DIGNITY_TABLE:
        return DIGNITY_TABLE[key]
    return "Bình"

def get_can_idx(can: str) -> int:
    """Get can index 0-9."""
    return CAN.index(can) if can in CAN else 0

def get_chi_idx(chi: str) -> int:
    """Get chi index 0-11."""
    return CHI.index(chi) if chi in CHI else 0
