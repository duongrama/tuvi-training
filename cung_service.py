"""
12 Cung Service - Vietnamese Astrology (Tử Vi)

Provides Cung placement calculations based on traditional Tử Vi system:
- Nạp Âm (Ngũ Hành classification)
- Cung Mệnh (Life Palace)
- Cung Thân (Body Palace)
- 12 Cung placement
"""

from typing import Optional, Dict, Tuple
from tu_vi.data.tuvi_tables import NAP_AM_TABLE


# 12 Cung names
CUNG = [
    "Mệnh",      # 1 - Life
    "Phụ Mẫu",   # 2 - Parents
    "Huynh Đệ",  # 3 - Siblings
    "Tử Tức",    # 4 - Children
    "Phúc Đức",  # 5 - Fortune
    "Điền Trạch", # 6 - Property
    "Quan Lộc", # 7 - Authority (was Quyền Quý)
    "Thiên Di",   # 8 - Travel
    "Tài Bạch",   # 9 - Wealth
    "Tật Ách",   # 10 - Career (was Tập Ách)
    "Nô Bộc",    # 11 - Subordinates
    "Phu Thê"   # 12 - Spouse (was Chu Tước)
]


# Nạp Âm table - maps year stems to classification
# Based on: odd years = Dương, even years = Âm, but with specific exceptions
NAP_AM = {
    "Giáp": "Dương",
    "Ất": "Âm",
    "Bính": "Dương",
    "Đinh": "Âm",
    "Mậu": "Dương",
    "Kỷ": "Âm",
    "Canh": "Dương",
    "Tân": "Âm",
    "Nhâm": "Dương",
    "Quý": "Âm",
}

# Can and Chi index maps
CAN_IDX = {"Giáp": 0, "Ất": 1, "Bính": 2, "Đinh": 3, "Mậu": 4, "Kỷ": 5,
           "Canh": 6, "Tân": 7, "Nhâm": 8, "Quý": 9}
CHI_IDX = {"Tý": 0, "Sửu": 1, "Dần": 2, "Mão": 3, "Thìn": 4, "Tỵ": 5,
           "Ngọ": 6, "Mùi": 7, "Thân": 8, "Dậu": 9, "Tuất": 10, "Hợi": 11}


def get_nap_am_info(year_can: str, year_chi: str) -> Dict[str, str]:
    """
    Get full Nạp Âm info (element + name) from year can and chi.

    Args:
        year_can: Year stem (Giáp, Ất, etc.)
        year_chi: Year branch (Tý, Sửu, etc.)

    Returns:
        dict with 'ngu_hanh' (element) and 'name' (full Nạp Âm name)
    """
    can_idx = CAN_IDX.get(year_can, 0)
    chi_idx = CHI_IDX.get(year_chi, 0)
    key = (can_idx, chi_idx)
    result = NAP_AM_TABLE.get(key, ("Kim", "Giáp Tý"))
    return {"ngu_hanh": result[0], "name": result[1]}


# Cung Mệnh calculation table
# Based on lunar month and hour (using 12 earthly branches for hours)
# Simplified: uses month-branch and hour-branch to find Mệnh cung

# Hour branches (12 double-hours)
HOUR_BRANCH = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Month branches
MONTH_BRANCH = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]


# Cung Mệnh lookup table: (month_branch, hour_branch) -> cung_index
# This is a simplified version of the traditional calculation
MENH_TABLE = {
    # Dần month
    ("Dần", "Tý"): 0, ("Dần", "Sửu"): 11, ("Dần", "Dần"): 10, ("Dần", "Mão"): 9,
    ("Dần", "Thìn"): 8, ("Dần", "Tỵ"): 7, ("Dần", "Ngọ"): 6, ("Dần", "Mùi"): 5,
    ("Dần", "Thân"): 4, ("Dần", "Dậu"): 3, ("Dần", "Tuất"): 2, ("Dần", "Hợi"): 1,
    # Mão month
    ("Mão", "Tý"): 1, ("Mão", "Sửu"): 0, ("Mão", "Dần"): 11, ("Mão", "Mão"): 10,
    ("Mão", "Thìn"): 9, ("Mão", "Tỵ"): 8, ("Mão", "Ngọ"): 7, ("Mão", "Mùi"): 6,
    ("Mão", "Thân"): 5, ("Mão", "Dậu"): 4, ("Mão", "Tuất"): 3, ("Mão", "Hợi"): 2,
    # Thìn month
    ("Thìn", "Tý"): 2, ("Thìn", "Sửu"): 1, ("Thìn", "Dần"): 0, ("Thìn", "Mão"): 11,
    ("Thìn", "Thìn"): 10, ("Thìn", "Tỵ"): 9, ("Thìn", "Ngọ"): 8, ("Thìn", "Mùi"): 7,
    ("Thìn", "Thân"): 6, ("Thìn", "Dậu"): 5, ("Thìn", "Tuất"): 4, ("Thìn", "Hợi"): 3,
    # Tỵ month
    ("Tỵ", "Tý"): 3, ("Tỵ", "Sửu"): 2, ("Tỵ", "Dần"): 1, ("Tỵ", "Mão"): 0,
    ("Tỵ", "Thìn"): 11, ("Tỵ", "Tỵ"): 10, ("Tỵ", "Ngọ"): 9, ("Tỵ", "Mùi"): 8,
    ("Tỵ", "Thân"): 7, ("Tỵ", "Dậu"): 6, ("Tỵ", "Tuất"): 5, ("Tỵ", "Hợi"): 4,
    # Ngọ month
    ("Ngọ", "Tý"): 4, ("Ngọ", "Sửu"): 3, ("Ngọ", "Dần"): 2, ("Ngọ", "Mão"): 1,
    ("Ngọ", "Thìn"): 0, ("Ngọ", "Tỵ"): 11, ("Ngọ", "Ngọ"): 10, ("Ngọ", "Mùi"): 9,
    ("Ngọ", "Thân"): 8, ("Ngọ", "Dậu"): 7, ("Ngọ", "Tuất"): 6, ("Ngọ", "Hợi"): 5,
    # Mùi month
    ("Mùi", "Tý"): 5, ("Mùi", "Sửu"): 4, ("Mùi", "Dần"): 3, ("Mùi", "Mão"): 2,
    ("Mùi", "Thìn"): 1, ("Mùi", "Tỵ"): 0, ("Mùi", "Ngọ"): 11, ("Mùi", "Mùi"): 10,
    ("Mùi", "Thân"): 9, ("Mùi", "Dậu"): 8, ("Mùi", "Tuất"): 7, ("Mùi", "Hợi"): 6,
    # Thân month
    ("Thân", "Tý"): 6, ("Thân", "Sửu"): 5, ("Thân", "Dần"): 4, ("Thân", "Mão"): 3,
    ("Thân", "Thìn"): 2, ("Thân", "Tỵ"): 1, ("Thân", "Ngọ"): 0, ("Thân", "Mùi"): 11,
    ("Thân", "Thân"): 10, ("Thân", "Dậu"): 9, ("Thân", "Tuất"): 8, ("Thân", "Hợi"): 7,
    # Dậu month
    ("Dậu", "Tý"): 7, ("Dậu", "Sửu"): 6, ("Dậu", "Dần"): 5, ("Dậu", "Mão"): 4,
    ("Dậu", "Thìn"): 3, ("Dậu", "Tỵ"): 2, ("Dậu", "Ngọ"): 1, ("Dậu", "Mùi"): 0,
    ("Dậu", "Thân"): 11, ("Dậu", "Dậu"): 10, ("Dậu", "Tuất"): 9, ("Dậu", "Hợi"): 8,
    # Tuất month
    ("Tuất", "Tý"): 8, ("Tuất", "Sửu"): 7, ("Tuất", "Dần"): 6, ("Tuất", "Mão"): 5,
    ("Tuất", "Thìn"): 4, ("Tuất", "Tỵ"): 3, ("Tuất", "Ngọ"): 2, ("Tuất", "Mùi"): 1,
    ("Tuất", "Thân"): 0, ("Tuất", "Dậu"): 11, ("Tuất", "Tuất"): 10, ("Tuất", "Hợi"): 9,
    # Hợi month
    ("Hợi", "Tý"): 9, ("Hợi", "Sửu"): 8, ("Hợi", "Dần"): 7, ("Hợi", "Mão"): 6,
    ("Hợi", "Thìn"): 5, ("Hợi", "Tỵ"): 4, ("Hợi", "Ngọ"): 3, ("Hợi", "Mùi"): 2,
    ("Hợi", "Thân"): 1, ("Hợi", "Dậu"): 0, ("Hợi", "Tuất"): 11, ("Hợi", "Hợi"): 10,
    # Tý month
    ("Tý", "Tý"): 10, ("Tý", "Sửu"): 9, ("Tý", "Dần"): 8, ("Tý", "Mão"): 7,
    ("Tý", "Thìn"): 6, ("Tý", "Tỵ"): 5, ("Tý", "Ngọ"): 4, ("Tý", "Mùi"): 3,
    ("Tý", "Thân"): 2, ("Tý", "Dậu"): 1, ("Tý", "Tuất"): 0, ("Tý", "Hợi"): 11,
    # Sửu month
    ("Sửu", "Tý"): 11, ("Sửu", "Sửu"): 10, ("Sửu", "Dần"): 9, ("Sửu", "Mão"): 8,
    ("Sửu", "Thìn"): 7, ("Sửu", "Tỵ"): 6, ("Sửu", "Ngọ"): 5, ("Sửu", "Mùi"): 4,
    ("Sửu", "Thân"): 3, ("Sửu", "Dậu"): 2, ("Sửu", "Tuất"): 1, ("Sửu", "Hợi"): 0,
}


def get_nap_am(year_can: str) -> str:
    """Get Nạp Âm (Yin/Yang) classification from year stem."""
    return NAP_AM.get(year_can, "Dương")


def get_nap_am_element(year_can: str) -> str:
    """Get Nạp Âm element (Kim, Mộc, Thủy, Hỏa, Thổ) from year can."""
    # Simplified: based on year can
    can_elements = {
        "Giáp": "Mộc", "Ất": "Mộc",
        "Bính": "Hỏa", "Đinh": "Hỏa",
        "Mậu": "Thổ", "Kỷ": "Thổ",
        "Canh": "Kim", "Tân": "Kim",
        "Nhâm": "Thủy", "Quý": "Thủy"
    }
    return can_elements.get(year_can, "Kim")


def get_hour_branch(hour: int) -> str:
    """Get hour branch (Chi) from hour (0-23)."""
    # Double-hour system: each branch covers 2 hours
    # 23-1 = Tý, 1-3 = Sửu, etc.
    idx = ((hour + 1) // 2) % 12
    return HOUR_BRANCH[idx]


def calculate_12_cung(lunar_month: int, lunar_year_can: str, hour: int, year_chi: str = "Tý") -> dict:
    """
    Calculate 12 Cung placement.

    Args:
        lunar_month: Lunar month (1-12)
        lunar_year_can: Year stem (Giáp, Ất, etc.)
        hour: Birth hour (0-23)
        year_chi: Year branch (Tý, Sửu, etc.) - optional, for full Nạp Âm

    Returns:
        dict with 12 cung placement
    """
    # Get month branch
    month_branch = MONTH_BRANCH[lunar_month - 1]

    # Get hour branch
    hour_branch = get_hour_branch(hour)

    # Calculate Cung Mệnh
    menh_key = (month_branch, hour_branch)
    menh_index = MENH_TABLE.get(menh_key, 0)

    # Cung Thân is opposite (6 positions away)
    than_index = (menh_index + 6) % 12

    # Build 12 cung in order starting from Mệnh
    cungs = {}
    for i in range(12):
        cung_idx = (menh_index + i) % 12
        cungs[CUNG[i]] = CUNG[cung_idx]

    # Get full Nạp Âm info if year_chi provided
    nap_am_info = get_nap_am_info(lunar_year_can, year_chi)

    return {
        "nap_am": nap_am_info,
        "cung_menh": CUNG[menh_index],
        "cung_than": CUNG[than_index],
        "month_branch": month_branch,
        "hour_branch": hour_branch,
        "cungs": cungs
    }


def get_cung_details(cungs: dict, nap_am: str) -> dict:
    """
    Get detailed information for each cung.

    Args:
        cungs: 12 cung placement dict
        nap_am: Nạp Âm classification

    Returns:
        dict with cung details
    """
    cung_details = {}

    # Basic descriptions
    descriptions = {
        "Mệnh": "Cung Mệnh - Vận mệnh, cuộc đời, số phận",
        "Phụ Mẫu": "Cung Phụ Mẫu - Cha mẹ, tổ tiên",
        "Huynh Đệ": "Cung Huynh Đệ - Anh chị em, bạn bè",
        "Tử Tức": "Cung Tử Tức - Con cái, hậu duệ",
        "Phúc Đức": "Cung Phúc Đức - Phúc lộc, may mắn",
        "Điền Trạch": "Cung Điền Trạch - Nhà cửa, đất đai",
        "Quan Lộc": "Cung Quan Lộc - Sự nghiệp, công việc",
        "Thiên Di": "Cung Thiên Di - Xuất ngoại, du lịch",
        "Tài Bạch": "Cung Tài Bạch - Tài lộc, tiền bạc",
        "Tật Ách": "Cung Tật Ách - Tài lộc, bệnh tật",
        "Nô Bộc": "Cung Nô Bộc - Quần thần, đồng nghiệp",
        "Phu Thê": "Cung Phu Thê - Hôn nhân, vợ chồng",
    }

    for cung_name, cung_value in cungs.items():
        cung_details[cung_name] = {
            "star": cung_value,
            "description": descriptions.get(cung_name, ""),
            "is_dien": nap_am == "Âm"  # Simplified: Âm years have different interpretations
        }

    return cung_details
