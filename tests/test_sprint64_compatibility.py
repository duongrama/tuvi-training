"""Sprint 64 CMP-1/CMP-3: Tu Vi Compatibility endpoint tests."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects')

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from tu_vi.main import app

# ── Mock data ─────────────────────────────────────────────────────────────────

USAGE_OK   = {"readings_count": 0, "is_premium": False, "remaining": 3, "limit": 3}
USAGE_LIMIT = {"readings_count": 3, "is_premium": False, "remaining": 0, "limit": 3}


def _make_palace_mock(name, major_star_names, earthly_branch="ziEarthly"):
    p = MagicMock()
    p.name = name
    p.earthly_branch = earthly_branch
    stars = []
    for sn in major_star_names:
        s = MagicMock()
        s.name = sn
        s.brightness = "旺"
        stars.append(s)
    p.major_stars = stars
    p.minor_stars = []
    p.adjective_stars = []
    p.changsheng12 = ""
    p.boshi12 = ""
    p.jiangqian12 = ""
    p.suiqian12 = ""
    return p


def _make_chart_mock(five_elements="金四局", zodiac="鸡", soul_branch="ziEarthly",
                     spouse_stars=None, spouse_branch="xuEarthly"):
    """Build a minimal iztro-py chart mock."""
    spouse_stars = spouse_stars or ["taiyinMaj"]
    chart = MagicMock()
    chart.five_elements_class = five_elements
    chart.zodiac = zodiac
    chart.earthly_branch_of_soul_palace = soul_branch
    chart.earthly_branch_of_body_palace = soul_branch
    chart.chinese_date = "癸酉 六月 十三 午"
    chart.time = "午"

    palaces = []
    for pname, ebranch in [
        ("soulPalace", soul_branch), ("parentsPalace", "chouEarthly"),
        ("spiritPalace", "yinEarthly"), ("propertyPalace", "maoEarthly"),
        ("careerPalace", "chenEarthly"), ("friendsPalace", "siEarthly"),
        ("surfacePalace", "wuEarthly"), ("healthPalace", "weiEarthly"),
        ("wealthPalace", "shenEarthly"), ("childrenPalace", "youEarthly"),
        ("spousePalace", spouse_branch), ("siblingsPalace", "haiEarthly"),
    ]:
        stars = spouse_stars if pname == "spousePalace" else ["tianjiMaj"]
        palaces.append(_make_palace_mock(pname, stars, ebranch))
    chart.palaces = palaces
    return chart


CHART_A = _make_chart_mock(
    five_elements="金四局", zodiac="鸡",
    soul_branch="ziEarthly", spouse_stars=["tianfuMaj"], spouse_branch="xuEarthly"
)
CHART_B = _make_chart_mock(
    five_elements="水二局", zodiac="猪",
    soul_branch="shenEarthly", spouse_stars=["tanlangMaj"], spouse_branch="chouEarthly"
)


# ── Endpoint tests ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_compatibility_returns_score_and_factors():
    """Response must have score, rating, factors (4 keys), person_a, person_b."""
    call_count = [0]
    def by_solar_side(date_str, hour, gender):
        c = CHART_A if call_count[0] == 0 else CHART_B
        call_count[0] += 1
        return c

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("iztro_py.by_solar", side_effect=by_solar_side), \
         patch("tu_vi.main.invoke_llm", return_value="Hai người rất hợp nhau."):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility", json={
                "person_a": {"name": "Anh", "year": 1993, "month": 6, "day": 13, "hour": 10, "gender": "nam"},
                "person_b": {"name": "Em", "year": 1995, "month": 3, "day": 22, "hour": 14, "gender": "nu"},
                "device_id": "test_compat_01"
            })
    assert r.status_code == 200
    data = r.json()
    assert "score" in data
    assert "rating" in data
    assert "factors" in data
    assert "person_a" in data
    assert "person_b" in data
    factors = data["factors"]
    assert "ngu_hanh" in factors
    assert "zodiac" in factors
    assert "phu_the" in factors
    assert "menh_harmony" in factors


@pytest.mark.asyncio
async def test_compatibility_score_is_sum_of_factors():
    """Total score = sum of 4 factor scores."""
    call_count = [0]
    def by_solar_side(date_str, hour, gender):
        c = CHART_A if call_count[0] == 0 else CHART_B
        call_count[0] += 1
        return c

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("iztro_py.by_solar", side_effect=by_solar_side), \
         patch("tu_vi.main.invoke_llm", return_value="Phân tích..."):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility", json={
                "person_a": {"name": "A", "year": 1993, "month": 6, "day": 13, "hour": 10, "gender": "nam"},
                "person_b": {"name": "B", "year": 1995, "month": 3, "day": 22, "hour": 14, "gender": "nu"},
                "device_id": "test_compat_02"
            })
    data = r.json()
    factors = data["factors"]
    expected_total = (factors["ngu_hanh"]["score"] + factors["zodiac"]["score"] +
                      factors["phu_the"]["score"] + factors["menh_harmony"]["score"])
    assert data["score"] == expected_total


@pytest.mark.asyncio
async def test_compatibility_freemium_gated():
    """Returns 429 when daily limit reached."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_LIMIT)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility", json={
                "person_a": {"name": "A", "year": 1990, "month": 1, "day": 1, "hour": 0, "gender": "nam"},
                "person_b": {"name": "B", "year": 1992, "month": 2, "day": 2, "hour": 0, "gender": "nu"},
                "device_id": "test_compat_limit"
            })
    assert r.status_code == 429


@pytest.mark.asyncio
async def test_compatibility_analysis_in_response():
    """Response must contain 'analysis' field with LLM text."""
    call_count = [0]
    def by_solar_side(date_str, hour, gender):
        c = CHART_A if call_count[0] == 0 else CHART_B
        call_count[0] += 1
        return c

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("iztro_py.by_solar", side_effect=by_solar_side), \
         patch("tu_vi.main.invoke_llm", return_value="Mocked LLM text"):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility", json={
                "person_a": {"name": "Anh", "year": 1993, "month": 6, "day": 13, "hour": 10, "gender": "nam"},
                "person_b": {"name": "Em", "year": 1995, "month": 3, "day": 22, "hour": 14, "gender": "nu"},
                "device_id": "test_compat_03"
            })
    assert r.status_code == 200
    assert "analysis" in r.json()


# ── Scoring unit tests ─────────────────────────────────────────────────────────

def test_ngu_hanh_tuong_sinh_scores_25():
    """Kim generates Thủy → Tương Sinh → 25pts."""
    from tu_vi.compatibility_service import score_ngu_hanh
    score, detail = score_ngu_hanh("Kim", "Thủy")
    assert score == 25
    assert "Tương Sinh" in detail


def test_ngu_hanh_tuong_khac_scores_5():
    """Kim destroys Mộc → Tương Khắc → 5pts."""
    from tu_vi.compatibility_service import score_ngu_hanh
    score, detail = score_ngu_hanh("Kim", "Mộc")
    assert score == 5
    assert "Tương Khắc" in detail


def test_ngu_hanh_same_element_scores_20():
    """Same element → 20pts."""
    from tu_vi.compatibility_service import score_ngu_hanh
    score, detail = score_ngu_hanh("Hỏa", "Hỏa")
    assert score == 20


def test_zodiac_tam_hop_scores_25():
    """Thân-Tý-Thìn are Tam Hợp triad — any two → 25pts."""
    from tu_vi.compatibility_service import score_zodiac_compat
    score, detail = score_zodiac_compat("Thân", "Tý")
    assert score == 25
    assert "Tam Hợp" in detail


def test_zodiac_luc_xung_scores_5():
    """Tý-Ngọ clash → 5pts."""
    from tu_vi.compatibility_service import score_zodiac_compat
    score, detail = score_zodiac_compat("Tý", "Ngọ")
    assert score == 5
    assert "Lục Xung" in detail


def test_zodiac_luc_hop_scores_22():
    """Tý-Sửu Lục Hợp → 22pts."""
    from tu_vi.compatibility_service import score_zodiac_compat
    score, detail = score_zodiac_compat("Tý", "Sửu")
    assert score == 22
    assert "Lục Hợp" in detail


def test_rating_thresholds():
    """Rating labels match spec thresholds."""
    from tu_vi.compatibility_service import get_rating
    assert get_rating(85) == "Rất hợp"
    assert get_rating(70) == "Khá hợp"
    assert get_rating(50) == "Bình thường"
    assert get_rating(30) == "Cần cân nhắc"
    assert get_rating(10) == "Nhiều thử thách"


_PRECOMPUTED = {
    "score": 72,
    "rating": "Khá hợp",
    "factors": {
        "ngu_hanh":     {"score": 25, "detail": "Kim→Thủy — Tương Sinh"},
        "zodiac":       {"score": 22, "detail": "Dậu-Hợi — Lục Hợp"},
        "phu_the":      {"score": 15, "detail": "A: Thái Âm (15đ), B: Tham Lang (15đ)"},
        "menh_harmony": {"score": 10, "detail": "Tý-Thân — Trung tính"},
    },
    "person_a": {"name": "Anh", "menh": "Tý", "cuc": "Kim Tứ Cục", "zodiac": "Dậu", "element": "Kim"},
    "person_b": {"name": "Em",  "menh": "Thân", "cuc": "Thủy Nhị Cục", "zodiac": "Hợi", "element": "Thủy"},
    "device_id": "test_stream_01",
}


@pytest.mark.asyncio
async def test_compatibility_stream_returns_sse():
    """Stream endpoint accepts pre-computed result; returns 200 SSE with score event first."""
    async def mock_astream(messages):
        for chunk in ["Hai bạn ", "rất hợp ", "nhau."]:
            m = MagicMock()
            m.content = chunk
            yield m

    mock_llm = MagicMock()
    mock_llm.astream = mock_astream

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=mock_llm):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=_PRECOMPUTED)
    assert r.status_code == 200
    assert "text/event-stream" in r.headers["content-type"]
    # First SSE event must contain score and factors
    import json
    first_event = r.text.split("data: ")[1].split("\n\n")[0]
    data = json.loads(first_event)
    assert "score" in data
    assert "factors" in data
    assert "rating" in data
    # No iztro_py.by_solar should have been called
    assert data["score"] == 72


def test_phu_the_detail_vietnamese():
    """score_phu_the() detail must use Vietnamese star names, not English IDs."""
    from tu_vi.compatibility_service import score_phu_the
    score, detail = score_phu_the(["taiyinMaj"], ["tanlangMaj"])
    # Must NOT contain raw English IDs
    assert "taiyinMaj" not in detail
    assert "tanlangMaj" not in detail
    # Must contain Vietnamese names
    assert "Thái Âm" in detail or "Tham Lang" in detail
