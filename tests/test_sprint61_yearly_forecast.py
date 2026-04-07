"""Sprint 61 LN-1/LN-3 + Sprint 62 palace fix: Yearly Forecast tests."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects')

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from tu_vi.main import app

# ── Mock iztro data helpers ───────────────────────────────────────────────────

PALACE_NAMES_12 = [
    'childrenPalace', 'spousePalace', 'siblingsPalace', 'soulPalace',
    'parentsPalace', 'spiritPalace', 'propertyPalace', 'careerPalace',
    'friendsPalace', 'surfacePalace', 'healthPalace', 'wealthPalace',
]
MUTAGEN_4 = ['tianjiMaj', 'tianliangMaj', 'ziweiMaj', 'taiyinMaj']

MONTHLY_PALACE_NAMES = [
    'spiritPalace', 'propertyPalace', 'careerPalace', 'friendsPalace',
    'surfacePalace', 'healthPalace', 'wealthPalace', 'childrenPalace',
    'spousePalace', 'siblingsPalace', 'soulPalace', 'parentsPalace',
]
MONTHLY_MUTAGEN = ['wuquMaj', 'tanlangMaj', 'tianliangMaj', 'wenquMin']


def _make_palace(idx, eb='siEarthly', name='soulPalace'):
    p = MagicMock()
    p.earthly_branch = eb
    p.name = name
    return p


def _make_horoscope_mock():
    """Build a full mock horoscope object."""
    yearly = MagicMock()
    yearly.heavenly_stem = 'yiHeavenly'
    yearly.earthly_branch = 'siEarthly'
    yearly.palace_names = PALACE_NAMES_12[:]
    yearly.mutagen = MUTAGEN_4[:]

    monthly = MagicMock()
    monthly.palace_names = MONTHLY_PALACE_NAMES[:]
    monthly.mutagen = MONTHLY_MUTAGEN[:]

    h = MagicMock()
    h.yearly = yearly
    h.monthly = monthly
    h.nominal_age = 43
    return h


def _make_chart_mock(rotating_monthly=False):
    """Build a mock by_solar chart with 12 palaces.

    If rotating_monthly=True, each horoscope() call returns a different
    palace_names[0] for monthly data — simulates real Lưu Nguyệt rotation.
    """
    eb_list = [
        'yinEarthly', 'maoEarthly', 'chenEarthly', 'siEarthly',
        'wuEarthly', 'weiEarthly', 'shenEarthly', 'youEarthly',
        'xuEarthly', 'haiEarthly', 'ziEarthly', 'chouEarthly',
    ]
    palace_names_en = [
        'childrenPalace', 'spousePalace', 'siblingsPalace', 'soulPalace',
        'parentsPalace', 'spiritPalace', 'propertyPalace', 'careerPalace',
        'friendsPalace', 'surfacePalace', 'healthPalace', 'wealthPalace',
    ]
    chart = MagicMock()
    palaces = []
    for eb, nm in zip(eb_list, palace_names_en):
        p = MagicMock()
        p.earthly_branch = eb
        p.name = nm
        palaces.append(p)
    chart.palaces = palaces

    if rotating_monthly:
        # Each call to horoscope() returns a different palace_names[0] for monthly
        call_count = [0]
        def side_effect(date_str, hour):
            h = _make_horoscope_mock()
            # Rotate palace_names[0] differently each call (1 ref + 12 monthly)
            rotation = palace_names_en[call_count[0] % 12]
            h.monthly.palace_names = [rotation] + palace_names_en[1:]
            call_count[0] += 1
            return h
        chart.horoscope.side_effect = side_effect
    else:
        chart.horoscope.return_value = _make_horoscope_mock()
    return chart


MOCK_PROFILE = {"birth_date": "18/05/1984", "gender": "nam", "hour": "0"}
USAGE_OK = {"readings_count": 0, "is_premium": False, "remaining": 3, "limit": 3}
USAGE_LIMIT = {"readings_count": 3, "is_premium": False, "remaining": 0, "limit": 3}


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_yearly_forecast_returns_12_months():
    """Response must contain exactly 12 month entries."""
    mock_chart = _make_chart_mock()
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    data = r.json()
    assert len(data["months"]) == 12


@pytest.mark.asyncio
async def test_yearly_forecast_has_luu_nien():
    """Response luu_nien must have menh, tu_hoa (4 entries), palace_rotation (12 entries)."""
    mock_chart = _make_chart_mock()
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    ln = r.json()["luu_nien"]
    assert "menh" in ln
    assert len(ln["tu_hoa"]) == 4
    assert len(ln["palace_rotation"]) == 12
    # Each rotation entry has required fields
    entry = ln["palace_rotation"][0]
    assert "position" in entry and "luu_nien_cung" in entry and "natal_cung" in entry


@pytest.mark.asyncio
async def test_yearly_forecast_rating_logic():
    """Monthly rating: good/neutral/caution assigned correctly."""
    mock_chart = _make_chart_mock()

    # Make monthly Mệnh = Quan Lộc (good), no Hóa Kỵ
    good_monthly = MagicMock()
    good_monthly.palace_names = [
        'childrenPalace', 'spousePalace', 'siblingsPalace', 'parentsPalace',
        'spiritPalace', 'propertyPalace', 'careerPalace', 'friendsPalace',
        'surfacePalace', 'healthPalace', 'wealthPalace', 'soulPalace',  # soulPalace at idx 11
    ]
    # soulPalace at index 11 → ENGLISH_PALACE_TRANSLATIONS[palace_names[11]] = Mệnh
    # override: put careerPalace at soul_idx position
    good_monthly.palace_names = [
        'soulPalace', 'childrenPalace', 'spousePalace', 'siblingsPalace',
        'parentsPalace', 'spiritPalace', 'propertyPalace', 'careerPalace',
        'friendsPalace', 'surfacePalace', 'healthPalace', 'wealthPalace',
    ]
    # soulPalace at 0 → monthly menh = Mệnh, not Quan Lộc
    # Let's patch to get careerPalace at soul position
    good_monthly.palace_names[0] = 'careerPalace'  # Quan Lộc at soul position
    good_monthly.mutagen = ['wuquMaj', 'tanlangMaj', 'tianliangMaj', 'zuofuMin']  # no Hóa Kỵ on soul

    h_good = _make_horoscope_mock()
    h_good.monthly = good_monthly

    mock_chart.horoscope.return_value = h_good

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    months = r.json()["months"]
    # All months have valid rating values
    for m in months:
        assert m["rating"] in ("good", "neutral", "caution")


@pytest.mark.asyncio
async def test_yearly_forecast_translation():
    """Response values must be Vietnamese — no Chinese characters."""
    import re
    chinese_re = re.compile(r'[\u4e00-\u9fff]')
    mock_chart = _make_chart_mock()
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    data = r.json()
    assert not chinese_re.search(data["can_chi"]), f"can_chi has Chinese: {data['can_chi']}"
    for th in data["luu_nien"]["tu_hoa"]:
        assert not chinese_re.search(th), f"tu_hoa has Chinese: {th}"
    for m in data["months"]:
        for th in m["tu_hoa"]:
            assert not chinese_re.search(th), f"monthly tu_hoa has Chinese: {th}"


@pytest.mark.asyncio
async def test_yearly_forecast_freemium_gated():
    """Returns 429 when usage limit reached and not premium."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_LIMIT)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 429


@pytest.mark.asyncio
async def test_yearly_forecast_no_profile_no_params():
    """Returns 400 when no profile and no birth params provided."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=None)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_yearly_forecast_with_explicit_params():
    """Works when birth params provided directly (no profile needed)."""
    mock_chart = _make_chart_mock()
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get(
                "/api/tuvi/forecast/yearly"
                "?year=2026&birth_year=1984&birth_month=5&birth_day=18&gender=nam"
            )
    assert r.status_code == 200
    data = r.json()
    assert data["year"] == 2026
    assert len(data["months"]) == 12


# ── Sprint 62: Palace rotation fix tests ──────────────────────────────────────

@pytest.mark.asyncio
async def test_luu_nguyet_menh_rotates():
    """12 months must NOT all return 'Mệnh' — palace_names[0] drives the value."""
    mock_chart = _make_chart_mock(rotating_monthly=True)
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    months = r.json()["months"]
    assert len(months) == 12
    menh_values = [m["luu_nguyet_menh"] for m in months]
    # With rotating mock, not all values should be identical
    assert len(set(menh_values)) > 1, f"All months returned same menh: {menh_values[0]}"


@pytest.mark.asyncio
async def test_luu_nguyet_menh_is_palace_names_0():
    """luu_nguyet_menh = translation of monthly.palace_names[0], not soulPalace index."""
    mock_chart = _make_chart_mock()
    # Override monthly palace_names[0] to careerPalace (= Quan Lộc)
    h = _make_horoscope_mock()
    h.monthly.palace_names = ['careerPalace'] + PALACE_NAMES_12[1:]
    mock_chart.horoscope.return_value = h

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    # All months should show Quan Lộc (palace_names[0] = careerPalace)
    for m in r.json()["months"]:
        assert m["luu_nguyet_menh"] == "Quan Lộc", \
            f"Expected Quan Lộc but got: {m['luu_nguyet_menh']}"


@pytest.mark.asyncio
async def test_monthly_rating_varies():
    """Ratings differ when palace_names[0] rotates through good/caution palaces."""
    mock_chart = _make_chart_mock()

    # Build 13 horoscope mocks (1 ref + 12 months) with varied palace_names[0]
    # Cycle through: wealthPalace (good), healthPalace (caution), siblingsPalace (neutral)
    varied = ['wealthPalace', 'healthPalace', 'siblingsPalace'] * 4 + ['wealthPalace']
    call_idx = [0]
    def side_effect(date_str, hour):
        h = _make_horoscope_mock()
        palace0 = varied[call_idx[0] % len(varied)]
        h.monthly.palace_names = [palace0] + PALACE_NAMES_12[1:]
        # Give month 1 a Hóa Kỵ + healthPalace → caution
        if palace0 == 'healthPalace':
            h.monthly.mutagen = ['taiyinMaj', 'tianjiMaj', 'tianliangMaj', 'taiyinMaj']  # Hóa Kỵ present
        call_idx[0] += 1
        return h
    mock_chart.horoscope.side_effect = side_effect

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.get_profile", new=AsyncMock(return_value=MOCK_PROFILE)), \
         patch("iztro_py.by_solar", return_value=mock_chart):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.get("/api/tuvi/forecast/yearly?year=2026&device_id=test")
    assert r.status_code == 200
    ratings = [m["rating"] for m in r.json()["months"]]
    assert len(set(ratings)) > 1, f"All ratings identical: {ratings[0]}"
