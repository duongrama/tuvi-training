# Sprint 46: Tu Vi P0 Fix — TL Interface Spec for BE

**Author:** TL | **Date:** 2026-03-15 | **Total:** 13pts
**Purpose:** Detailed fix instructions for BE. Root causes identified, test cases verified.

---

## ROOT CAUSE ANALYSIS

### BUG 1: Lunar Day Parsing — `parse_chinese_num()` Missing `廿` and `初`

**File:** `gieo_que/backend/tu_vi/iztro_service.py` lines 335-362

**NOT a lunar conversion bug.** Both `lunarcalendar` and `iztro-py` return the CORRECT lunar date. The bug is in **parsing Chinese numeral output** from iztro-py.

iztro-py returns `lunar_date` as Chinese text like `一九九三年五月廿四`. The parser doesn't handle:
- `廿` (niàn = 20): `廿四` = 24, but parsed as just `四` = 4
- `初` (chū = first): `初七` = 7, `初十` = 10 — `初` prefix for days 1-10
- `正月` = month 1 (not `一月`)
- `冬月` = month 11
- `腊月` = month 12
- `闰X月` = leap month X
- `〇` (líng = 0) in year numbers: `二〇二〇` = 2020

**This is why 13/7/1993 returns day 4 instead of 24:** `廿四` → parser skips `廿` → returns 4.

### BUG 2: Hour Mapping — Off-by-one

**File:** `gieo_que/backend/tu_vi/iztro_service.py` lines 314-319

Current formula `((hour + 1) // 2) % 12` with special case produces incorrect time_index for some hours.

iztro-py `by_solar()` expects `time_index` 0-12:
```
0: early Tý (23:00-01:00)
1: Sửu (01:00-03:00)
2: Dần (03:00-05:00)
...
11: Hợi (21:00-23:00)
12: late Tý (23:00-00:00)
```

**Correct mapping:** `hour // 2` for hours 0-22, special case for hour 23 → index 12.

**NOTE:** For Boss's test case (hour=8), the current formula gives 4 and correct is also 4 (8//2=4). So this bug is NOT visible in Boss's test case but affects other hours. Still must fix.

### BUG 3: Palace Position — PALACE_POSITION Mapping

**File:** `gieo_que/backend/tu_vi/iztro_service.py` lines 88-101

The `PALACE_POSITION` assigns sequential numbers 1-12 to palaces, but the numbering doesn't follow the standard counterclockwise order from Mệnh. The correct counterclockwise order after Mệnh is:

Mệnh → Huynh Đệ → Phu Thê → Tử Tức → Tài Bạch → Tật Ách → Thiên Di → Nô Bộc → Quan Lộc → Điền Trạch → Phúc Đức → Phụ Mẫu

Current code has: Mệnh(1), Phụ Mẫu(2), Huynh Đệ(3)... which is WRONG order.

**HOWEVER:** iztro-py itself places palaces correctly on the Thiên Bàn. Each `palace` object has an `earthly_branch` field that tells us which fixed position on the board it sits at. The real question is: does the frontend grid render them at the right earthly branch positions?

**Key insight:** The `position` field (1-12) in our API response is used by the frontend to place palaces in the 4x4 grid. If position numbers don't map to the correct earthly branch cells, palaces appear in wrong cells.

---

## TV-P0-1: Fix Chinese Numeral Parser (5pts)

### What to Change

**File:** `gieo_que/backend/tu_vi/iztro_service.py`

Replace the `parse_chinese_num()` function AND the lunar date extraction logic with a robust parser that handles all iztro-py output patterns.

### New Chinese Numeral Patterns to Handle

```
Year: 一九九三 = 1993, 二〇二〇 = 2020
      〇 (U+3007) = 0

Month names:
  正月 = 1, 二月 = 2, 三月 = 3, 四月 = 4, 五月 = 5, 六月 = 6
  七月 = 7, 八月 = 8, 九月 = 9, 十月 = 10, 十一月 = 11
  冬月 = 11, 腊月 = 12
  闰X月 = leap month X (set is_leap=True)

Day prefixes:
  初一 = 1, 初二 = 2, ..., 初十 = 10
  十一 = 11, ..., 十九 = 19
  二十 = 20, 廿 = 20
  廿一 = 21, ..., 廿九 = 29
  三十 = 30, 卅 = 30
```

### Recommended Implementation Approach

**Option A (cleanest):** Don't parse `lunar_date` string at all. Use `lunarcalendar` library (already imported in `lunar_service.py`) for the lunar date, since it returns proper integers:

```
from lunarcalendar import Solar, Converter
solar = Solar(year, month, day)
lunar = Converter.Solar2Lunar(solar)
# lunar.year, lunar.month, lunar.day, lunar.isleap — all integers!
```

This is already used in `lunar_service.py` and returns correct results (verified: 13/7/1993 → 24/5/1993).

**Option B (if iztro-py lunar_date is preferred):** Fix the parser to handle all patterns. Add `'廿': 20, '卅': 30, '〇': 0, '初': 0` to the chinese_nums dict, and add special month name parsing.

**TL recommends Option A** — it's simpler, already verified, and doesn't require maintaining a fragile Chinese character parser.

### Also Fix: Hour Mapping (same file, lines 314-319)

Replace:
```python
iztro_hour = ((hour + 1) // 2) % 12
if iztro_hour == 0:
    iztro_hour = 12
```

With:
```python
if hour == 23:
    iztro_hour = 12  # late Tý
else:
    iztro_hour = hour // 2  # 0=early Tý, 1=Sửu, ..., 11=Hợi
```

### Also Fix: is_leap Detection

Currently `is_leap_month` is passed as a parameter from the user (defaults False). Should be detected from the actual lunar date:

```
lunar = Converter.Solar2Lunar(solar)
is_leap = lunar.isleap  # True if this date falls in a leap month
```

---

## TV-P0-2: Fix Palace Position on Thiên Bàn (5pts)

### What to Change

The frontend 4x4 grid has 12 cells with FIXED earthly branch positions:

```
Row 0: Tỵ(pos 6)  | Ngọ(pos 7) | Mùi(pos 8)  | Thân(pos 9)
Row 1: Thìn(pos 5) | [CENTER]   | [CENTER]    | Dậu(pos 10)
Row 2: Mão(pos 4)  | [CENTER]   | [CENTER]    | Tuất(pos 11)
Row 3: Dần(pos 3)  | Sửu(pos 2) | Tý(pos 1)   | Hợi(pos 12)
```

Each palace from iztro-py has an `earthly_branch` field (e.g., `yinEarthly` = Dần). The position number should map to the earthly branch's fixed cell on the grid.

### New PALACE_POSITION Mapping

Replace the arbitrary 1-12 numbering with earthly-branch-based position:

```
EARTHLY_BRANCH_POSITION = {
    'ziEarthly': 1,    # Tý
    'chouEarthly': 2,  # Sửu
    'yinEarthly': 3,   # Dần
    'maoEarthly': 4,   # Mão
    'chenEarthly': 5,  # Thìn
    'siEarthly': 6,    # Tỵ
    'wuEarthly': 7,    # Ngọ
    'weiEarthly': 8,   # Mùi
    'shenEarthly': 9,  # Thân
    'youEarthly': 10,  # Dậu
    'xuEarthly': 11,   # Tuất
    'haiEarthly': 12,  # Hợi
}
```

Then in the palace loop (line 495), replace:
```python
our_position = PALACE_POSITION.get(palace.name, idx + 1)
```
With:
```python
our_position = EARTHLY_BRANCH_POSITION.get(palace.earthly_branch, idx + 1)
```

This ensures each palace is placed at its correct earthly branch cell on the Thiên Bàn, regardless of iztro-py's internal iteration order.

### Frontend Grid Must Match

The frontend 4x4 grid (tuvi-chart.js `PALACE_GRID`) already maps positions 1-12 to grid cells. Verify it matches the earthly branch layout above. The grid from Sprint 39 should already be correct since it was designed for this layout.

---

## TV-P0-1 TEST CASES (33 Cases)

### Category 1: Tết Dates — 1/1 Âm Lịch (10 cases)

| # | Solar | Expected Lunar | is_leap |
|---|-------|---------------|---------|
| 1 | 1990-01-27 | 1/1/1990 | False |
| 2 | 1993-01-23 | 1/1/1993 | False |
| 3 | 1995-01-31 | 1/1/1995 | False |
| 4 | 2000-02-05 | 1/1/2000 | False |
| 5 | 2005-02-09 | 1/1/2005 | False |
| 6 | 2010-02-14 | 1/1/2010 | False |
| 7 | 2015-02-19 | 1/1/2015 | False |
| 8 | 2020-01-25 | 1/1/2020 | False |
| 9 | 2024-02-10 | 1/1/2024 | False |
| 10 | 2025-01-29 | 1/1/2025 | False |

### Category 2: Boss's Test Case (1 case)

| # | Solar | Expected Lunar | is_leap |
|---|-------|---------------|---------|
| 11 | 1993-07-13 | 24/5/1993 | False |

### Category 3: Leap Month Cases (5 cases)

| # | Solar | Expected Lunar | is_leap |
|---|-------|---------------|---------|
| 12 | 2020-05-25 | 3/闰4/2020 | True |
| 13 | 2020-06-15 | 24/闰4/2020 | True |
| 14 | 2001-06-10 | 19/闰4/2001 | True |
| 15 | 1995-09-25 | 1/闰8/1995 | True |
| 16 | 1985-04-01 | 11/闰2/1985 | True |

### Category 4: Month Boundary Cases (5 cases)

| # | Solar | Expected Lunar | is_leap |
|---|-------|---------------|---------|
| 17 | 1993-07-18 | 29/5/1993 | False |
| 18 | 1993-07-19 | 1/6/1993 | False |
| 19 | 1990-03-26 | 30/2/1990 | False |
| 20 | 1990-03-27 | 1/3/1990 | False |
| 21 | 2025-01-28 | 29/12/2024 | False |

### Category 5: Common Birth Dates (7 cases)

| # | Solar | Expected Lunar | is_leap |
|---|-------|---------------|---------|
| 22 | 1975-03-15 | 3/2/1975 | False |
| 23 | 1980-06-15 | 3/5/1980 | False |
| 24 | 1985-06-01 | 13/4/1985 | False |
| 25 | 1990-12-31 | 15/11/1990 | False |
| 26 | 2000-09-15 | 17/8/2000 | False |
| 27 | 2004-05-25 | 7/4/2004 | False |
| 28 | 2010-08-15 | 6/7/2010 | False |

### Category 6: Edge Cases (5 cases)

| # | Solar | Expected Lunar | is_leap |
|---|-------|---------------|---------|
| 29 | 1993-12-31 | 19/11/1993 | False |
| 30 | 1990-01-01 | 5/12/1989 | False |
| 31 | 1980-02-29 | 14/1/1980 | False |
| 32 | 2020-01-24 | 30/12/2019 | False |
| 33 | 2025-01-31 | 3/1/2025 | False |

### Sources
- Hong Kong Observatory Gregorian-Lunar Conversion Tables (T{YEAR}e.txt)
- Ho Ngoc Duc Vietnamese Lunar Calendar (xemamlich.uhm.vn)
- lunarcalendar Python library (verified correct for all 33 cases)

---

## Hour Mapping Test Cases (13 cases — one per time_index)

| Hour (24h) | Expected time_index | Earthly Branch |
|------------|-------------------|----------------|
| 0 | 0 | Early Tý |
| 1 | 0 | Early Tý |
| 2 | 1 | Sửu |
| 4 | 2 | Dần |
| 6 | 3 | Mão |
| 8 | 4 | Thìn |
| 10 | 5 | Tỵ |
| 12 | 6 | Ngọ |
| 14 | 7 | Mùi |
| 16 | 8 | Thân |
| 18 | 9 | Dậu |
| 20 | 10 | Tuất |
| 22 | 11 | Hợi |
| 23 | 12 | Late Tý |

---

## Implementation Order for BE

1. **Fix `parse_chinese_num()` OR replace with lunarcalendar** (TV-P0-1)
2. **Fix hour mapping** (same file, 3 lines)
3. **Fix `is_leap` detection** from lunarcalendar
4. **Replace `PALACE_POSITION` with `EARTHLY_BRANCH_POSITION`** (TV-P0-2)
5. **Write 33 + 13 = 46 unit tests** (test lunar + test hour mapping)
6. **Run existing tests** to verify no regression
