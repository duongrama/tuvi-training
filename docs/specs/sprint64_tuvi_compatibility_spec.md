# Sprint 64: Tu Vi — Relationship Compatibility (TV P2-2)

**Author:** TL | **Date:** 2026-03-16 | **Total:** 6pts
**Scope:** Tu Vi (port 17070) — compare two birth charts for compatibility
**Rationale:** Users want to check relationship compatibility. iztro-py generates both charts, we compute compatibility from key palace + element data, then LLM provides narrative analysis.

---

## Context

iztro-py provides per-chart:
- `five_elements_class` (Cục: 金四局, 水二局, etc.)
- `zodiac` (Chinese zodiac animal)
- 12 palaces with major stars, earthly branch, brightness
- Phu Thê (Spouse) palace — most relevant for compatibility

No built-in compatibility method — we compute a score from traditional Tử Vi compatibility rules + let LLM narrate the analysis.

---

## Items

### CMP-1: BE — Compatibility Endpoint (3pts)

**New endpoint:** `POST /api/tuvi/compatibility`

**Request body:**
```json
{
  "person_a": {
    "name": "Anh",
    "year": 1993, "month": 6, "day": 13, "hour": 10, "gender": "nam"
  },
  "person_b": {
    "name": "Em",
    "year": 1995, "month": 3, "day": 22, "hour": 14, "gender": "nu"
  },
  "device_id": "xxx"
}
```

**Logic:**

1. **Generate both charts** via `iztro_py.by_solar()` (reuse existing `get_tuvi_chart()`)

2. **Compute compatibility score** (0-100) from 4 factors:

   **Factor 1 — Ngũ Hành Tương Sinh/Khắc (25pts max):**
   Extract Cục element (Kim/Mộc/Thủy/Hỏa/Thổ) from each chart's `five_elements_class`.
   - Tương Sinh (generating): 25pts (Kim→Thủy, Thủy→Mộc, Mộc→Hỏa, Hỏa→Thổ, Thổ→Kim)
   - Same element: 20pts
   - Tương Khắc (destructive): 5pts (Kim→Mộc, Mộc→Thổ, Thổ→Thủy, Thủy→Hỏa, Hỏa→Kim)
   - Neutral: 15pts

   **Factor 2 — Zodiac Compatibility (25pts max):**
   Traditional Tam Hợp (三合) and Lục Hợp (六合) pairings:
   - Tam Hợp (triad): 25pts (e.g., Thân-Tý-Thìn, Dần-Ngọ-Tuất, Tỵ-Dậu-Sửu, Hợi-Mão-Mùi)
   - Lục Hợp (pair): 22pts (e.g., Tý-Sửu, Dần-Hợi, Mão-Tuất, Thìn-Dậu, Tỵ-Thân, Ngọ-Mùi)
   - Lục Xung (clash): 5pts (e.g., Tý-Ngọ, Sửu-Mùi, Dần-Thân, Mão-Dậu, Thìn-Tuất, Tỵ-Hợi)
   - Neutral: 15pts

   **Factor 3 — Phu Thê Palace Stars (25pts max):**
   Check major stars in each person's Phu Thê (Spouse) palace:
   - Auspicious main stars (Thiên Phủ, Thiên Tướng, Thiên Lương, Thái Âm miếu): +25pts
   - Mixed stars (Tử Vi, Vũ Khúc, Tham Lang): +15pts
   - Challenging stars (Thất Sát, Phá Quân, Liêm Trinh): +8pts
   - Average both persons' scores

   **Factor 4 — Mệnh Palace Harmony (25pts max):**
   Compare earthly branches of both Mệnh palaces:
   - Tam Hợp/Lục Hợp: 25pts
   - Same branch: 20pts
   - Lục Xung: 5pts
   - Neutral: 15pts

   **Total = Factor 1 + Factor 2 + Factor 3 + Factor 4** (0-100 scale)

3. **Build LLM prompt** for narrative interpretation:
   - Include both charts' key data (Mệnh, Phu Thê, Cục, zodiac)
   - Include computed score + factor breakdown
   - Ask LLM to analyze: overall compatibility, strengths, challenges, advice
   - Use existing `stream_llm_response()` pattern
   - Inject Phu Thê palace doc if available (from Sprint 51/54 docs)

4. **Freemium gated** — counts as 1 reading

**Response schema:**
```json
{
  "score": 78,
  "rating": "Rất hợp",
  "factors": {
    "ngu_hanh": {"score": 25, "detail": "Kim sinh Thủy — Tương Sinh"},
    "zodiac": {"score": 22, "detail": "Dậu-Hợi — Lục Hợp"},
    "phu_the": {"score": 18, "detail": "A: Thái Âm (miếu), B: Tham Lang (vượng)"},
    "menh_harmony": {"score": 13, "detail": "Tý-Thân — Tam Hợp"}
  },
  "person_a": {"name": "Anh", "menh": "Mệnh", "cuc": "Kim Tứ Cục", "zodiac": "Dậu"},
  "person_b": {"name": "Em", "menh": "Mệnh", "cuc": "Thủy Nhị Cục", "zodiac": "Hợi"}
}
```

**Rating thresholds:**
- 80-100: "Rất hợp" (Excellent)
- 60-79: "Khá hợp" (Good)
- 40-59: "Bình thường" (Neutral)
- 20-39: "Cần cân nhắc" (Caution)
- 0-19: "Nhiều thử thách" (Challenging)

**Streaming option:** `POST /api/tuvi/compatibility/stream` — same data but LLM narrative streams via SSE. Score + factors returned in first SSE event, then LLM narrative streams.

### CMP-2: FE — Compatibility UI (2pts)

**Entry point:** New "Hợp Duyên" button on Tu Vi main page.

**UI Flow:**

1. **Input Panel** — Two-person form:
   - Person A: name, birth date (date picker), birth hour (dropdown 0-23), gender (toggle)
   - Person B: same fields
   - "So sánh" (Compare) button
   - If user has profile, auto-fill Person A from profile

2. **Results Panel:**
   - **Score Circle** — Large circular gauge (0-100) with color (green/yellow/red) + rating text
   - **4 Factor Bars** — Horizontal bars showing each factor's score (25pts max each)
     - Ngũ Hành: element icons + Tương Sinh/Khắc label
     - Zodiac: animal emojis + relationship type
     - Phu Thê: star names
     - Mệnh Harmony: earthly branch names
   - **LLM Analysis** — Streaming text below factors (same markdown rendering as palace interpretation)

3. **Design:** Follow Tu Vi dark theme. Plain CSS (no Tailwind). Score circle can use CSS conic-gradient or SVG arc.

### CMP-3: Tests (1pt)

**BE tests (TDD):**
- `test_compatibility_returns_score_and_factors` — verify response shape
- `test_ngu_hanh_tuong_sinh_scores_25` — Kim→Thủy = 25pts
- `test_ngu_hanh_tuong_khac_scores_5` — Kim→Mộc = 5pts
- `test_zodiac_tam_hop_scores_25` — Thân-Tý-Thìn triad
- `test_zodiac_luc_xung_scores_5` — Tý-Ngọ clash
- `test_compatibility_freemium_gated` — verify 429 at limit
- Mock `iztro_py.by_solar` + `stream_llm_response` — NEVER real calls

**FE tests:**
- `test_two_person_form_submits` — mock fetch, verify POST body
- `test_score_circle_renders` — verify score value + color class
- `test_factor_bars_render_4` — verify 4 factor bars present
- `test_streaming_analysis` — mock SSE, verify markdown render

---

## Technical Notes

- `five_elements_class` returns Chinese (金四局). Parse element: first char (金/木/水/火/土) → map to Vietnamese (Kim/Mộc/Thủy/Hỏa/Thổ)
- `zodiac` returns Chinese animal (鸡/猪/etc.). Translate via existing `translate_chinese()`
- Earthly branch from `get_soul_palace().earthly_branch` is English enum (ziEarthly). Map via existing `EARTHLY_BRANCH_MAP`
- Zodiac compatibility tables (Tam Hợp, Lục Hợp, Lục Xung) are static lookup — define as constants
- LLM prompt should include both charts' data in English bracket context injection pattern (Sprint 38 lesson)

---

## Acceptance Criteria

- [ ] POST /api/tuvi/compatibility returns score (0-100) + 4 factors
- [ ] Score changes with different birth data
- [ ] Ngũ Hành scoring follows Tương Sinh/Khắc rules
- [ ] Zodiac scoring follows Tam Hợp/Lục Hợp/Lục Xung
- [ ] LLM analysis streams via SSE (mocked in tests)
- [ ] Freemium gated (counts as 1 reading)
- [ ] FE shows score circle + 4 factor bars + streaming text
- [ ] Auto-fills Person A from profile if available
- [ ] BE tests: 7+, mocked, 75%+ coverage
- [ ] FE tests: 4+, 80%+ coverage
