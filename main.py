"""
Tu Vi API - Vietnamese Astrology Service

Runs on port 17070.
"""

import sys
import os

# Fix PYTHONPATH for iztro imports
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from dotenv import load_dotenv
load_dotenv(os.path.expanduser('~/dev/.env'))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response as FastAPIResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
import sys
from datetime import date
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '..'))
from shared.backend.profile_service import get_profile, save_profile, delete_profile, build_context_string
from shared.backend.daily_service import get_streak, update_streak
from shared.backend.share_service import generate_share_from_reading, build_og_meta
from shared.backend.push_service import subscribe as push_subscribe, unsubscribe as push_unsubscribe
from shared.backend.llm_service import invoke_llm, stream_llm_response
from shared.backend.freemium_service import get_usage, increment_usage
from tu_vi.llm_service import stream_tuvi_palace_interpretation
from tu_vi.lunar_service import birth_to_lunar, get_tuvi_chart, get_nap_giap_for_hour
from tu_vi.cung_service import calculate_12_cung, get_cung_details

# Freemium limit for Tu Vi (must match across get_usage/increment_usage checks)
TUVI_DAILY_LIMIT = 3


def _compute_usage(raw: dict) -> dict:
    """Recompute remaining using TUVI_DAILY_LIMIT (shared service hardcodes 9999)."""
    if raw.get("is_premium"):
        return {**raw, "limit": 0, "remaining": 0}
    remaining = max(0, TUVI_DAILY_LIMIT - raw.get("readings_count", 0))
    return {**raw, "limit": TUVI_DAILY_LIMIT, "remaining": remaining}

# ── Daily fortune cache (personalized per device_id+date) ──────────────
_tuvi_daily_cache: dict = {}

def make_tuvi_daily_cache_key(device_id: str, date_str: str) -> str:
    return f"tuvi_{device_id}_{date_str}"

def get_cached_tuvi_daily(device_id: str) -> dict:
    today = date.today().isoformat()
    key = make_tuvi_daily_cache_key(device_id, today)
    return _tuvi_daily_cache.get(key)

def cache_tuvi_daily(device_id: str, data: dict) -> None:
    today = date.today().isoformat()
    key = make_tuvi_daily_cache_key(device_id, today)
    _tuvi_daily_cache[key] = data

def calculate_tuvi_chart(year, month, day, hour, minute=0, gender="nam", is_leap_month=False, nam_xem=None):
    """Wrapper to calculate Tử Vi chart - import here to avoid recursion."""
    from tu_vi.iztro_service import get_tuvi_chart as _get_chart
    return _get_chart(year, month, day, hour, minute, gender, is_leap_month, nam_xem)


app = FastAPI(title="Tu Vi API", version="1.0.0")

app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CacheControlMiddleware(BaseHTTPMiddleware):
    """Add Cache-Control headers for static assets (PERF-4)."""
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        path = request.url.path
        if path.startswith("/shared/"):
            response.headers["Cache-Control"] = "public, max-age=86400"
        elif path.startswith("/js/") or path.startswith("/css/"):
            response.headers["Cache-Control"] = "public, max-age=3600"
        return response


app.add_middleware(CacheControlMiddleware)


@app.get("/api/og-meta")
async def og_meta(reading_id: str = "", name: str = "", birth_date: str = ""):
    """Return dynamic OG meta for a Tử Vi chart (SEO-1)."""
    if name:
        reading_title = f"Lá Số Tử Vi — {name}"
        description = f"Xem lá số tử vi cho {name}, sinh {birth_date}" if birth_date else f"Lá số tử vi của {name}"
    else:
        reading_title = "Lá Số Tử Vi"
        description = "Xem lá số tử vi theo phương pháp cổ truyền Việt Nam"
    return build_og_meta("Tử Vi", reading_title, description, "/shared/og-card.png")


BOT_UAS = ["facebookexternalhit", "Twitterbot", "TelegramBot", "LinkedInBot", "Slackbot"]


@app.middleware("http")
async def bot_og_middleware(request: Request, call_next):
    """Serve dynamic OG HTML to social bots (SEO-1)."""
    user_agent = request.headers.get("user-agent", "")
    is_bot = any(bot in user_agent for bot in BOT_UAS)
    name = request.query_params.get("name", "")
    if is_bot and request.url.path == "/" and name:
        birth_date = request.query_params.get("birth_date", "")
        reading_title = f"Lá Số Tử Vi — {name}"
        description = f"Xem lá số tử vi cho {name}, sinh {birth_date}" if birth_date else f"Lá số tử vi của {name}"
        meta = build_og_meta("Tử Vi", reading_title, description, "/shared/og-card.png")
        html = f"""<!DOCTYPE html><html lang="vi"><head>
<meta charset="UTF-8">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:image" content="{meta['image_url']}">
<meta property="og:type" content="website">
<title>{meta['title']}</title>
</head><body></body></html>"""
        return FastAPIResponse(html, media_type="text/html")
    return await call_next(request)


@app.get("/favicon.ico")
async def favicon():
    """Serve favicon — eliminates 404 in browser console."""
    _favicon = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'shared', 'frontend', 'favicon.ico')
    return FileResponse(_favicon)

# Serve shared frontend assets
SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'shared', 'frontend')
if os.path.exists(SHARED_DIR):
    app.mount("/shared", StaticFiles(directory=SHARED_DIR), name="shared")

# i18n files served at /i18n/ (consistent with all other apps)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
I18N_DIR = os.path.join(FRONTEND_DIR, "i18n")
if os.path.exists(I18N_DIR):
    app.mount("/i18n", StaticFiles(directory=I18N_DIR), name="i18n")

# Static file serving for frontend
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class BirthRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int = 0
    minute: int = 0
    is_leap_month: bool = False
    gender: str = "nam"
    nam_xem: int = None


@app.get("/")
def root():
    """Serve index.html."""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Tu Vi API - Use /api endpoints"}


@app.get("/sw.js")
def serve_sw():
    """Serve service worker at root scope (required for push notifications)."""
    return FileResponse(os.path.join(FRONTEND_DIR, "sw.js"), media_type="application/javascript")


@app.get("/manifest.json")
def serve_manifest():
    """Serve PWA manifest."""
    return FileResponse(os.path.join(FRONTEND_DIR, "manifest.json"), media_type="application/json")


@app.get("/hop-tuoi")
def serve_hop_tuoi():
    """Serve standalone hop-tuoi page (birth-year-only compatibility)."""
    return FileResponse(os.path.join(FRONTEND_DIR, "hop-tuoi.html"))


@app.get("/api/health")
def health():
    """Health check."""
    return {"status": "ok", "version": "1.0.0"}


# Profile endpoints
@app.get("/api/profile")
async def get_profile_endpoint(device_id: str = "default"):
    """Get user profile."""
    profile = await get_profile(device_id)
    if not profile:
        return {"profile": None}
    return {"profile": profile}


@app.post("/api/profile")
async def save_profile_endpoint(device_id: str = "default", request: dict = None):
    """Save user profile."""
    data = request or {}
    profile = await save_profile(device_id, data)
    return {"profile": profile}


@app.delete("/api/profile")
async def delete_profile_endpoint(device_id: str = "default"):
    """Delete user profile."""
    deleted = await delete_profile(device_id)
    return {"deleted": deleted}


@app.post("/api/lunar")
def convert_to_lunar(request: BirthRequest):
    """Convert solar birth date to lunar date."""
    try:
        result = birth_to_lunar(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_leap_month=request.is_leap_month
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/tuvi")
def get_tuvi(request: BirthRequest):
    """Get Tử Vi birth chart."""
    try:
        # First get lunar date
        birth_data = birth_to_lunar(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_leap_month=request.is_leap_month
        )

        # Then get chart
        chart = get_tuvi_chart(birth_data)

        # Add nap giap for hour
        chart["nap_giap_hour"] = get_nap_giap_for_hour(birth_data)

        return chart
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/cung")
def get_12_cung(request: BirthRequest):
    """Get 12 Cung placement for birth chart."""
    try:
        # First get lunar date
        birth_data = birth_to_lunar(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_leap_month=request.is_leap_month
        )

        lunar = birth_data["lunar"]
        can_chi = birth_data["can_chi"]

        # Extract year can and chi
        year_can = can_chi["year"].split()[0]
        year_chi = can_chi["year"].split()[1]

        # Calculate 12 cung with year_chi for full Nạp Âm
        cungs = calculate_12_cung(lunar["month"], year_can, request.hour, year_chi)

        # Get cung details
        cung_details = get_cung_details(cungs["cungs"], cungs["nap_am"])

        return {
            "birth": birth_data,
            "nap_am": cungs["nap_am"],
            "cung_menh": cungs["cung_menh"],
            "cung_than": cungs["cung_than"],
            "month_branch": cungs["month_branch"],
            "hour_branch": cungs["hour_branch"],
            "cungs": cungs["cungs"],
            "cung_details": cung_details
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/tuvi/chart")
def get_tuvi_chart_endpoint(request: BirthRequest):
    """Get complete Tử Vi birth chart with 14 Chính Tinh and fortune periods."""
    try:
        # Use iztro for correct calculations
        chart = calculate_tuvi_chart(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            gender=request.gender,
            is_leap_month=request.is_leap_month,
            nam_xem=request.nam_xem,
        )

        # dai_han / tieu_han / nap_am already in chart from iztro_service
        return chart
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tuvi/interpret")
def get_interpretation(palace_index: int = 1, star_name: str = None):
    """Get interpretation for a palace and optional star."""
    from tu_vi.interpretation_service import get_interpretation as _get_interp
    return _get_interp(palace_index, star_name)


class InterpretStreamRequest(BaseModel):
    question: str
    birth_info: dict
    chart_data: dict
    static_interpretation: str


@app.post("/api/tuvi/interpret/stream")
async def interpret_stream(request: InterpretStreamRequest, device_id: str = None):
    """Stream LLM interpretation for Tử Vi chart."""
    from tu_vi.llm_service import stream_tuvi_interpretation

    # Get user context for personalization
    user_context = ""
    if device_id:
        try:
            user_context = await build_context_string(device_id)
        except Exception as e:
            print(f"Warning: Failed to get user context: {e}")

    # Use shared stream_llm_response - TV allows timeframes
    return await stream_tuvi_interpretation(
        question=request.question,
        birth_info=request.birth_info,
        chart_data=request.chart_data,
        static_interpretation=request.static_interpretation,
        user_context=user_context
    )


# ── TV-FP-1: Daily Fortune ─────────────────────────────────────────────

@app.get("/api/tuvi/daily")
async def get_tuvi_daily(device_id: str = "default"):
    """Get personalized daily fortune based on user's birth chart."""
    profile = await get_profile(device_id)
    if not profile:
        return {"error": "no_profile"}

    # Extract birth data — profile may store 'birth_date' as 'dd/mm/yyyy' string
    try:
        if "birth_date" in profile:
            day_s, month_s, year_s = profile["birth_date"].split("/")
            p_year, p_month, p_day = int(year_s), int(month_s), int(day_s)
        elif all(k in profile for k in ("year", "month", "day")):
            p_year, p_month, p_day = int(profile["year"]), int(profile["month"]), int(profile["day"])
        else:
            return {"error": "no_profile"}
        p_hour = int(profile.get("hour", 0))
        p_gender = profile.get("gender", "nam")
    except (ValueError, AttributeError):
        return {"error": "no_profile"}

    # Return cached if available
    cached = get_cached_tuvi_daily(device_id)
    if cached:
        streak = await get_streak("tuvi", device_id)
        cached["streak_count"] = streak["consecutive_days"]
        return cached

    # Build chart context
    try:
        chart = calculate_tuvi_chart(
            year=p_year, month=p_month, day=p_day,
            hour=p_hour, gender=p_gender,
        )
    except Exception as e:
        return {"error": f"chart_error: {e}"}

    tieu_han = chart.get("tieu_han", {})
    palace_name = tieu_han.get("palace_name", "") if isinstance(tieu_han, dict) else ""
    stars = tieu_han.get("stars", []) if isinstance(tieu_han, dict) else []
    menh = chart.get("menh", "")
    today_str = date.today().strftime("%d/%m/%Y")
    stars_str = ", ".join(stars[:3]) if stars else "không có sao"

    system_prompt = "Bạn là nhà tử vi chuyên nghiệp. Luận giải bằng tiếng Việt, giọng dự báo, xưng hô 'bạn'."
    user_prompt = (
        f"Hôm nay {today_str}, người có Cung Mệnh {menh}, "
        f"Tiểu Hạn đang ở cung {palace_name} với các sao {stars_str}. "
        f"Hãy viết vận hạn ngắn gọn cho ngày hôm nay (2-3 đoạn, không đề cập ngày cụ thể trong tương lai)."
    )

    fortune_text = invoke_llm(system_prompt, user_prompt)

    result = {
        "fortune_text": fortune_text,
        "date": date.today().isoformat(),
        "palace_name": palace_name,
        "key_star": stars[0] if stars else "",
        "menh": menh,
    }
    cache_tuvi_daily(device_id, result)

    streak = await update_streak("tuvi", device_id)
    result["streak_count"] = streak["consecutive_days"]
    return result


@app.get("/api/tuvi/streak")
async def get_tuvi_streak(device_id: str = "default"):
    """Get user's daily reading streak for Tu Vi."""
    return await get_streak("tuvi", device_id)


@app.post("/api/streak/update")
async def update_streak_endpoint(device_id: str = "default"):
    """Update streak when user reads daily content."""
    return await update_streak("tuvi", device_id)


@app.get("/api/badges")
async def get_badges_endpoint(device_id: str = "default"):
    """Get badges earned by device."""
    from shared.backend.daily_service import get_badges
    return await get_badges(device_id)


# ── TV-FP-2: Share as Image ─────────────────────────────────────────────

@app.post("/api/tuvi/share")
async def generate_tuvi_share(request: dict):
    """Generate shareable birth chart summary image."""
    try:
        result = generate_share_from_reading(request, "tuvi")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── TV-FP-3: Push Notifications ─────────────────────────────────────────

@app.post("/api/push/subscribe")
async def push_subscribe_endpoint(device_id: str = "default", subscription: str = ""):
    """Subscribe to push notifications."""
    return await push_subscribe(device_id, "tuvi", subscription)


@app.delete("/api/push/unsubscribe")
async def push_unsubscribe_endpoint(device_id: str = "default"):
    """Unsubscribe from push notifications."""
    success = await push_unsubscribe(device_id, "tuvi")
    return {"success": success}


# ── Freemium usage endpoints ─────────────────────────────────────────────

@app.get("/api/usage")
async def get_usage_endpoint(device_id: str = "default"):
    """Get daily usage for freemium gating."""
    raw = await get_usage("tuvi", device_id)
    return _compute_usage(raw)


@app.post("/api/usage/increment")
async def increment_usage_endpoint(device_id: str = "default"):
    """Increment usage after a reading."""
    try:
        raw = await increment_usage("tuvi", device_id, daily_limit=TUVI_DAILY_LIMIT)
        return _compute_usage(raw)
    except PermissionError:
        raw = await get_usage("tuvi", device_id)
        raise HTTPException(status_code=429, detail="Daily limit reached.")


# ── Palace name extraction helper ────────────────────────────────────────

_PALACE_NAME_MAP = {
    "mệnh": "menh",
    "menh": "menh",
    "phụ mẫu": "phu_mau",
    "huynh đệ": "huynh_de",
    "tử tức": "tu_tuc",
    "phúc đức": "phuc_duc",
    "điền trạch": "dien_trach",
    "quan lộc": "quan_loc",
    "thiên di": "thien_di",
    "tài bạch": "tai_bach",
    "tật ách": "tat_ach",
    "nô bộc": "no_boc",
    "phu thê": "phu_the",
    "phú thê": "phu_the",
}


def _extract_palace_name(question: str) -> str:
    """Attempt to extract palace_name key from question string."""
    q = question.lower()
    for vn_name, key in _PALACE_NAME_MAP.items():
        if vn_name in q:
            return key
    return ""


class PalaceInterpretRequest(BaseModel):
    question: str = ""
    birth_info: dict = {}
    chart_data: dict = {}
    static_interpretation: str = ""
    palace_name: str = ""  # extracted from question if empty


@app.post("/api/tuvi/interpret/palace")
async def interpret_palace(request: PalaceInterpretRequest, device_id: str = "default"):
    """Stream per-palace LLM interpretation with freemium gating.

    Accepts FE format: {question, birth_info, chart_data, static_interpretation, palace_name}.
    Uses chart_data directly — no redundant chart recalculation.
    """
    # ── Freemium gate ──────────────────────────────────────────────────
    usage = _compute_usage(await get_usage("tuvi", device_id))
    if usage["remaining"] <= 0 and not usage["is_premium"]:
        raise HTTPException(status_code=429, detail="Daily limit reached. Upgrade to premium.")

    # ── Resolve palace_name ────────────────────────────────────────────
    palace_name = request.palace_name or _extract_palace_name(request.question)

    # ── Extract target palace from existing chart_data ─────────────────
    chart = request.chart_data
    palaces = chart.get("palaces", [])
    target_palace = None
    for p in palaces:
        pname = p.get("cung_name", "").lower().replace(" ", "_")
        if pname == palace_name.lower() or p.get("palace_name", "").lower() == palace_name.lower():
            target_palace = p
            break
    if target_palace is None:
        target_palace = {"stars": [], "trang_sinh": "", "bac_si": "", "thai_tue": "", "tuong_tinh": ""}

    # ── Load interpretation doc ────────────────────────────────────────
    docs_dir = os.path.join(os.path.dirname(__file__), "docs", "interpretations")
    doc_path = os.path.join(docs_dir, f"{palace_name}.md")
    if os.path.exists(doc_path):
        with open(doc_path, encoding="utf-8") as f:
            palace_doc = f.read()
    else:
        palace_doc = f"# Cung {palace_name}\nKhông có tài liệu chi tiết."

    # ── Build chart summary from chart_data ────────────────────────────
    chart_summary = {
        "cung_menh": chart.get("menh", ""),
        "nap_am": chart.get("nap_am", {}),
    }

    # ── Stream LLM response ────────────────────────────────────────────
    response = await stream_tuvi_palace_interpretation(
        palace_name=palace_name,
        palace_data=target_palace,
        palace_doc=palace_doc,
        chart_summary=chart_summary,
    )

    # ── Increment usage after initiating stream ────────────────────────
    try:
        await increment_usage("tuvi", device_id, daily_limit=TUVI_DAILY_LIMIT)
    except PermissionError:
        pass  # Stream already sent — skip increment, don't error

    return response


# ── LN-1: Yearly Forecast / Lưu Niên ─────────────────────────────────────

_TU_HOA_ORDER = ["Hóa Lộc", "Hóa Quyền", "Hóa Khoa", "Hóa Kỵ"]
_GOOD_PALACES = {"Tài Bạch", "Quan Lộc", "Phúc Đức"}
_CAUTION_PALACES = {"Tật Ách", "Nô Bộc"}


def _build_yearly_tu_hoa(mutagen: list) -> list:
    """Translate iztro-py yearly mutagen (4 English star IDs) → Vietnamese Tứ Hóa strings."""
    from tu_vi.iztro_service import ENGLISH_STAR_TRANSLATIONS
    result = []
    for i, star_en in enumerate(mutagen or []):
        star_vn = ENGLISH_STAR_TRANSLATIONS.get(star_en, star_en)
        result.append(f"{star_vn} {_TU_HOA_ORDER[i]}" if i < 4 else star_vn)
    return result


def _monthly_rating(luu_nguyet_menh: str, monthly_tu_hoa: list) -> str:
    """Simple heuristic: good/caution/neutral based on Lưu Nguyệt Mệnh palace + Hóa Kỵ."""
    has_hoa_ky = any("Hóa Kỵ" in s for s in monthly_tu_hoa)
    if luu_nguyet_menh in _GOOD_PALACES and not has_hoa_ky:
        return "good"
    if luu_nguyet_menh in _CAUTION_PALACES and has_hoa_ky:
        return "caution"
    return "neutral"


@app.get("/api/tuvi/forecast/yearly")
async def yearly_forecast(
    year: int,
    birth_year: int = None,
    birth_month: int = None,
    birth_day: int = None,
    birth_hour: int = None,
    gender: str = None,
    device_id: str = "default",
):
    """Get yearly Lưu Niên forecast + 12-month Lưu Nguyệt breakdown."""
    from iztro_py import by_solar
    from tu_vi.iztro_service import (
        ENGLISH_PALACE_TRANSLATIONS, ENGLISH_STAR_TRANSLATIONS,
        HEAVENLY_STEM_MAP, EARTHLY_BRANCH_MAP, translate_chinese,
        get_iztro_hour,
    )

    # ── Freemium gate ──────────────────────────────────────────────────
    usage = _compute_usage(await get_usage("tuvi", device_id))
    if usage["remaining"] <= 0 and not usage["is_premium"]:
        raise HTTPException(status_code=429, detail="Daily limit reached. Upgrade to premium.")

    # ── Resolve birth data: params > profile ───────────────────────────
    if not all([birth_year, birth_month, birth_day]):
        profile = await get_profile(device_id)
        if not profile:
            raise HTTPException(status_code=400, detail="Birth data required. Set profile or pass params.")
        try:
            if "birth_date" in profile:
                d, m, y = profile["birth_date"].split("/")
                birth_year, birth_month, birth_day = int(y), int(m), int(d)
            else:
                birth_year = int(profile["year"])
                birth_month = int(profile["month"])
                birth_day = int(profile["day"])
        except (KeyError, ValueError, AttributeError):
            raise HTTPException(status_code=400, detail="Invalid profile birth data.")
        birth_hour = birth_hour if birth_hour is not None else int(profile.get("hour", 0))
        gender = gender or profile.get("gender", "nam")

    birth_hour = birth_hour or 0
    gender = gender or "nam"
    iztro_hour = get_iztro_hour(birth_hour)
    iztro_gender = "男" if gender.lower() in ("nam", "male", "m") else "女"

    # ── Build chart ────────────────────────────────────────────────────
    date_str = f"{birth_year}-{birth_month}-{birth_day}"
    chart = by_solar(date_str, iztro_hour, iztro_gender)

    # ── Yearly overview: use June 15 (post-Lập Xuân, reliable year) ───
    h_ref = chart.horoscope(f"{year}-6-15", iztro_hour)
    y_data = h_ref.yearly

    # Can-Chi for the year
    stem_cn = HEAVENLY_STEM_MAP.get(y_data.heavenly_stem, y_data.heavenly_stem)
    branch_cn = EARTHLY_BRANCH_MAP.get(y_data.earthly_branch, y_data.earthly_branch)
    can_chi = translate_chinese(stem_cn + branch_cn)

    # Lưu Niên Tứ Hóa
    luu_nien_tu_hoa = _build_yearly_tu_hoa(y_data.mutagen)

    # Palace rotation: index i in palace_names corresponds to chart.palaces[i]
    # palace_names[0] = the role the first palace plays in Lưu Niên (= Lưu Niên Mệnh)
    luu_nien_menh = ENGLISH_PALACE_TRANSLATIONS.get(y_data.palace_names[0], "")

    palace_rotation = []
    for i, pname_en in enumerate(y_data.palace_names):
        orig_palace = chart.palaces[i]
        branch_cn_p = EARTHLY_BRANCH_MAP.get(orig_palace.earthly_branch, "")
        position_vn = translate_chinese(branch_cn_p)
        luu_nien_cung = ENGLISH_PALACE_TRANSLATIONS.get(pname_en, pname_en)
        natal_cung = ENGLISH_PALACE_TRANSLATIONS.get(orig_palace.name, orig_palace.name)
        palace_rotation.append({
            "position": position_vn,
            "luu_nien_cung": luu_nien_cung,
            "natal_cung": natal_cung,
        })

    luu_nien = {
        "menh": luu_nien_menh,
        "tu_hoa": luu_nien_tu_hoa,
        "palace_rotation": palace_rotation,
    }

    # ── Monthly breakdown ──────────────────────────────────────────────
    months = []
    for m in range(1, 13):
        h_m = chart.horoscope(f"{year}-{m}-15", iztro_hour)
        m_data = h_m.monthly

        # palace_names[0] = the role the first palace plays this month (= Lưu Nguyệt Mệnh)
        luu_nguyet_menh = ENGLISH_PALACE_TRANSLATIONS.get(m_data.palace_names[0], "")
        m_tu_hoa = _build_yearly_tu_hoa(m_data.mutagen)
        rating = _monthly_rating(luu_nguyet_menh, m_tu_hoa)
        key_stars = [s.split(" Hóa")[0] for s in m_tu_hoa[:2]]

        months.append({
            "month": m,
            "luu_nguyet_menh": luu_nguyet_menh,
            "tu_hoa": m_tu_hoa,
            "rating": rating,
            "key_stars": key_stars,
        })

    return {
        "year": year,
        "can_chi": can_chi,
        "nominal_age": h_ref.nominal_age,
        "luu_nien": luu_nien,
        "months": months,
    }


# ── CMP-1: Compatibility Endpoint ─────────────────────────────────────────────

class PersonBirth(BaseModel):
    name: str = ""
    year: int
    month: int
    day: int
    hour: int = 0
    gender: str = "nam"


class CompatibilityRequest(BaseModel):
    person_a: PersonBirth
    person_b: PersonBirth
    device_id: str = "default"


@app.post("/api/tuvi/compatibility")
async def tuvi_compatibility(request: CompatibilityRequest):
    """Compute Tu Vi compatibility for two birth charts.

    Returns score (0-100), rating, 4 factor breakdowns, and LLM narrative analysis.
    Freemium gated — counts as 1 reading.
    """
    from iztro_py import by_solar
    from tu_vi.iztro_service import get_iztro_hour, ENGLISH_STAR_TRANSLATIONS
    from tu_vi.compatibility_service import compute_compatibility, get_rating

    # ── Freemium gate ──────────────────────────────────────────────────
    usage = _compute_usage(await get_usage("tuvi", request.device_id))
    if usage["remaining"] <= 0 and not usage["is_premium"]:
        raise HTTPException(status_code=429, detail="Daily limit reached. Upgrade to premium.")

    def _build_chart(person: PersonBirth):
        iztro_hour = get_iztro_hour(person.hour)
        iztro_gender = "男" if person.gender.lower() in ("nam", "male", "m") else "女"
        date_str = f"{person.year}-{person.month}-{person.day}"
        return by_solar(date_str, iztro_hour, iztro_gender)

    # ── Generate both charts ───────────────────────────────────────────
    chart_a = _build_chart(request.person_a)
    chart_b = _build_chart(request.person_b)

    # ── Compute scores ─────────────────────────────────────────────────
    result = compute_compatibility(chart_a, chart_b,
                                   name_a=request.person_a.name,
                                   name_b=request.person_b.name)

    # ── LLM narrative ──────────────────────────────────────────────────
    pa = result["person_a"]
    pb = result["person_b"]
    factors = result["factors"]
    system_prompt = (
        "Bạn là nhà tử vi chuyên về tình duyên hợp số. "
        "Phân tích bằng tiếng Việt, giọng ấm áp, xưng hô 'hai bạn'."
    )
    user_prompt = (
        f"[CONTEXT - dùng nội bộ để phân tích, không nhắc lại]\n"
        f"Người A ({pa['name']}): Cung Mệnh {pa['menh']}, Cục {pa['cuc']}, Tuổi {pa['zodiac']}\n"
        f"Người B ({pb['name']}): Cung Mệnh {pb['menh']}, Cục {pb['cuc']}, Tuổi {pb['zodiac']}\n"
        f"Điểm tổng: {result['score']}/100 ({result['rating']})\n"
        f"Ngũ Hành: {factors['ngu_hanh']['detail']} ({factors['ngu_hanh']['score']}đ)\n"
        f"Tuổi: {factors['zodiac']['detail']} ({factors['zodiac']['score']}đ)\n"
        f"Phu Thê: {factors['phu_the']['detail']} ({factors['phu_the']['score']}đ)\n"
        f"Cung Mệnh: {factors['menh_harmony']['detail']} ({factors['menh_harmony']['score']}đ)\n"
        f"[END CONTEXT]\n\n"
        f"Viết phân tích hợp duyên cho hai người trên: tổng quan, điểm mạnh, thử thách, lời khuyên. "
        f"Khoảng 3-4 đoạn ngắn."
    )
    analysis = invoke_llm(system_prompt, user_prompt)

    # ── Increment usage ────────────────────────────────────────────────
    try:
        await increment_usage("tuvi", request.device_id, daily_limit=TUVI_DAILY_LIMIT)
    except PermissionError:
        pass

    return {**result, "analysis": analysis}


class CompatibilityStreamRequest(BaseModel):
    score: int
    rating: str
    factors: dict
    person_a: dict   # {name, menh, cuc, zodiac} OR {year, name, zodiac, element, nap_am}
    person_b: dict
    device_id: str = "default"
    context: str = "romance"           # romance / family / business (Sprint 98 COMP-4)
    invitation_id: str | None = None   # for hop-tuoi viral flow (Sprint 98 COMP-4)


@app.post("/api/tuvi/compatibility/stream")
async def tuvi_compatibility_stream(request: CompatibilityStreamRequest):
    """Stream Tu Vi compatibility LLM narrative via SSE.

    Accepts pre-computed score+factors from /api/tuvi/compatibility.
    Streams LLM narrative only — no iztro_py chart re-computation.
    Freemium gated — counts as 1 reading.
    """
    import json
    from fastapi.responses import StreamingResponse

    # ── Freemium gate ──────────────────────────────────────────────────
    usage = _compute_usage(await get_usage("tuvi", request.device_id))
    if usage["remaining"] <= 0 and not usage["is_premium"]:
        raise HTTPException(status_code=429, detail="Daily limit reached. Upgrade to premium.")

    pa = request.person_a
    pb = request.person_b
    factors = request.factors
    ctx = request.context or "romance"

    # ── Context-specific system prompt ──────────────────────────────────────
    context_framing = {
        "romance": "tình duyên và hôn nhân",
        "family": "mối quan hệ gia đình thân thiết",
        "business": "hợp tác kinh doanh và sự nghiệp",
    }.get(ctx, "tình duyên và hôn nhân")

    system_prompt = (
        f"Bạn là nhà tử vi chuyên về {context_framing}. "
        "Phân tích bằng tiếng Việt, giọng ấm áp, xưng hô 'hai bạn'. "
        "LUÔN viết đầy đủ 5 phần theo đúng tiêu đề được chỉ định dưới đây — "
        "không bỏ qua phần nào, kể cả khi kết quả đã tốt."
    )

    # ── Build verdict strings (hop-tuoi vs full-chart) ──────────────────────
    z_factor = factors.get("zodiac", {})
    e_factor = factors.get("element", {})
    # Fallback for full-chart factor structure
    ngu_hanh_factor = factors.get("ngu_hanh", {})
    phu_the_factor = factors.get("phu_the", {})
    menh_factor = factors.get("menh_harmony", {})

    if e_factor:  # hop-tuoi flow (COMP-4): zodiac + element
        zodiac_info = (
            f"Con Giáp: {pa.get('zodiac', '?')} và {pb.get('zodiac', '?')} — "
            f"{z_factor.get('detail', '')} ({z_factor.get('score', 0)}đ)"
        )
        element_info = (
            f"Ngũ Hành: {pa.get('element', '?')} và {pb.get('element', '?')} — "
            f"{e_factor.get('detail', '')} ({e_factor.get('score', 0)}đ)"
        )
    else:  # full-chart flow (S64): ngu_hanh + zodiac + phu_the + menh_harmony
        zodiac_info = f"Tuổi: {z_factor.get('detail', '')} ({z_factor.get('score', 0)}đ)"
        element_info = f"Ngũ Hành: {ngu_hanh_factor.get('detail', '')} ({ngu_hanh_factor.get('score', 0)}đ)\nPhu Thê: {phu_the_factor.get('detail', '')} ({phu_the_factor.get('score', 0)}đ)\nCung Mệnh: {menh_factor.get('detail', '')} ({menh_factor.get('score', 0)}đ)"

    user_prompt = (
        "[CONTEXT - DO NOT echo or mention this block. Use silently to personalize.]\n"
        f"Người A ({pa.get('name', 'A')}, năm {pa.get('year', '?')}): {pa.get('zodiac', '')}, {pa.get('nap_am', '')}, mệnh {pa.get('element', pa.get('menh', ''))}\n"
        f"Người B ({pb.get('name', 'B')}, năm {pb.get('year', '?')}): {pb.get('zodiac', '')}, {pb.get('nap_am', '')}, mệnh {pb.get('element', pb.get('menh', ''))}\n"
        f"Điểm tổng: {request.score}/100 ({request.rating})\n"
        f"{zodiac_info}\n"
        f"{element_info}\n"
        "[END CONTEXT]\n\n"
        "Viết phân tích theo ĐÚNG 5 phần sau — mỗi phần có tiêu đề riêng:\n\n"
        "## 1. Phân Tích Con Giáp\n"
        "[Phân tích chi tiết về sự tương thích của hai con giáp]\n\n"
        "## 2. Phân Tích Ngũ Hành\n"
        "[Phân tích tương tác ngũ hành giữa hai người]\n\n"
        "## 3. Điểm Mạnh\n"
        "[3-4 điểm mạnh của cặp đôi này]\n\n"
        "## 4. Điểm Ma Sát\n"
        "[3-4 điểm ma sát hoặc thử thách]\n\n"
        "## 5. Hòa Giải & Lời Khuyên\n"
        "[LUÔN viết phần này — kể cả khi đã hợp nhau. "
        "Nếu Tương Khắc: gợi ý màu sắc, hướng, yếu tố trung gian. "
        "Nếu Lục Xung: gợi ý thời điểm, hoạt động bổ trợ. "
        "Nếu đã hợp: lời khuyên củng cố và duy trì.]"
    )

    score_event = json.dumps({
        "score": request.score,
        "rating": request.rating,
        "factors": request.factors,
        "person_a": request.person_a,
        "person_b": request.person_b,
        "context": ctx,
        "invitation_id": request.invitation_id,
    }, ensure_ascii=False)

    async def event_generator():
        # First event: score + factors JSON
        yield f"data: {score_event}\n\n"
        # Subsequent events: LLM narrative (delegate to stream_llm_response generator)
        # We call it and forward its SSE output
        from langchain_core.messages import HumanMessage, SystemMessage
        from shared.backend.llm_service import create_llm
        llm = create_llm(streaming=True)
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
        async for chunk in llm.astream(messages):
            text = chunk.content if hasattr(chunk, "content") else str(chunk)
            if text:
                yield f"data: {text}\n\n"
        yield "data: [DONE]\n\n"
        # Increment usage
        try:
            await increment_usage("tuvi", request.device_id, daily_limit=TUVI_DAILY_LIMIT)
        except PermissionError:
            pass

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ======================================================================
# Hợp Tuổi — Birth-year-only compatibility (Sprint 98 COMP-1)
# ======================================================================

class HopTuoiRequest(BaseModel):
    year_a: int
    year_b: int


@app.post("/api/tuvi/hop-tuoi")
async def hop_tuoi(request: HopTuoiRequest):
    """Compute birth-year-only compatibility score.

    No freemium gate — free teaser endpoint.
    Score 0-50 (zodiac 0-25 + element 0-25).
    """
    if not (1900 <= request.year_a <= 2025 and 1900 <= request.year_b <= 2025):
        raise HTTPException(status_code=400, detail="Year must be 1900-2025")

    from tu_vi.hop_tuoi_service import score_hop_tuoi
    return score_hop_tuoi(request.year_a, request.year_b)


class InvitationCreateRequest(BaseModel):
    initiator_device_id: str
    year_a: int
    year_b: int
    name_a: str = ""
    name_b: str = ""
    context: str = "romance"
    hop_tuoi_result: dict = {}


@app.post("/api/tuvi/invitation/create")
async def invitation_create(request: InvitationCreateRequest):
    """Create a shareable Hợp Tuổi invitation."""
    from tu_vi.invitation_service import create_invitation
    return await create_invitation(
        initiator_device_id=request.initiator_device_id,
        year_a=request.year_a,
        year_b=request.year_b,
        name_a=request.name_a,
        name_b=request.name_b,
        context=request.context,
        hop_tuoi_result=request.hop_tuoi_result,
    )


@app.get("/api/tuvi/invitation/{invitation_id}")
async def invitation_get(invitation_id: str):
    """Retrieve invitation by 8-char ID."""
    from tu_vi.invitation_service import get_invitation
    result = await get_invitation(invitation_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return result


class InvitationCompleteRequest(BaseModel):
    partner_device_id: str


@app.post("/api/tuvi/invitation/{invitation_id}/complete")
async def invitation_complete(invitation_id: str, request: InvitationCompleteRequest):
    """Mark invitation as completed by partner."""
    from tu_vi.invitation_service import complete_invitation
    result = await complete_invitation(invitation_id, request.partner_device_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return {"partner_completed": True, **result}


# ======================================================================
# Main
# ======================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=17070)
