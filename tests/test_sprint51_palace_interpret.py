"""Sprint 51 TVI-4 Tests — /api/tuvi/interpret/palace endpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from tu_vi.main import app

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "interpretations")


# ── Palace doc loading ───────────────────────────────────────────────────────

@pytest.mark.parametrize("palace", ["menh", "quan_loc", "phu_the", "tai_bach"])
def test_palace_doc_exists(palace):
    """Each of the 4 palace interpretation docs must exist."""
    path = os.path.join(DOCS_DIR, f"{palace}.md")
    assert os.path.exists(path), f"Missing doc: {path}"


@pytest.mark.parametrize("palace", ["menh", "quan_loc", "phu_the", "tai_bach"])
def test_palace_doc_not_empty(palace):
    """Palace docs must have meaningful content (>= 50 lines)."""
    path = os.path.join(DOCS_DIR, f"{palace}.md")
    if os.path.exists(path):
        with open(path) as f:
            lines = [l for l in f.readlines() if l.strip()]
        assert len(lines) >= 50, f"{palace}.md too short: {len(lines)} non-empty lines"


# ── Endpoint smoke tests (mocked LLM) ────────────────────────────────────────

@pytest.fixture
def mock_stream():
    async def fake_stream(*args, **kwargs):
        from fastapi.responses import StreamingResponse
        async def gen():
            yield "data: ok\n\n".encode()
            yield "data: [DONE]\n\n".encode()
        return StreamingResponse(gen(), media_type="text/event-stream")
    return fake_stream


@pytest.mark.asyncio
async def test_palace_interpret_known_palace(mock_stream):
    """POST /api/tuvi/interpret/palace with known palace returns SSE stream."""
    with patch("tu_vi.main.stream_tuvi_palace_interpretation", new=AsyncMock(side_effect=mock_stream)):
        with patch("tu_vi.main.get_usage", new=AsyncMock(return_value={"remaining": 5, "readings_count": 1, "is_premium": False})):
            with patch("tu_vi.main.increment_usage", new=AsyncMock(return_value={})):
                async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                    resp = await client.post(
                        "/api/tuvi/interpret/palace?device_id=test123",
                        json={"question": "Luận giải cung Mệnh", "birth_info": {}, "chart_data": {}, "palace_name": "menh"}
                    )
                    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_palace_interpret_freemium_blocked():
    """POST /api/tuvi/interpret/palace returns 429 when daily limit reached."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value={"remaining": 0, "readings_count": 3, "is_premium": False})):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/tuvi/interpret/palace?device_id=test123",
                json={"question": "Luận giải cung Mệnh", "birth_info": {}, "chart_data": {}, "palace_name": "menh"}
            )
            assert resp.status_code == 429


@pytest.mark.asyncio
async def test_palace_interpret_unknown_palace(mock_stream):
    """Unknown palace_name falls back gracefully (no doc file — still streams generic)."""
    with patch("tu_vi.main.stream_tuvi_palace_interpretation", new=AsyncMock(side_effect=mock_stream)):
        with patch("tu_vi.main.get_usage", new=AsyncMock(return_value={"remaining": 5, "readings_count": 1, "is_premium": False})):
            with patch("tu_vi.main.increment_usage", new=AsyncMock(return_value={})):
                async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                    resp = await client.post(
                        "/api/tuvi/interpret/palace?device_id=test123",
                        json={"question": "Luận giải cung Huynh Đệ", "birth_info": {}, "chart_data": {}, "palace_name": "huynh_de"}
                    )
                    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_palace_interpret_premium_bypasses_limit(mock_stream):
    """Premium users (is_premium=True) can call regardless of remaining count."""
    with patch("tu_vi.main.stream_tuvi_palace_interpretation", new=AsyncMock(side_effect=mock_stream)):
        with patch("tu_vi.main.get_usage", new=AsyncMock(return_value={"remaining": 0, "readings_count": 3, "is_premium": True})):
            with patch("tu_vi.main.increment_usage", new=AsyncMock(return_value={})):
                async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                    resp = await client.post(
                        "/api/tuvi/interpret/palace?device_id=premium_user",
                        json={"question": "Luận giải cung Mệnh", "birth_info": {}, "chart_data": {}, "palace_name": "menh"}
                    )
                    assert resp.status_code == 200


# ── LLM prompt construction ───────────────────────────────────────────────────

def test_build_palace_prompt_contains_palace_name():
    """Palace prompt must reference the target palace name."""
    from tu_vi.llm_service import build_palace_prompt
    system_p, user_p = build_palace_prompt(
        palace_name="Quan Lộc",
        palace_data={"stars": [{"name": "Tử Vi", "brightness": "Miếu", "tu_hoa": None}],
                     "trang_sinh": "Lâm Quan", "bac_si": "Bác Sĩ",
                     "thai_tue": "Tang Môn", "tuong_tinh": "Tướng Tinh"},
        palace_doc="## Cung Quan Lộc\nThể hiện sự nghiệp.",
        chart_summary={"cung_menh": "Tỵ", "nap_am": {"name": "Hải Trung Kim"}},
    )
    assert "Quan Lộc" in user_p or "Quan Lộc" in system_p
    assert "Tử Vi" in user_p


def test_build_palace_prompt_injects_doc():
    """Palace doc content must appear in the system prompt."""
    from tu_vi.llm_service import build_palace_prompt
    doc_content = "## Cung Mệnh\nDoc content here"
    system_p, user_p = build_palace_prompt(
        palace_name="Mệnh",
        palace_data={"stars": [], "trang_sinh": "", "bac_si": "", "thai_tue": "", "tuong_tinh": ""},
        palace_doc=doc_content,
        chart_summary={"cung_menh": "Tỵ", "nap_am": {"name": "Hải Trung Kim"}},
    )
    assert "Doc content here" in system_p
