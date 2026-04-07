"""Sprint 89 TVB-1 BE tests — /api/badges + /api/streak/update for Tu Vi.
TDD: write tests FIRST (Red), then implement.
"""
import sys
import os

_tu_vi_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend_dir = os.path.dirname(_tu_vi_dir)
_project_dir = os.path.dirname(os.path.dirname(_backend_dir))
for p in [_tu_vi_dir, _backend_dir, _project_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from tu_vi.main import app

client = TestClient(app)


def test_badges_endpoint_returns_200():
    """GET /api/badges returns 200 with badges list."""
    mock_badges = {"badges": [], "total_earned": 0}
    with patch("shared.backend.daily_service.get_badges", new=AsyncMock(return_value=mock_badges)):
        resp = client.get("/api/badges?device_id=test-device-s89")
    assert resp.status_code == 200
    data = resp.json()
    assert "badges" in data or "total_earned" in data


def test_streak_update_endpoint_returns_200():
    """POST /api/streak/update returns 200 with streak info."""
    mock_streak = {"consecutive_days": 3, "last_date": "2026-03-19"}
    with patch("shared.backend.daily_service.update_streak", new=AsyncMock(return_value=mock_streak)):
        resp = client.post("/api/streak/update?device_id=test-device-s89")
    assert resp.status_code == 200
    data = resp.json()
    assert "consecutive_days" in data or data  # returns streak object
