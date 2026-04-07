"""Sprint 101 ANA-3: TV invitation message_variant A/B test."""
import sys, os
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects')
sys.path.insert(0, '/home/hungson175/dev/teams/boitoan_mvps/projects/gieo_que/backend')

import pytest
from httpx import AsyncClient, ASGITransport
from tu_vi.main import app


@pytest.mark.asyncio
async def test_invitation_create_returns_message_variant():
    """Invitation create response includes message_variant."""
    body = {
        "initiator_device_id": "test-device",
        "year_a": 1984, "year_b": 1985,
        "context": "romance",
        "hop_tuoi_result": {"combined_score": 65}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/invitation/create", json=body)
    assert r.status_code == 200
    data = r.json()
    assert "message_variant" in data
    assert "message_text" in data


@pytest.mark.asyncio
async def test_invitation_variant_is_one_of_three():
    """message_variant is one of default, curiosity, urgency."""
    allowed = {"default", "curiosity", "urgency"}
    variants_seen = set()
    for _ in range(20):
        body = {
            "initiator_device_id": f"test-device-{_}",
            "year_a": 1984, "year_b": 1985,
            "context": "romance",
            "hop_tuoi_result": {}
        }
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/api/tuvi/invitation/create", json=body)
        assert r.status_code == 200
        variant = r.json()["message_variant"]
        assert variant in allowed, f"Unexpected variant: {variant}"
        variants_seen.add(variant)
    # Should see at least 2 variants in 20 tries (random, so unlikely to only get 1)
    assert len(variants_seen) >= 2, f"Only saw {variants_seen} in 20 tries — random.choice may be broken"


@pytest.mark.asyncio
async def test_invitation_message_text_is_nonempty():
    """message_text is a non-empty string."""
    body = {
        "initiator_device_id": "test-device",
        "year_a": 1984, "year_b": 1985,
        "context": "romance",
        "hop_tuoi_result": {}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/invitation/create", json=body)
    assert r.status_code == 200
    msg = r.json()["message_text"]
    assert isinstance(msg, str)
    assert len(msg) > 10, f"message_text too short: {msg!r}"


@pytest.mark.asyncio
async def test_invitation_message_text_contains_link():
    """message_text contains the invitation deep link."""
    body = {
        "initiator_device_id": "test-device",
        "year_a": 1984, "year_b": 1985,
        "context": "romance",
        "hop_tuoi_result": {}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/api/tuvi/invitation/create", json=body)
    assert r.status_code == 200
    invite_id = r.json()["invitation_id"]
    msg = r.json()["message_text"]
    assert invite_id in msg, f"message_text missing invite_id: {msg}"


@pytest.mark.asyncio
async def test_invitation_get_returns_variant():
    """GET invitation returns stored message_variant."""
    body = {
        "initiator_device_id": "test-device",
        "year_a": 1984, "year_b": 1985,
        "context": "romance",
        "hop_tuoi_result": {}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        create_r = await c.post("/api/tuvi/invitation/create", json=body)
        invite_id = create_r.json()["invitation_id"]
        get_r = await c.get(f"/api/tuvi/invitation/{invite_id}")
    assert get_r.status_code == 200
    data = get_r.json()
    assert "message_variant" in data
    assert data["message_variant"] in {"default", "curiosity", "urgency"}
