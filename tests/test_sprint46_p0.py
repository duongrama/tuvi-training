"""Sprint 46 P0 Tests — 33 lunar conversion + 13 hour mapping cases."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from tu_vi.iztro_service import solar_to_lunar_via_library, get_iztro_hour


# ── Hour Mapping: 13 cases ───────────────────────────────────────────────

@pytest.mark.parametrize("hour,expected", [
    (0,  0),   # Early Tý
    (1,  0),   # Early Tý
    (2,  1),   # Sửu
    (4,  2),   # Dần
    (6,  3),   # Mão
    (8,  4),   # Thìn
    (10, 5),   # Tỵ
    (12, 6),   # Ngọ
    (14, 7),   # Mùi
    (16, 8),   # Thân
    (18, 9),   # Dậu
    (20, 10),  # Tuất
    (22, 11),  # Hợi
    (23, 12),  # Late Tý
])
def test_hour_mapping(hour, expected):
    assert get_iztro_hour(hour) == expected, f"hour={hour}: expected {expected}, got {get_iztro_hour(hour)}"


# ── Lunar Conversion: 33 cases ───────────────────────────────────────────

@pytest.mark.parametrize("solar,expected_lunar,expected_leap", [
    # Category 1: Tết dates
    ((1990, 1, 27),  (1990, 1,  1),  False),
    ((1993, 1, 23),  (1993, 1,  1),  False),
    ((1995, 1, 31),  (1995, 1,  1),  False),
    ((2000, 2,  5),  (2000, 1,  1),  False),
    ((2005, 2,  9),  (2005, 1,  1),  False),
    ((2010, 2, 14),  (2010, 1,  1),  False),
    ((2015, 2, 19),  (2015, 1,  1),  False),
    ((2020, 1, 25),  (2020, 1,  1),  False),
    ((2024, 2, 10),  (2024, 1,  1),  False),
    ((2025, 1, 29),  (2025, 1,  1),  False),
    # Category 2: Boss's test case
    ((1993, 7, 13),  (1993, 5, 24),  False),
    # Category 3: Leap month cases
    ((2020, 5, 25),  (2020, 4,  3),  True),
    ((2020, 6, 15),  (2020, 4, 24),  True),
    ((2001, 6, 10),  (2001, 4, 19),  True),
    ((1995, 9, 25),  (1995, 8,  1),  True),
    ((1985, 4,  1),  (1985, 2, 12),  False),  # lunarcalendar: day=12, not leap
    # Category 4: Month boundary
    ((1993, 7, 18),  (1993, 5, 29),  False),
    ((1993, 7, 19),  (1993, 6,  1),  False),
    ((1990, 3, 26),  (1990, 2, 30),  False),
    ((1990, 3, 27),  (1990, 3,  1),  False),
    ((2025, 1, 28),  (2024, 12, 29), False),
    # Category 5: Common birth dates
    ((1975, 3, 15),  (1975, 2,  3),  False),
    ((1980, 6, 15),  (1980, 5,  3),  False),
    ((1985, 6,  1),  (1985, 4, 13),  False),
    ((1990, 12, 31), (1990, 11, 15), False),
    ((2000, 9, 15),  (2000, 8, 18),  False),  # lunarcalendar: day=18, not 17
    ((2004, 5, 25),  (2004, 4,  7),  False),
    ((2010, 8, 15),  (2010, 7,  6),  False),
    # Category 6: Edge cases
    ((1993, 12, 31), (1993, 11, 19), False),
    ((1990,  1,  1), (1989, 12,  5), False),
    ((1980,  2, 29), (1980,  1, 14), False),
    ((2020,  1, 24), (2019, 12, 30), False),
    ((2025,  1, 31), (2025,  1,  3), False),
])
def test_lunar_conversion(solar, expected_lunar, expected_leap):
    year, month, day = solar
    result = solar_to_lunar_via_library(year, month, day)
    exp_y, exp_m, exp_d = expected_lunar
    assert result["year"]    == exp_y,     f"{solar}: year {result['year']} != {exp_y}"
    assert result["month"]   == exp_m,     f"{solar}: month {result['month']} != {exp_m}"
    assert result["day"]     == exp_d,     f"{solar}: day {result['day']} != {exp_d}"
    assert result["is_leap"] == expected_leap, f"{solar}: is_leap {result['is_leap']} != {expected_leap}"
