"""
An Sao Service - Tử Vi Star Placement

Calculates Cục and places 14 Chính Tinh into 12 palaces.
Based on traditional Vietnamese astrology algorithm.
"""

from typing import Dict, List, Tuple
from tu_vi.data.tuvi_tables import (
    CHINH_TINH, STAR_ELEMENT, TUVI_POSITION, TUVI_GROUP_OFFSETS,
    THIEN_PHU_GROUP_OFFSETS, get_thien_phu_position, calculate_cuc,
    calculate_tu_vi_position, apply_offset, CUC_NAMES, CUNG
)
from tu_vi.cung_service import get_nap_am_info


def get_cung_menh_chi(cung_menh: str, cung_menh_pos: int) -> str:
    """Get Cung Menh earthly branch from cung position."""
    # CUNG is [Mệnh, Phụ Mẫu, ...] - positions 1-12
    # CHI is [Tý, Sửu, Dần, ...] - 12 branches in order starting from Tý
    # When Cung Mệnh is at position X, it corresponds to CHI[X-1]
    chi_list = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
    return chi_list[(cung_menh_pos - 1) % 12]


def place_14_chinh_tinh(
    year_can: str,
    cung_menh: str,
    cung_menh_pos: int,
    lunar_day: int
) -> Dict[str, Dict]:
    """
    Place 14 Chính Tinh into 12 palaces.

    Args:
        year_can: Year stem (Giáp, Ất, etc.)
        cung_menh: Cung Menh name
        cung_menh_pos: Cung Menh position (1-12)
        lunar_day: Lunar day (1-30)

    Returns:
        Dict of star_name -> {position, cung, element, dignity}
    """
    # Step 1: Calculate Cục
    cung_menh_chi = get_cung_menh_chi(cung_menh, cung_menh_pos)
    cuc = calculate_cuc(year_can, cung_menh_chi)

    # Step 2: Calculate Tử Vi position
    tu_vi_pos = calculate_tu_vi_position(cuc, lunar_day)

    # Step 3: Place Group 1 - Tử Vi group (6 stars)
    # Tử Vi is at calculated position
    # Other 5 stars at fixed offsets counter-clockwise from Tử Vi
    stars = {}

    # Tử Vi
    stars["Tử Vi"] = {
        "position": tu_vi_pos,
        "cung": CUNG[tu_vi_pos - 1],
        "element": STAR_ELEMENT["Tử Vi"]
    }

    # Group 1 stars (counter-clockwise from Tu Vi)
    for star_name, offset in TUVI_GROUP_OFFSETS.items():
        pos = apply_offset(tu_vi_pos, offset)
        stars[star_name] = {
            "position": pos,
            "cung": CUNG[pos - 1],
            "element": STAR_ELEMENT.get(star_name, "Thổ")
        }

    # Step 4: Place Group 2 - Thiên Phủ group (8 stars)
    # Thiên Phủ mirrors Tử Vi across axis
    thien_phu_pos = get_thien_phu_position(tu_vi_pos, cung_menh_pos)

    # Thiên Phủ
    stars["Thiên Phủ"] = {
        "position": thien_phu_pos,
        "cung": CUNG[thien_phu_pos - 1],
        "element": STAR_ELEMENT["Thiên Phủ"]
    }

    # Group 2 stars (clockwise from Thien Phu)
    for star_name, offset in THIEN_PHU_GROUP_OFFSETS.items():
        pos = apply_offset(thien_phu_pos, offset)
        stars[star_name] = {
            "position": pos,
            "cung": CUNG[pos - 1],
            "element": STAR_ELEMENT.get(star_name, "Thổ")
        }

    return stars, cuc


def build_palaces_with_stars(stars: Dict[str, Dict]) -> List[Dict]:
    """
    Build palace structure with stars grouped by position.

    Args:
        stars: Dict of star_name -> {position, cung, element}

    Returns:
        List of 12 palaces with stars
    """
    # Group stars by position
    palaces = {i: {"position": i, "dia_chi": CUNG[i-1], "cung_name": CUNG[i-1], "stars": []}
               for i in range(1, 13)}

    for star_name, star_info in stars.items():
        pos = star_info["position"]
        palaces[pos]["stars"].append({
            "name": star_name,
            "element": star_info["element"]
        })

    return list(palaces.values())


def get_full_chart(birth_data: dict, year_can: str, year_chi: str,
                   cung_menh: str, cung_menh_pos: int, gender: str = "nam") -> dict:
    """
    Build complete Tử Vi chart.

    Args:
        birth_data: Birth info from lunar_service
        year_can: Year stem
        year_chi: Year branch
        cung_menh: Cung Menh name
        cung_menh_pos: Cung Menh position (1-12)
        gender: "nam" or "nữ"

    Returns:
        Complete chart dict
    """
    lunar = birth_data.get("lunar", {})
    lunar_day = lunar.get("day", 15)

    # Calculate Cục and place stars
    stars, cuc = place_14_chinh_tinh(year_can, cung_menh, cung_menh_pos, lunar_day)

    # Build palaces
    palaces = build_palaces_with_stars(stars)

    # Get Cục name
    cuc_name = CUC_NAMES.get(cuc, "Kim Tứ Cục")

    # Get Nạp Âm info
    nap_am_info = get_nap_am_info(year_can, year_chi)

    return {
        "birth": birth_data,
        "gender": gender,
        "nap_am": nap_am_info,
        "cuc": {"value": cuc, "name": cuc_name},
        "cung_menh": cung_menh,
        "palaces": palaces,
        "stars": stars
    }
