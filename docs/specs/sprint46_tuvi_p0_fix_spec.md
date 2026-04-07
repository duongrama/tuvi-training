# Sprint 46: P0 — Tu Vi Lunar Conversion + Palace Position Fix

**Author:** PO | **Date:** 2026-03-15 | **Total:** 13pts
**Scope:** Tu Vi (port 17070) — core algorithm bugs
**Rationale:** Boss verified: 13/7/1993 solar should = 24/5/1993 âm lịch. API returns 4/5/1993. 20-day error. Wrong lunar → wrong palaces → wrong stars → wrong everything. Also: palace positions must follow Thiên Bàn (fixed earthly branch positions).

---

## Bug Evidence

**Input:** year=1993, month=7, day=13, hour=8, gender=male, calendar_type=solar
**Expected lunar:** 24/5/1993 (Quý Dậu, verified by Boss)
**Got:** 4/5/1993 — 20-day discrepancy
**Impact:** Every chart generated since launch has potentially wrong lunar dates → wrong palace placement → wrong star positions → wrong interpretations

---

## Items

### TV-P0-1: Fix Lunar Calendar Conversion (5pts) — TL+BE

**Problem:** The solar→lunar conversion algorithm is producing wrong dates.

**Requirements:**
1. TL researches correct lunar↔solar conversion algorithm
2. Search Google for reliable Vietnamese/Chinese lunar calendar conversion test data
3. Create **33 unit test cases** (Boss directive) covering:
   - Multiple years (1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020s)
   - Leap months (tháng nhuận) — these are the hardest
   - Edge cases: New Year boundary, last day of lunar month, first day of lunar month
   - Boss's birth data as mandatory test: 13/7/1993 solar = 24/5/1993 lunar
4. ALL 33 tests must PASS before any code is merged
5. If current library (iztro-py) has the bug, consider alternatives or patching

### TV-P0-2: Fix Palace Position Layout — Thiên Bàn (5pts) — TL+FE

**Problem:** Palace positions may not follow the traditional Thiên Bàn fixed layout.

**What is Thiên Bàn:**
- The 12 earthly branches (Tý, Sửu, Dần, Mão, Thìn, Tỵ, Ngọ, Mùi, Thân, Dậu, Tuất, Hợi) are at FIXED positions on the board
- They NEVER move — this is the "Celestial Board" (Thiên Bàn)
- The 12 palace NAMES (Mệnh, Phụ Mẫu, Phúc Đức, Điền Trạch...) are placed INTO these fixed positions based on birth month and hour
- The palace grid must show earthly branches at fixed positions, with palace names overlaid

**Requirements:**
1. TL verifies current implementation against traditional Thiên Bàn rules
2. The 4x4 grid layout (from Sprint 39) must show:
   - Fixed earthly branch labels at standard positions
   - Palace names placed according to correct algorithm
   - Stars placed into palaces (which are in fixed earthly branch positions)
3. If current implementation moves earthly branches instead of placing palaces into fixed positions, this is fundamentally wrong and must be rewritten

### TV-P0-3: Regression Test Suite (3pts) — QA

**Requirements:**
1. Run all 33 lunar conversion tests
2. Verify chart output for 5 known birth dates (including Boss's test case)
3. Compare palace positions against known reference (traditional Tử Vi software or manual calculation)
4. Playwright E2E: enter 13/7/1993, verify lunar shows 24/5/1993

---

## Execution Order

1. TL researches both bugs — identifies root cause in current code
2. TL creates 33 lunar test cases (search Google for verified solar↔lunar pairs)
3. BE fixes lunar conversion — must pass all 33 tests
4. TL+FE fix palace layout if needed (Thiên Bàn rules)
5. TL reviews all changes
6. QA runs regression suite
7. PO Playwright-verifies with Boss's test case

## Acceptance Criteria

- [ ] 13/7/1993 solar → 24/5/1993 lunar (exact match)
- [ ] 33 lunar conversion unit tests ALL passing
- [ ] Palace positions follow Thiên Bàn (fixed earthly branch positions)
- [ ] TL code review approved
- [ ] Playwright E2E verified by PO
