"""Sprint 48 Tests — Đại Hạn direction (4 cases) + Nạp Âm lookup (5 cases)."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from tu_vi.iztro_service import get_nap_am, get_tuvi_chart


# ── Nạp Âm Lookup: 5 cases ──────────────────────────────────────────────

@pytest.mark.parametrize("birth_year,expected", [
    (1984, "Hải Trung Kim"),   # Giáp Tý
    (1985, "Hải Trung Kim"),   # Ất Sửu
    (1990, "Lộ Bàng Thổ"),    # Canh Ngọ
    (1993, "Kiếm Phong Kim"),  # Quý Dậu
    (2000, "Bạch Lạp Kim"),    # Canh Thìn
])
def test_nap_am_lookup(birth_year, expected):
    result = get_nap_am(birth_year)
    assert result == expected, f"year {birth_year}: expected '{expected}', got '{result}'"


# ── Đại Hạn Direction: 4 cases via full chart ────────────────────────────

def test_daihan_duong_nam_thuan():
    """1984 Nam (Giáp=Dương) → Thuận (CW): Tỵ(3-12)→Ngọ(13-22)→Mùi(23-32)."""
    chart = get_tuvi_chart(1984, 5, 18, 0, gender="nam")
    dai_han = sorted(chart["dai_han"], key=lambda x: x["start_age"])
    assert len(dai_han) >= 3
    # First three should be clockwise from Tỵ
    first = dai_han[0]
    assert first["start_age"] == 3
    assert first["end_age"] == 12
    # Palace sequence must be ascending positions (clockwise = increasing position)
    positions = [d["palace_index"] for d in dai_han[:3]]
    # Clockwise means consecutive positions (wrapping 12→1)
    pos0, pos1, pos2 = positions
    assert (pos1 - pos0) % 12 == 1 or (pos1 == 1 and pos0 == 12), \
        f"Thuận expected consecutive positions, got {positions}"


def test_daihan_am_nam_nghich():
    """1985 Nam (Ất=Âm) → Nghịch (CCW): positions decrease."""
    chart = get_tuvi_chart(1985, 5, 18, 0, gender="nam")
    dai_han = sorted(chart["dai_han"], key=lambda x: x["start_age"])
    assert len(dai_han) >= 3
    positions = [d["palace_index"] for d in dai_han[:3]]
    pos0, pos1 = positions[0], positions[1]
    # Counterclockwise means decreasing position (wrapping 1→12)
    assert (pos0 - pos1) % 12 == 1 or (pos0 == 1 and pos1 == 12), \
        f"Nghịch expected decreasing positions, got {positions}"


def test_daihan_duong_nu_nghich():
    """1984 Nữ (Giáp=Dương) → Nghịch (CCW)."""
    chart = get_tuvi_chart(1984, 5, 18, 0, gender="nữ")
    dai_han = sorted(chart["dai_han"], key=lambda x: x["start_age"])
    assert len(dai_han) >= 3
    positions = [d["palace_index"] for d in dai_han[:3]]
    pos0, pos1 = positions[0], positions[1]
    assert (pos0 - pos1) % 12 == 1 or (pos0 == 1 and pos1 == 12), \
        f"Nghịch expected decreasing positions, got {positions}"


def test_daihan_am_nu_thuan():
    """1985 Nữ (Ất=Âm) → Thuận (CW)."""
    chart = get_tuvi_chart(1985, 5, 18, 0, gender="nữ")
    dai_han = sorted(chart["dai_han"], key=lambda x: x["start_age"])
    assert len(dai_han) >= 3
    positions = [d["palace_index"] for d in dai_han[:3]]
    pos0, pos1 = positions[0], positions[1]
    assert (pos1 - pos0) % 12 == 1 or (pos1 == 1 and pos0 == 12), \
        f"Thuận expected consecutive positions, got {positions}"


def test_boss_case_1984_full_sequence():
    """Boss test: 18/5/1984 Nam → Tỵ(3-12)→Ngọ(13-22)→Mùi(23-32)."""
    chart = get_tuvi_chart(1984, 5, 18, 0, gender="nam")
    dai_han = sorted(chart["dai_han"], key=lambda x: x["start_age"])

    assert dai_han[0]["start_age"] == 3  and dai_han[0]["end_age"] == 12
    assert dai_han[1]["start_age"] == 13 and dai_han[1]["end_age"] == 22
    assert dai_han[2]["start_age"] == 23 and dai_han[2]["end_age"] == 32

    # Nạp Âm must be Hải Trung Kim (not Cục name)
    assert chart["nap_am"]["name"] == "Hải Trung Kim"
    # Cục stays separate and correct
    assert "cuc" in chart


def test_nap_am_not_cuc_name():
    """nap_am field must NOT contain Cục name like 'Mộc Tam Cục'."""
    chart = get_tuvi_chart(1984, 5, 18, 0, gender="nam")
    nap_am_name = chart["nap_am"]["name"]
    assert "Cục" not in nap_am_name, f"nap_am should not be Cục name, got: {nap_am_name}"


def test_english_gender_male_direction():
    """gender='male' (English) must be treated as Nam → Quý Dậu (Âm) Nam → Nghịch (CCW)."""
    chart = get_tuvi_chart(1993, 7, 13, 6, gender="male")
    dai_han = sorted(chart["dai_han"], key=lambda x: x["start_age"])
    assert len(dai_han) >= 3
    positions = [d["palace_index"] for d in dai_han[:3]]
    pos0, pos1 = positions[0], positions[1]
    # 1993 = Quý Dậu (Âm year), Nam → Nghịch (CCW): positions decrease
    assert (pos0 - pos1) % 12 == 1 or (pos0 == 1 and pos1 == 12), \
        f"gender='male' should map to Nam → Nghịch, got positions {positions}"


def test_nap_am_uses_lunar_year():
    """1980-01-15 solar = lunar year 1979 (Kỷ Mùi) → Nạp Âm 'Thiên Thượng Hỏa', not 'Thạch Lựu Mộc' (1980)."""
    chart = get_tuvi_chart(1980, 1, 15, 0, gender="nam")
    assert chart["nap_am"]["name"] == "Thiên Thượng Hỏa", \
        f"Expected 'Thiên Thượng Hỏa' (lunar 1979), got '{chart['nap_am']['name']}'"
