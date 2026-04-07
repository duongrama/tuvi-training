"""Sprint 98 COMP-4: LLM streaming with context + Hoa Giai (5-section format)."""
import sys, os
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects')
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects/gieo_que/backend')

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from tu_vi.main import app

USAGE_OK = {"readings_count": 0, "is_premium": False, "remaining": 3, "limit": 3}

# Pre-computed hop-tuoi data for stream endpoint
_HOP_TUOI_DATA = {
    "score": 40,
    "rating": "Bình thường",
    "factors": {
        "zodiac": {"type": "trung_tinh", "label": "Trung tính", "score": 15,
                    "detail": "Ngọ-Thân — không thuộc nhóm hợp/xung đặc biệt"},
        "element": {"type": "tuong_sinh", "label": "Tương Sinh", "score": 25,
                    "detail": "Thổ→Kim — Thổ sinh Kim, hai người hỗ trợ nhau."},
    },
    "person_a": {"year": 1990, "name": "A", "zodiac": "Ngọ", "element": "Thổ", "nap_am": "Lộ Bàng Thổ"},
    "person_b": {"year": 1992, "name": "B", "zodiac": "Thân", "element": "Kim", "nap_am": "Kiếm Phong Kim"},
    "device_id": "test_comp4_01",
    "context": "romance",
    "invitation_id": "abc12345",
}


def _build_mock_astream(chunks):
    """Build a mock LLM astream that yields content chunks."""
    async def mock_astream(messages):
        for chunk in chunks:
            m = MagicMock()
            m.content = chunk
            yield m
    return mock_astream


def _build_mock_llm(chunks):
    mock_llm = MagicMock()
    mock_llm.astream = _build_mock_astream(chunks)
    return mock_llm


# ── Test 1: stream includes all 5 sections ──────────────────────────────────────

@pytest.mark.asyncio
async def test_stream_includes_all_five_sections():
    """LLM output must contain all 5 required section headings."""
    narrative = (
        "## 1. Phân Tích Con Giáp\n"
        "Ngọ và Thân có sự khác biệt về tính cách.\n"
        "## 2. Phân Tích Ngũ Hành\n"
        "Thổ sinh Kim — hai người hỗ trợ nhau.\n"
        "## 3. Điểm Mạnh\n"
        "Cả hai đều có ý chí mạnh mẽ.\n"
        "## 4. Điểm Ma Sát\n"
        "Ngọ tính nóng, Thân hay phê phán.\n"
        "## 5. Hòa Giải & Lời Khuyên\n"
        "Nên học cách lắng nghe và điều hoà cảm xúc.\n"
    )

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=_build_mock_llm([narrative])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=_HOP_TUOI_DATA)

    assert r.status_code == 200
    assert "text/event-stream" in r.headers["content-type"]
    text = r.text
    assert "Phân Tích Con Giáp" in text
    assert "Phân Tích Ngũ Hành" in text
    assert "Điểm Mạnh" in text
    assert "Điểm Ma Sát" in text
    assert "Hòa Giải & Lời Khuyên" in text


# ── Test 2: Hoa Giai present for Tương Khắc (conflict) pair ───────────────────

@pytest.mark.asyncio
async def test_hoa_giai_present_for_tuong_khac():
    """Hoa Giai section must appear even for worst Tương Khắc pairs."""
    tuong_khac_data = {
        **_HOP_TUOI_DATA,
        "factors": {
            "zodiac": {"type": "luc_xung", "label": "Lục Xung", "score": 5,
                       "detail": "Tý-Ngọ thuộc cặp Lục Xung"},
            "element": {"type": "tuong_khac", "label": "Tương Khắc", "score": 5,
                       "detail": "Kim→Mộc — Kim khắc Mộc"},
        },
        "person_a": {"year": 1984, "name": "A", "zodiac": "Tý", "element": "Kim"},
        "person_b": {"year": 1998, "name": "B", "zodiac": "Dần", "element": "Mộc"},
        "score": 10,
        "rating": "Xung Đột",
        "device_id": "test_hoagiai_01",
    }

    narrative = (
        "## 1. Phân Tích Con Giáp\n"
        "Tý và Dần có năng lượng đối nghịch nhau.\n"
        "## 2. Phân Tích Ngũ Hành\n"
        "Kim khắc Mộc — xung đột năng lượng.\n"
        "## 3. Điểm Mạnh\n"
        "Cả hai đều quyết đoán và mạnh mẽ.\n"
        "## 4. Điểm Ma Sát\n"
        "Kim và Mộc xung đột gay gắt.\n"
        "## 5. Hòa Giải & Lời Khuyên\n"
        "Hóa giải: tăng cường yếu tố Thổ để dung hòa Kim và Mộc. "
        "Màu sắc gợi ý: vàng, nâu đất. Hướng trung gian: Tây Bắc hoặc Đông Bắc.\n"
    )

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=_build_mock_llm([narrative])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=tuong_khac_data)

    assert r.status_code == 200
    text = r.text
    # Hoa Giai section must be present
    assert "Hòa Giải & Lời Khuyên" in text
    # Element remedy guidance for tuong_khac
    assert ("Thổ" in text) or ("màu" in text.lower()) or ("hóa giải" in text.lower())


# ── Test 3: Hoa Giai present for Tam Hợp (compatible) pair ──────────────────

@pytest.mark.asyncio
async def test_hoa_giai_present_for_tam_hop():
    """Hoa Giai section must appear even for excellent Tam Hợp pairs (strengthening advice)."""
    tam_hop_data = {
        **_HOP_TUOI_DATA,
        "factors": {
            "zodiac": {"type": "tam_hop", "label": "Tam Hợp", "score": 25,
                       "detail": "Tý-Thìn-Thân thuộc nhóm Tam Hợp"},
            "element": {"type": "tuong_sinh", "label": "Tương Sinh", "score": 25,
                       "detail": "Kim→Thủy — Kim sinh Thủy"},
        },
        "person_a": {"year": 1984, "name": "A", "zodiac": "Tý", "element": "Kim"},
        "person_b": {"year": 1996, "name": "B", "zodiac": "Tý", "element": "Thủy"},
        "score": 50,
        "rating": "Rất Hợp",
        "device_id": "test_hoagiai_02",
    }

    narrative = (
        "## 1. Phân Tích Con Giáp\n"
        "Tý và Tý cùng tuổi, có sự đồng điệu.\n"
        "## 2. Phân Tích Ngũ Hành\n"
        "Kim sinh Thủy — tương sinh.\n"
        "## 3. Điểm Mạnh\n"
        "Cả hai rất hòa hợp, cùng chí hướng.\n"
        "## 4. Điểm Ma Sát\n"
        "Cùng tuổi có thể cạnh tranh quyền lực.\n"
        "## 5. Hòa Giải & Lời Khuyên\n"
        "Củng cố: duy trì sự cân bằng, tránh chi phối lẫn nhau.\n"
    )

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=_build_mock_llm([narrative])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=tam_hop_data)

    assert r.status_code == 200
    text = r.text
    assert "Hòa Giải & Lời Khuyên" in text
    # For compatible pairs, Hoa Giai gives strengthening advice
    assert ("củng cố" in text.lower()) or ("tăng cường" in text.lower()) or ("duy trì" in text.lower())


# ── Test 4: context param changes LLM framing (romance vs business) ───────────

@pytest.mark.asyncio
async def test_context_romance_changes_framing():
    """Context=romance → 'tình duyên' framing in system prompt."""
    captured_messages = []

    async def capture_astream(messages):
        captured_messages.extend([m.content for m in messages])
        m = MagicMock()
        m.content = "Phân tích tình duyên."
        yield m

    mock_llm = MagicMock()
    mock_llm.astream = capture_astream

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=mock_llm):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json={**_HOP_TUOI_DATA, "context": "romance"})

    assert r.status_code == 200
    system_prompt = captured_messages[0] if captured_messages else ""
    assert "tình duyên" in system_prompt.lower() or "romance" in system_prompt.lower()


@pytest.mark.asyncio
async def test_context_business_changes_framing():
    """Context=business → 'hợp tác kinh doanh' framing in system prompt."""
    captured_messages = []

    async def capture_astream(messages):
        captured_messages.extend([m.content for m in messages])
        m = MagicMock()
        m.content = "Phân tích kinh doanh."
        yield m

    mock_llm = MagicMock()
    mock_llm.astream = capture_astream

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=mock_llm):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json={**_HOP_TUOI_DATA, "context": "business"})

    assert r.status_code == 200
    system_prompt = captured_messages[0] if captured_messages else ""
    assert "kinh doanh" in system_prompt.lower() or "business" in system_prompt.lower()


@pytest.mark.asyncio
async def test_context_family_changes_framing():
    """Context=family → 'mối quan hệ gia đình' framing."""
    captured_messages = []

    async def capture_astream(messages):
        captured_messages.extend([m.content for m in messages])
        m = MagicMock()
        m.content = "Phân tích gia đình."
        yield m

    mock_llm = MagicMock()
    mock_llm.astream = capture_astream

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=mock_llm):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json={**_HOP_TUOI_DATA, "context": "family"})

    assert r.status_code == 200
    system_prompt = captured_messages[0] if captured_messages else ""
    assert "gia đình" in system_prompt.lower() or "family" in system_prompt.lower()


# ── Test 5: freemium gate still enforced ──────────────────────────────────────

USAGE_LIMIT = {"readings_count": 3, "is_premium": False, "remaining": 0, "limit": 3}


@pytest.mark.asyncio
async def test_stream_respects_freemium_gate():
    """Stream endpoint returns 429 when daily limit reached."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_LIMIT)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=_HOP_TUOI_DATA)
    assert r.status_code == 429


# ── Test 6: first SSE event contains score + factors + context ───────────────

@pytest.mark.asyncio
async def test_stream_first_event_contains_context():
    """First SSE event must include context + invitation_id from request."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm",
               return_value=_build_mock_llm(["Phân tích hoàn tất."])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=_HOP_TUOI_DATA)

    assert r.status_code == 200
    import json
    first_event = r.text.split("data: ")[1].split("\n\n")[0]
    data = json.loads(first_event)
    assert data["context"] == "romance"
    assert data["invitation_id"] == "abc12345"
    assert data["score"] == 40
    assert "factors" in data


# ── Test 7: stream ends with [DONE] marker ────────────────────────────────────

@pytest.mark.asyncio
async def test_stream_ends_with_done_marker():
    """SSE stream must end with 'data: [DONE]'."""
    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm",
               return_value=_build_mock_llm(["Chunk1 ", "Chunk2"])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=_HOP_TUOI_DATA)

    assert r.status_code == 200
    assert "[DONE]" in r.text


# ── Test 8: LLM prompt includes zodiac + element verdict details ────────────────

@pytest.mark.asyncio
async def test_stream_llm_prompt_includes_verdict_details():
    """User prompt must include zodiac verdict detail and element verdict detail."""
    captured_user_prompts = []

    async def capture_astream(messages):
        # Last message is the user prompt
        for m in messages:
            if hasattr(m, "type") and m.type == "human":
                captured_user_prompts.append(m.content)
        m = MagicMock()
        m.content = "Done"
        yield m

    mock_llm = MagicMock()
    mock_llm.astream = capture_astream

    with patch("tu_vi.main.get_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("tu_vi.main.increment_usage", new=AsyncMock(return_value=USAGE_OK)), \
         patch("shared.backend.llm_service.create_llm", return_value=mock_llm):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/compatibility/stream", json=_HOP_TUOI_DATA)

    assert r.status_code == 200
    user_prompt = captured_user_prompts[0] if captured_user_prompts else ""
    # Must include zodiac detail
    assert "Ngọ" in user_prompt or "Thân" in user_prompt
    # Must include element verdict
    assert "Tương Sinh" in user_prompt or "Thổ" in user_prompt
    # Must request 5 sections
    assert "5" in user_prompt or "năm" in user_prompt.lower()
