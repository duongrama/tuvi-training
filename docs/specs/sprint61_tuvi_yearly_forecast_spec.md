# Sprint 61: Tu Vi — Yearly Forecast / Lưu Niên (TV P2-4)

**Author:** TL | **Date:** 2026-03-16 | **Total:** 5pts
**Scope:** Tu Vi (port 17070) — yearly forecast with Lưu Niên palace rotation + monthly lucky/unlucky analysis
**Rationale:** Users want to see fortune outlook for a selected year. iztro-py's `horoscope()` method already provides Lưu Niên data — we just need to extract, translate, and present it.

---

## Context

iztro-py `chart.horoscope(date, hour)` returns:
- `yearly` — Lưu Niên: palace rotation for that year (12 palaces get shifted names), Tứ Hóa (mutagen), Can-Chi
- `monthly` — Lưu Nguyệt: same structure per month
- `age` — Tiểu Hạn: age-based annual fortune
- `nominal_age` — Vietnamese age

Currently Tu Vi shows: birth chart + Đại Hạn + current Tiểu Hạn. No way to explore a specific year's fortune.

---

## Items

### LN-1: BE — Yearly Forecast Endpoint (2pts)

**New endpoint:** `GET /api/tuvi/forecast/yearly`

**Query params:**
- `year` (int, required) — target year (e.g., 2026)
- `month` (int, optional) — birth month (from stored chart)
- `day` (int, optional) — birth day
- `hour` (int, optional) — birth hour
- `gender` (str, optional) — gender
- `device_id` (str, optional) — load from profile if params not provided

**Logic:**
1. Build chart from birth data (reuse `get_tuvi_chart()` pattern)
2. For each month (1-12) of target year, call `chart.horoscope(f'{year}-{month}-15', birth_hour)`
3. Extract from each horoscope:
   - `yearly.palace_names` — 12 Lưu Niên cung names (translated to Vietnamese)
   - `yearly.mutagen` — Lưu Niên Tứ Hóa (4 stars, translated)
   - `yearly.heavenly_stem` + `earthly_branch` — year's Can-Chi (translated)
   - `monthly.palace_names` — 12 Lưu Nguyệt cung names
   - `monthly.mutagen` — Lưu Nguyệt Tứ Hóa
   - `nominal_age` — Vietnamese age that year

**Response schema:**
```json
{
  "year": 2026,
  "can_chi": "Bính Ngọ",
  "nominal_age": 34,
  "luu_nien": {
    "menh": "Tài Bạch",
    "tu_hoa": ["Thiên Đồng Hóa Lộc", "Thiên Cơ Hóa Quyền", "Văn Xương Hóa Khoa", "Liêm Trinh Hóa Kỵ"],
    "palace_rotation": [
      {"position": "Tý", "luu_nien_cung": "Tài Bạch", "natal_cung": "Mệnh"},
      ...12 entries
    ]
  },
  "months": [
    {
      "month": 1,
      "luu_nguyet_menh": "Quan Lộc",
      "tu_hoa": ["...", "...", "...", "..."],
      "rating": "good|neutral|caution",
      "key_stars": ["Tả Phù", "Hữu Bật"]
    },
    ...12 entries
  ]
}
```

**Monthly rating logic (simple heuristic):**
- `good`: Lưu Nguyệt Mệnh falls on Tài Bạch/Quan Lộc/Phúc Đức + no Hóa Kỵ in Mệnh
- `caution`: Lưu Nguyệt Mệnh falls on Tật Ách/Nô Bộc + Hóa Kỵ present
- `neutral`: everything else

**Translation:** Reuse existing `translate_chinese()` from iztro_service.py for all star/palace name translations.

**Freemium:** This endpoint is gated — check usage before returning data. Uses same `TUVI_DAILY_LIMIT` as palace interpretation.

### LN-2: FE — Yearly Forecast View (2pts)

**Entry point:** New "Lưu Niên" tab/button on Tu Vi main page (next to existing "Luận Giải" buttons).

**UI Components:**

1. **Year Selector** — Dropdown or stepper (current year ± 5 years range). Default: current year.

2. **Year Overview Card** — Shows:
   - Target year + Can-Chi (e.g., "Năm 2026 — Bính Ngọ")
   - Vietnamese age (e.g., "Tuổi 34")
   - Lưu Niên Mệnh palace (e.g., "Lưu Niên Mệnh: Tài Bạch")
   - Lưu Niên Tứ Hóa (4 colored dots like existing Tứ Hóa display)

3. **12-Month Calendar Grid** — 3×4 or 4×3 grid showing:
   - Month name (Tháng 1-12)
   - Rating indicator (green dot = good, yellow = neutral, red = caution)
   - Lưu Nguyệt Mệnh palace name
   - Key Tứ Hóa star (abbreviated)

4. **Month Detail** — Click a month → expand/bottom-sheet showing:
   - Full Lưu Nguyệt palace rotation
   - Lưu Nguyệt Tứ Hóa (4 entries)
   - Brief interpretation (static text from lookup, NOT LLM — keep it fast)

**Design:** Follow existing Tu Vi dark theme + CSS variables. No Tailwind (plain CSS only). Use existing `md-*` CSS classes for text styling.

**Responsive:** Desktop shows grid inline. Mobile (<600px) uses vertical card list instead of grid.

### LN-3: Tests (1pt)

**BE tests (TDD):**
- `test_yearly_forecast_returns_12_months` — verify response has 12 month entries
- `test_yearly_forecast_has_luu_nien` — verify luu_nien object with palace_rotation
- `test_yearly_forecast_rating_logic` — verify good/neutral/caution assignment
- `test_yearly_forecast_different_year` — verify changing year changes results
- `test_yearly_forecast_freemium_gated` — verify 429 when limit reached
- `test_yearly_forecast_translation` — verify Chinese→Vietnamese translation applied
- Mock iztro-py `by_solar` + `horoscope` calls — NEVER call real library in tests

**FE tests:**
- `test_year_selector_changes_data` — mock fetch, verify re-render on year change
- `test_month_grid_renders_12_items` — verify 12 month cards present
- `test_month_click_shows_detail` — verify expand/bottom-sheet on click
- `test_rating_colors` — verify green/yellow/red classes applied correctly

---

## API Data Flow

```
User selects year 2026
  → FE: GET /api/tuvi/forecast/yearly?year=2026&device_id=X
  → BE: load profile → get birth data
  → BE: chart = by_solar(birth_date, hour, gender)
  → BE: for month 1-12:
       h = chart.horoscope(f'2026-{month}-15', hour)
       extract yearly + monthly data
       translate Chinese → Vietnamese
       calculate monthly rating
  → BE: return JSON with year overview + 12 months
  → FE: render year card + month grid
  → FE: click month → show detail panel
```

---

## Technical Notes

- iztro-py `horoscope()` is deterministic — same birth data + same date always returns same result. Safe to compute per-request (no caching needed for MVP).
- `palace_names` from horoscope uses English enum keys (e.g., `wealthPalace`). Must translate to Vietnamese using existing enum mapping.
- `mutagen` uses English star identifiers (e.g., `tiantongMaj`). Must translate using existing `translate_chinese()` or new enum map.
- Monthly rating is a simple heuristic for visual UX — not a deep astrological analysis. Can be refined later.
- Year range: limit to birth_year+1 through current_year+5. Don't allow years before birth.

---

## Acceptance Criteria

- [ ] GET /api/tuvi/forecast/yearly returns 12 months with ratings
- [ ] Lưu Niên Tứ Hóa correctly translated to Vietnamese
- [ ] Palace rotation changes per year (verify with 2 different years)
- [ ] Monthly rating (good/neutral/caution) renders with correct colors
- [ ] Year selector works (change year → new data)
- [ ] Freemium gated — uses per-device limit
- [ ] BE tests: 6+ tests, all mocked, 75%+ coverage
- [ ] FE tests: 4+ tests, 80%+ coverage
- [ ] All existing 1130+ tests still pass
