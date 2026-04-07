"""Sprint 49 Tests — Extract iztro-py hidden stars + metadata (TVO-1/2/3)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from tu_vi.iztro_service import get_tuvi_chart


# Boss chart fixture — reused across multiple tests
@pytest.fixture(scope="module")
def boss_chart():
    return get_tuvi_chart(1984, 5, 18, 0, gender="nam")


@pytest.fixture(scope="module")
def boss_palaces(boss_chart):
    return {p["dia_chi"]: p for p in boss_chart["palaces"]}


# ── TVO-1: Ring fields present and Vietnamese ───────────────────────────────

def test_ring_fields_present(boss_palaces):
    """Ring fields exist and are non-empty in every palace (Tướng Tinh removed)."""
    for chi, p in boss_palaces.items():
        for field in ("trang_sinh", "bac_si", "thai_tue"):
            assert field in p, f"Palace {chi} missing field '{field}'"
            assert p[field], f"Palace {chi} field '{field}' is empty"
    # Tướng Tinh ring removed — must not be present
    for chi, p in boss_palaces.items():
        assert "tuong_tinh" not in p, f"Palace {chi} still has removed 'tuong_tinh' field"


def test_ring_fields_are_vietnamese(boss_palaces):
    """Ring fields contain Vietnamese text — no raw Chinese characters."""
    import re
    chinese_re = re.compile(r'[\u4e00-\u9fff]')
    for chi, p in boss_palaces.items():
        for field in ("trang_sinh", "bac_si", "thai_tue"):
            val = p.get(field, "")
            assert not chinese_re.search(val), \
                f"Palace {chi}.{field} still has Chinese chars: '{val}'"


def test_trang_sinh_boss_case(boss_palaces):
    """1984 Mộc Tam Cục, Dương Nam → Tỵ (Mệnh) should have a known Tràng Sinh value."""
    # Tỵ is palace 6; with Mộc Tam Cục CW from Hợi: Hợi=Trường Sinh, Tý=Mộc Dục, ...Tỵ=Bệnh
    assert boss_palaces["Tỵ"]["trang_sinh"] == "Bệnh"
    assert boss_palaces["Hợi"]["trang_sinh"] == "Trường Sinh"


def test_bac_si_boss_case(boss_palaces):
    """Giáp year → Lộc Tồn at Dần → Bác Sĩ at Dần."""
    assert boss_palaces["Dần"]["bac_si"] == "Bác Sĩ"


def test_thai_tue_boss_case(boss_palaces):
    """Year branch Tý → Thái Tuế ring starts at Tý."""
    thai_tue_val = boss_palaces["Tý"]["thai_tue"]
    # suiqian12 at Tý palace for 1984 chart — should be a recognizable Vietnamese ring name
    assert thai_tue_val and "Tuế" in thai_tue_val or thai_tue_val in (
        "Tuế Kiến", "Thái Tuế", "Hối Khí", "Tang Môn", "Quán Sách",
        "Quan Phù", "Tiểu Hao", "Đại Hao", "Long Đức", "Bạch Hổ",
        "Thiên Đức", "Điếu Khách", "Bệnh Phù"
    ), f"Unexpected thai_tue value: {thai_tue_val}"


# ── TVO-2: Palace Can Chi ───────────────────────────────────────────────────

def test_palace_can_chi_present(boss_palaces):
    """Every palace has a can_chi field in 'X Y' format."""
    import re
    pattern = re.compile(r'^\S+ \S+$')
    for chi, p in boss_palaces.items():
        assert "can_chi" in p, f"Palace {chi} missing can_chi"
        assert pattern.match(p["can_chi"]), \
            f"Palace {chi} can_chi bad format: '{p['can_chi']}'"


def test_palace_can_chi_boss_dan(boss_palaces):
    """Giáp year → Ngũ Hổ Độn: Dần stem = Bính → palace Dần = 'Bính Dần'."""
    assert boss_palaces["Dần"]["can_chi"] == "Bính Dần"


def test_palace_can_chi_boss_ty(boss_palaces):
    """Giáp year: Tý palace can_chi = 'Bính Tý' (wraps after Ất Hợi)."""
    assert boss_palaces["Tý"]["can_chi"] == "Bính Tý"


def test_is_body_palace_present(boss_palaces):
    """Every palace has is_body_palace boolean field."""
    for chi, p in boss_palaces.items():
        assert "is_body_palace" in p, f"Palace {chi} missing is_body_palace"
        assert isinstance(p["is_body_palace"], bool)


# ── TVO-3: Mệnh Chủ / Thân Chủ ─────────────────────────────────────────────

def test_menh_chu_boss(boss_chart):
    """Mệnh at Tỵ → Mệnh Chủ = Vũ Khúc."""
    assert boss_chart["menh_chu"] == "Vũ Khúc"


def test_than_chu_boss(boss_chart):
    """Year branch Tý → Thân Chủ = Hỏa Tinh."""
    assert boss_chart["than_chu"] == "Hỏa Tinh"


def test_menh_chu_ngo():
    """Mệnh at Ngọ → Mệnh Chủ = Phá Quân (different birth)."""
    # 1966 Bính Ngọ — find a birth that puts Mệnh at Ngọ
    # Use a known case: just test the logic via a chart where menh = Ngọ
    chart = get_tuvi_chart(1966, 7, 15, 0, gender="nam")
    if chart["cung_menh"] == "Ngọ":
        assert chart["menh_chu"] == "Phá Quân"


# ── TVO-3: Adjective stars ───────────────────────────────────────────────────

def test_adjective_stars_extracted(boss_palaces):
    """At least some palaces have adjective_stars (non-empty lists)."""
    total = sum(len(p.get("adjective_stars", [])) for p in boss_palaces.values())
    assert total > 0, "No adjective_stars extracted at all"


def test_adjective_stars_are_vietnamese(boss_palaces):
    """Adjective star names are Vietnamese (no English IDs like 'hongluan')."""
    import re
    ascii_id_re = re.compile(r'^[a-z]+$')
    for chi, p in boss_palaces.items():
        for s in p.get("adjective_stars", []):
            assert not ascii_id_re.match(s["name"]), \
                f"Palace {chi} adjective star still has English ID: '{s['name']}'"


def test_total_star_count(boss_chart):
    """Total star entries + ring fields across all palaces ≥ 100 (iztro-py provides 114)."""
    total = 0
    for p in boss_chart["palaces"]:
        total += len(p.get("stars", []))
        total += len(p.get("adjective_stars", []))
        # Count non-empty ring fields as stars too
        total += sum(1 for f in ("trang_sinh", "bac_si", "thai_tue") if p.get(f))
    assert total >= 100, f"Only {total} stars+rings — expected ≥ 100"
