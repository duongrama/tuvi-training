"""Tests for Tu Vi Feature Parity: TV-FP-1 (daily), TV-FP-2 (share), TV-FP-3 (push)."""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import sys
import os

# Fix PYTHONPATH
_tu_vi_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend_dir = os.path.dirname(_tu_vi_dir)
_project_dir = os.path.dirname(os.path.dirname(_backend_dir))
for p in [_tu_vi_dir, _backend_dir, _project_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi.testclient import TestClient
from tu_vi.main import app

client = TestClient(app)


# ── TV-FP-1: Daily Fortune ──────────────────────────────────────────────

class TestDailyFortune:

    def test_daily_endpoint_exists(self):
        with patch("tu_vi.main.get_profile", new_callable=AsyncMock) as mock_profile, \
             patch("tu_vi.main.get_cached_tuvi_daily", return_value=None), \
             patch("tu_vi.main.cache_tuvi_daily"), \
             patch("tu_vi.main.get_streak", new_callable=AsyncMock) as mock_streak, \
             patch("tu_vi.main.update_streak", new_callable=AsyncMock) as mock_update:
            mock_profile.return_value = None
            mock_streak.return_value = {"streak_count": 0, "consecutive_days": 0}
            mock_update.return_value = {"streak_count": 1, "consecutive_days": 1}
            response = client.get("/api/tuvi/daily?device_id=test")
            assert response.status_code == 200

    def test_daily_returns_no_profile_when_missing(self):
        with patch("tu_vi.main.get_profile", new_callable=AsyncMock) as mock_profile:
            mock_profile.return_value = None
            response = client.get("/api/tuvi/daily?device_id=no_profile_user")
            assert response.status_code == 200
            data = response.json()
            assert data.get("error") == "no_profile"

    def test_daily_returns_fortune_text_with_birth_date_string(self):
        """profile_service stores birth_date as 'dd/mm/yyyy' string — must parse correctly."""
        profile = {"birth_date": "15/05/1990", "gender": "nam", "name": "Test User"}
        chart_mock = {
            "menh": "Ngọ", "than": "Mão",
            "tieu_han": {"palace_name": "Mệnh", "stars": ["Tử Vi"]},
            "dai_han": []
        }
        with patch("tu_vi.main.get_profile", new_callable=AsyncMock) as mock_profile, \
             patch("tu_vi.main.get_cached_tuvi_daily", return_value=None), \
             patch("tu_vi.main.cache_tuvi_daily"), \
             patch("tu_vi.main.calculate_tuvi_chart", return_value=chart_mock), \
             patch("tu_vi.main.invoke_llm", return_value="Hôm nay tốt."), \
             patch("tu_vi.main.get_streak", new_callable=AsyncMock) as mock_streak, \
             patch("tu_vi.main.update_streak", new_callable=AsyncMock) as mock_update:
            mock_profile.return_value = profile
            mock_streak.return_value = {"streak_count": 1, "consecutive_days": 1}
            mock_update.return_value = {"streak_count": 2, "consecutive_days": 2}
            response = client.get("/api/tuvi/daily?device_id=test_birth_date")
            assert response.status_code == 200
            data = response.json()
            assert "fortune_text" in data
            assert data.get("error") is None

    def test_daily_returns_fortune_text_when_profile_exists(self):
        profile = {
            "year": 1990, "month": 5, "day": 15,
            "hour": 8, "gender": "nam", "name": "Test User"
        }
        chart_mock = {
            "menh": "Ngọ", "than": "Mão",
            "tieu_han": {"palace_name": "Mệnh", "stars": ["Tử Vi", "Thiên Phủ"]},
            "dai_han": [{"age_start": 20, "age_end": 30, "palace_name": "Quan Lộc"}]
        }
        with patch("tu_vi.main.get_profile", new_callable=AsyncMock) as mock_profile, \
             patch("tu_vi.main.get_cached_tuvi_daily", return_value=None), \
             patch("tu_vi.main.cache_tuvi_daily"), \
             patch("tu_vi.main.calculate_tuvi_chart", return_value=chart_mock), \
             patch("tu_vi.main.invoke_llm", return_value="Hôm nay vận hạn tốt."), \
             patch("tu_vi.main.get_streak", new_callable=AsyncMock) as mock_streak, \
             patch("tu_vi.main.update_streak", new_callable=AsyncMock) as mock_update:
            mock_profile.return_value = profile
            mock_streak.return_value = {"streak_count": 3, "consecutive_days": 3}
            mock_update.return_value = {"streak_count": 4, "consecutive_days": 4}
            response = client.get("/api/tuvi/daily?device_id=test123")
            assert response.status_code == 200
            data = response.json()
            assert "fortune_text" in data
            assert "date" in data
            assert "streak_count" in data

    def test_daily_uses_cache_when_available(self):
        cached = {
            "fortune_text": "Cached fortune", "date": "2026-03-15",
            "palace_name": "Mệnh", "key_star": "Tử Vi", "streak_count": 2
        }
        profile = {"year": 1990, "month": 5, "day": 15, "hour": 8, "gender": "nam"}
        with patch("tu_vi.main.get_profile", new_callable=AsyncMock) as mock_profile, \
             patch("tu_vi.main.get_cached_tuvi_daily", return_value=cached), \
             patch("tu_vi.main.get_streak", new_callable=AsyncMock) as mock_streak:
            mock_profile.return_value = profile
            mock_streak.return_value = {"streak_count": 2, "consecutive_days": 2}
            response = client.get("/api/tuvi/daily?device_id=cached_user")
            assert response.status_code == 200
            data = response.json()
            assert data["fortune_text"] == "Cached fortune"

    def test_daily_cache_key_includes_device_id(self):
        """Verify personalized cache key per device_id (not shared across users)."""
        from tu_vi.main import make_tuvi_daily_cache_key
        key1 = make_tuvi_daily_cache_key("user_a", "2026-03-15")
        key2 = make_tuvi_daily_cache_key("user_b", "2026-03-15")
        assert key1 != key2
        assert "user_a" in key1
        assert "tuvi" in key1

    def test_daily_streak_endpoint(self):
        with patch("tu_vi.main.get_streak", new_callable=AsyncMock) as mock_streak:
            mock_streak.return_value = {"streak_count": 5, "consecutive_days": 5}
            response = client.get("/api/tuvi/streak?device_id=test")
            assert response.status_code == 200
            data = response.json()
            assert "streak_count" in data


# ── TV-FP-2: Share as Image ─────────────────────────────────────────────

class TestShareImage:

    def test_share_endpoint_exists(self):
        with patch("tu_vi.main.generate_share_from_reading", return_value={
            "story": "/shared/shares/test_story.png",
            "card": "/shared/shares/test_card.png",
            "hash": "abc123",
            "share_page": "/shared/shares/test.html"
        }):
            payload = {
                "menh": "Ngọ", "than": "Mão",
                "birth_info": {"name": "Test", "year": 1990},
                "tieu_han": {"palace_name": "Mệnh"},
                "dai_han": []
            }
            response = client.post("/api/tuvi/share", json=payload)
            assert response.status_code == 200

    def test_share_returns_image_urls(self):
        with patch("tu_vi.main.generate_share_from_reading", return_value={
            "story": "/shared/shares/img_story.png",
            "card": "/shared/shares/img_card.png",
            "hash": "def456",
            "share_page": "/shared/shares/page.html"
        }):
            payload = {"menh": "Ngọ", "birth_info": {}}
            response = client.post("/api/tuvi/share", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "story" in data
            assert "card" in data
            assert "share_page" in data

    def test_share_passes_tuvi_app_name(self):
        """generate_share_from_reading must be called with app_name='tuvi'."""
        with patch("tu_vi.main.generate_share_from_reading") as mock_share:
            mock_share.return_value = {"story": "", "card": "", "hash": "", "share_page": ""}
            payload = {"menh": "Ngọ", "birth_info": {}}
            client.post("/api/tuvi/share", json=payload)
            mock_share.assert_called_once()
            call_args = mock_share.call_args
            assert call_args[0][1] == "tuvi" or call_args[1].get("app_name") == "tuvi"


# ── TV-FP-3: Push Notifications ─────────────────────────────────────────

class TestPushNotifications:

    def test_push_subscribe_endpoint_exists(self):
        with patch("tu_vi.main.push_subscribe", new_callable=AsyncMock) as mock_sub:
            mock_sub.return_value = {"success": True}
            response = client.post(
                "/api/push/subscribe?device_id=test&subscription=%7B%7D"
            )
            assert response.status_code == 200

    def test_push_unsubscribe_endpoint_exists(self):
        with patch("tu_vi.main.push_unsubscribe", new_callable=AsyncMock) as mock_unsub:
            mock_unsub.return_value = True
            response = client.delete("/api/push/unsubscribe?device_id=test")
            assert response.status_code == 200

    def test_push_subscribe_uses_tuvi_app_name(self):
        with patch("tu_vi.main.push_subscribe", new_callable=AsyncMock) as mock_sub:
            mock_sub.return_value = {"success": True}
            client.post("/api/push/subscribe?device_id=test&subscription=%7B%7D")
            mock_sub.assert_called_once()
            call_args = mock_sub.call_args[0]
            assert call_args[1] == "tuvi"
