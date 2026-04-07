"""Sprint 98 COMP-1: Hop Tuổi compatibility engine tests."""
import sys, os
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects')
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects/gieo_que/backend')

import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport
from tu_vi.main import app

# ======================================================================
# Unit tests: year_to_zodiac
# ======================================================================

def test_year_to_zodiac_1984():
    """1984 → Tý."""
    from tu_vi.hop_tuoi_service import year_to_zodiac
    chi, name = year_to_zodiac(1984)
    assert chi == "Tý"
    assert name == "Tý"


def test_year_to_zodiac_1990():
    """1990 → Ngọ."""
    from tu_vi.hop_tuoi_service import year_to_zodiac
    chi, name = year_to_zodiac(1990)
    assert chi == "Ngọ"


def test_year_to_zodiac_60_year_cycle():
    """Verify 60-year zodiac cycle correctness."""
    from tu_vi.hop_tuoi_service import year_to_zodiac
    for year, expected in [(1984, "Tý"), (1985, "Sửu"), (1986, "Dần"),
                             (1987, "Mão"), (1988, "Thìn"), (1989, "Tỵ"),
                             (1990, "Ngọ"), (1991, "Mùi"), (1992, "Thân")]:
        chi, _ = year_to_zodiac(year)
        assert chi == expected, f"year={year}: expected {expected}, got {chi}"


# ======================================================================
# Unit tests: year_to_nap_am
# ======================================================================

def test_nap_am_1984():
    """1984 → Hải Trung Kim, Kim."""
    from tu_vi.hop_tuoi_service import year_to_nap_am
    nap = year_to_nap_am(1984)
    assert nap["nap_am"] == "Hải Trung Kim"
    assert nap["element"] == "Kim"


def test_nap_am_1990():
    """1990 → Lộ Bàng Thổ, Thổ."""
    from tu_vi.hop_tuoi_service import year_to_nap_am
    nap = year_to_nap_am(1990)
    assert nap["nap_am"] == "Lộ Bàng Thổ"
    assert nap["element"] == "Thổ"


def test_nap_am_60_years_all_elements():
    """All 60 years in cycle return a valid element."""
    from tu_vi.hop_tuoi_service import year_to_nap_am
    elements = set()
    for offset in range(60):
        year = 1984 + offset
        nap = year_to_nap_am(year)
        assert nap["element"] in ("Kim", "Mộc", "Thủy", "Hoả", "Thổ")
        elements.add(nap["element"])
    assert elements == {"Kim", "Mộc", "Thủy", "Hoả", "Thổ"}


# ======================================================================
# Unit tests: zodiac verdicts
# ======================================================================

def test_tam_hop_ty_thin():
    """Tý + Thìn = tam_hop, score 25."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1984, 1988)  # Tý + Thìn
    assert result["zodiac_verdict"]["type"] == "tam_hop"
    assert result["zodiac_verdict"]["score"] == 25


def test_luc_hop_ty_suu():
    """Tý + Sửu = luc_hop, score 22."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1984, 1985)  # Tý + Sửu
    assert result["zodiac_verdict"]["type"] == "luc_hop"
    assert result["zodiac_verdict"]["score"] == 22


def test_luc_xung_ty_ngo():
    """Tý + Ngọ = luc_xung, score 5."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1984, 1990)  # Tý + Ngọ
    assert result["zodiac_verdict"]["type"] == "luc_xung"
    assert result["zodiac_verdict"]["score"] == 5


def test_luc_hai_ty_mui():
    """Tý + Mùi = luc_hai, score 10."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1984, 1991)  # Tý + Mùi
    assert result["zodiac_verdict"]["type"] == "luc_hai"
    assert result["zodiac_verdict"]["score"] == 10


def test_trung_tinh():
    """Sửu + Dần = trung_tinh, score 15."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1985, 1986)  # Sửu + Dần
    assert result["zodiac_verdict"]["type"] == "trung_tinh"
    assert result["zodiac_verdict"]["score"] == 15


def test_luc_xung_mao_dau():
    """Mão + Dậu = luc_xung, score 5 (TL regression fix)."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    # 1987 = Mão, 1993 = Dậu
    result = score_hop_tuoi(1987, 1993)
    assert result["zodiac_verdict"]["type"] == "luc_xung"
    assert result["zodiac_verdict"]["score"] == 5


def test_luc_xung_thin_tuat():
    """Thìn + Tuất = luc_xung, score 5 (TL regression fix)."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    # 1988 = Thìn, 1994 = Tuất
    result = score_hop_tuoi(1988, 1994)
    assert result["zodiac_verdict"]["type"] == "luc_xung"
    assert result["zodiac_verdict"]["score"] == 5


# ======================================================================
# Unit tests: element verdicts
# ======================================================================

def test_tuong_sinh_score():
    """Tương Sinh element pair → element score 25."""
    # Kim→Thủy (Kim sinh Thủy)
    # 1984: Kim (Hải Trung Kim)
    # 1996: offset 12 = Nham Lạp Thủy, element = Thủy
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1984, 1996)
    assert result["element_verdict"]["type"] == "tuong_sinh"
    assert result["element_verdict"]["score"] == 25


def test_tuong_khac_score():
    """Tương Khắc element pair → element score 5."""
    # Kim (1984) + Mộc (1998) = Kim→Mộc Tương Khắc
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1984, 1998)
    assert result["element_verdict"]["type"] == "tuong_khac"
    assert result["element_verdict"]["score"] == 5


def test_same_element_score():
    """Same element → element score 20."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    # 1984 (Kim) + 1992 (Kim: Kiếm Phong Kim) = same element
    result = score_hop_tuoi(1984, 1992)
    assert result["element_verdict"]["type"] == "cung_ngu_hanh"
    assert result["element_verdict"]["score"] == 20


# ======================================================================
# Unit tests: combined score
# ======================================================================

def test_combined_score_bounds():
    """Combined score always 0-50."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    for a in range(1940, 2020):
        for b in range(1940, 2020):
            r = score_hop_tuoi(a, b)
            assert 0 <= r["combined_score"] <= 50, f"{a}+{b}: {r['combined_score']}"


def test_combined_rating_rat_hop():
    """Tam Hợp + Tương Sinh → Rất Hợp."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    # Same zodiac Tý (cung_tuoi=20) + Tương Sinh(25) = 45 → "Rất Hợp"
    result = score_hop_tuoi(1984, 1996)
    assert result["combined_rating"] == "Rất Hợp"


def test_person_data_fields():
    """Each person has all required fields."""
    from tu_vi.hop_tuoi_service import score_hop_tuoi
    result = score_hop_tuoi(1990, 1992)
    for person in [result["person_a"], result["person_b"]]:
        assert "year" in person
        assert "zodiac" in person
        assert "zodiac_name" in person
        assert "nap_am" in person
        assert "element" in person


# ======================================================================
# API endpoint tests
# ======================================================================

@pytest.mark.asyncio
async def test_hop_tuoi_endpoint_valid():
    """POST /api/tuvi/hop-tuoi → 200 with full response."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/hop-tuoi", json={"year_a": 1990, "year_b": 1992})
    assert r.status_code == 200
    data = r.json()

    assert "person_a" in data
    assert "person_b" in data
    assert "zodiac_verdict" in data
    assert "element_verdict" in data
    assert "combined_score" in data
    assert "combined_rating" in data
    assert "summary" in data


@pytest.mark.asyncio
async def test_hop_tuoi_tam_hop_result():
    """Tý (1984) + Thìn (1988) = tam_hop, high score."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/hop-tuoi", json={"year_a": 1984, "year_b": 1988})
    assert r.status_code == 200
    data = r.json()
    assert data["person_a"]["zodiac"] == "Tý"
    assert data["person_b"]["zodiac"] == "Thìn"
    assert data["zodiac_verdict"]["type"] == "tam_hop"


@pytest.mark.asyncio
async def test_hop_tuoi_invalid_year_low():
    """Year < 1900 → 400."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/hop-tuoi", json={"year_a": 1800, "year_b": 1990})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_hop_tuoi_invalid_year_high():
    """Year > 2025 → 400."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/hop-tuoi", json={"year_a": 2050, "year_b": 1990})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_hop_tuoi_missing_field():
    """Missing required field → 422."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/hop-tuoi", json={"year_a": 1990})  # year_b missing
    assert r.status_code == 422


# ======================================================================
# Invitation endpoint tests
# ======================================================================

@pytest.mark.asyncio
async def test_invitation_create():
    """POST /api/tuvi/invitation/create → 200 with invitation_id + deep_link."""
    body = {
        "initiator_device_id": "test-device",
        "year_a": 1990, "year_b": 1992,
        "context": "romance",
        "hop_tuoi_result": {"combined_score": 40}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/invitation/create", json=body)
    assert r.status_code == 200
    data = r.json()
    assert "invitation_id" in data
    assert "deep_link" in data
    assert len(data["invitation_id"]) == 8


@pytest.mark.asyncio
async def test_invitation_get():
    """GET /api/tuvi/invitation/{id} → 200 with invitation data."""
    body = {
        "initiator_device_id": "test-device",
        "year_a": 1990, "year_b": 1992,
        "context": "romance",
        "hop_tuoi_result": {"combined_score": 40}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        create_r = await c.post("/api/tuvi/invitation/create", json=body)
        invite_id = create_r.json()["invitation_id"]
        r = await c.get(f"/api/tuvi/invitation/{invite_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == invite_id
    assert data["year_a"] == 1990
    assert data["year_b"] == 1992
    assert data["context"] == "romance"


@pytest.mark.asyncio
async def test_invitation_get_not_found():
    """GET /api/tuvi/invitation/{fake_id} → 404."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/api/tuvi/invitation/aaaaaaaa")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_invitation_complete():
    """POST /api/tuvi/invitation/{id}/complete → 200, partner_completed=True."""
    body = {
        "initiator_device_id": "device-a",
        "year_a": 1990, "year_b": 1992,
        "context": "romance",
        "hop_tuoi_result": {}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        create_r = await c.post("/api/tuvi/invitation/create", json=body)
        invite_id = create_r.json()["invitation_id"]
        complete_r = await c.post(
            f"/api/tuvi/invitation/{invite_id}/complete",
            json={"partner_device_id": "device-b"}
        )
    assert complete_r.status_code == 200
    data = complete_r.json()
    assert data["partner_completed"] is True


@pytest.mark.asyncio
async def test_invitation_complete_not_found():
    """POST /api/tuvi/invitation/{fake_id}/complete → 404."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post(
            "/api/tuvi/invitation/aaaaaaaa/complete",
            json={"partner_device_id": "device-b"}
        )
    assert r.status_code == 404
