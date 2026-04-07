# Sprint 48: P0 — Tu Vi Đại Hạn Direction + Nạp Âm Fix

**Author:** TL | **Date:** 2026-03-15 | **Total:** 10pts
**Scope:** Tu Vi (port 17070) — Đại Hạn direction + Nạp Âm display
**Rationale:** Boss verified: 18/5/1984 Nam giờ Tý (Giáp Tý year) should have Đại Hạn THUẬN (Tỵ→Ngọ→Mùi clockwise). App shows NGHỊCH. Also Nạp Âm shows "Mộc Tam Cục" (which is Cục) instead of "Hải Trung Kim" (the actual Nạp Âm for Giáp Tý).

---

## ROOT CAUSE ANALYSIS

### BUG 1: Đại Hạn — Custom Service Ignores iztro-py Data

**File:** `gieo_que/backend/tu_vi/fortune_period_service.py` (206 lines)

This is a **completely wrong custom implementation** that:
- Uses `birth_year % 12` for starting position (should use Mệnh Cung's earthly branch)
- Always goes forward for male, backward for female (WRONG — should check Dương/Âm of year stem)
- Calculates its own start_age from year_offset (should use Cục value: 2/3/4/5/6)
- Does NOT use iztro-py's `palace.decadal` data which is already CORRECT

**Proof:** iztro-py returns correct data for Boss's test case:
- Mệnh at Tỵ, decadal range (3,12) — first period
- Next: Ngọ (13,22) — clockwise (THUẬN) ✓
- Mùi (23,32), Thân (33,42)... all correct

**Fix:** Delete `fortune_period_service.py` entirely. Build Đại Hạn timeline from iztro-py's `palace.decadal` data that `iztro_service.py` already extracts into each palace.

### BUG 2: Nạp Âm — Conflated with Cục

**File:** `gieo_que/backend/tu_vi/iztro_service.py` lines 548-552

Current code:
```python
"nap_am": {
    "nam": cung_menh_dia_chi,
    "ngu_hanh": ...,
    "name": CUC_NAMES.get(result.five_elements_class, ...).get("name", ...)
}
```

This assigns the CỤC name ("Mộc Tam Cục") to the `nap_am` field. Cục and Nạp Âm are **completely different concepts:**

| Concept | What | Source | Example (Giáp Tý) |
|---------|------|--------|-------------------|
| **Cục** (局) | Determines Đại Hạn start age in Tử Vi | Calculated from Mệnh Cung + Tử Vi star | Mộc Tam Cục (starts age 3) |
| **Nạp Âm** (納音) | Poetic five-element name for birth year | Fixed 60-entry lookup by Can-Chi year | Hải Trung Kim (海中金) |

iztro-py does NOT provide Nạp Âm. We must add a lookup table.

---

## Items

### TV-DH-1: Replace fortune_period_service with iztro-py Data (5pts) — BE

**What to do:**

1. **Delete** `fortune_period_service.py` entirely (206 lines of wrong code)

2. **In `main.py`:** Remove the import and call to `get_fortune_periods()`. Instead, build the `dai_han` array from `chart["palaces"]` which already contains correct decadal data from iztro-py:

```
dai_han = []
for p in chart["palaces"]:
    if p.get("dai_han"):
        dai_han.append({
            "start_age": p["dai_han"]["range"][0],
            "end_age": p["dai_han"]["range"][1],
            "palace_name": p["cung_name"],
            "palace_index": p["position"],
            "can_chi": p["dai_han"]["can_chi"],
            "is_current": p["dai_han"]["is_current"],
            "period": p["dai_han"]["can_chi"]  # for FE compat
        })
dai_han.sort(key=lambda x: x["start_age"])
chart["dai_han"] = dai_han
```

3. **For Tiểu Hạn:** iztro-py already provides `palace.ages` (list of ages for Tiểu Hạn). Build from that too — no custom calculation needed.

### TV-DH-2: Add Nạp Âm Lookup Table (2pts) — BE

**What to do:**

Add a `NAP_AM_TABLE` dict mapping Can-Chi year pairs to their Nạp Âm name. Then populate `chart["nap_am"]` correctly.

**The 30-entry lookup (each covers 2 years):**

```
NAP_AM_TABLE = {
    ("Giáp", "Tý"):  "Hải Trung Kim",   ("Ất", "Sửu"):  "Hải Trung Kim",
    ("Bính", "Dần"):  "Lô Trung Hỏa",   ("Đinh", "Mão"):  "Lô Trung Hỏa",
    ("Mậu", "Thìn"):  "Đại Lâm Mộc",    ("Kỷ", "Tỵ"):    "Đại Lâm Mộc",
    ("Canh", "Ngọ"):  "Lộ Bàng Thổ",    ("Tân", "Mùi"):   "Lộ Bàng Thổ",
    ("Nhâm", "Thân"): "Kiếm Phong Kim",  ("Quý", "Dậu"):   "Kiếm Phong Kim",
    ("Giáp", "Tuất"): "Sơn Đầu Hỏa",    ("Ất", "Hợi"):    "Sơn Đầu Hỏa",
    ("Bính", "Tý"):   "Giản Hạ Thủy",   ("Đinh", "Sửu"):  "Giản Hạ Thủy",
    ("Mậu", "Dần"):   "Thành Đầu Thổ",  ("Kỷ", "Mão"):    "Thành Đầu Thổ",
    ("Canh", "Thìn"): "Bạch Lạp Kim",   ("Tân", "Tỵ"):    "Bạch Lạp Kim",
    ("Nhâm", "Ngọ"):  "Dương Liễu Mộc", ("Quý", "Mùi"):   "Dương Liễu Mộc",
    ("Giáp", "Thân"): "Tuyền Trung Thủy",("Ất", "Dậu"):   "Tuyền Trung Thủy",
    ("Bính", "Tuất"): "Ốc Thượng Thổ",  ("Đinh", "Hợi"):  "Ốc Thượng Thổ",
    ("Mậu", "Tý"):   "Tích Lịch Hỏa",  ("Kỷ", "Sửu"):   "Tích Lịch Hỏa",
    ("Canh", "Dần"):  "Tùng Bách Mộc",  ("Tân", "Mão"):   "Tùng Bách Mộc",
    ("Nhâm", "Thìn"): "Trường Lưu Thủy",("Quý", "Tỵ"):   "Trường Lưu Thủy",
    ("Giáp", "Ngọ"):  "Sa Trung Kim",   ("Ất", "Mùi"):    "Sa Trung Kim",
    ("Bính", "Thân"): "Sơn Hạ Hỏa",    ("Đinh", "Dậu"):  "Sơn Hạ Hỏa",
    ("Mậu", "Tuất"): "Bình Địa Mộc",   ("Kỷ", "Hợi"):   "Bình Địa Mộc",
    ("Canh", "Tý"):  "Bích Thượng Thổ", ("Tân", "Sửu"):  "Bích Thượng Thổ",
    ("Nhâm", "Dần"): "Kim Bạch Kim",    ("Quý", "Mão"):  "Kim Bạch Kim",
    ("Giáp", "Thìn"): "Phúc Đăng Hỏa",  ("Ất", "Tỵ"):   "Phúc Đăng Hỏa",
    ("Bính", "Ngọ"):  "Thiên Hà Thủy",  ("Đinh", "Mùi"): "Thiên Hà Thủy",
    ("Mậu", "Thân"): "Đại Dịch Thổ",   ("Kỷ", "Dậu"):  "Đại Dịch Thổ",
    ("Canh", "Tuất"): "Thoa Xuyến Kim", ("Tân", "Hợi"):  "Thoa Xuyến Kim",
    ("Nhâm", "Tý"):  "Tang Triết Mộc",  ("Quý", "Sửu"): "Tang Triết Mộc",
    ("Giáp", "Dần"): "Đại Khê Thủy",   ("Ất", "Mão"):  "Đại Khê Thủy",
    ("Bính", "Thìn"): "Sa Trung Thổ",   ("Đinh", "Tỵ"): "Sa Trung Thổ",
    ("Mậu", "Ngọ"):  "Thiên Thượng Hỏa",("Kỷ", "Mùi"): "Thiên Thượng Hỏa",
    ("Canh", "Thân"): "Thạch Lựu Mộc",  ("Tân", "Dậu"): "Thạch Lựu Mộc",
    ("Nhâm", "Tuất"): "Đại Hải Thủy",   ("Quý", "Hợi"): "Đại Hải Thủy",
}
```

**How to get Can and Chi from birth year:**

```
CAN = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
year_can = CAN[(birth_year - 4) % 10]
year_chi = CHI[(birth_year - 4) % 12]
nap_am = NAP_AM_TABLE.get((year_can, year_chi), "Unknown")
```

Note: Base year is 4 (year 4 AD = Giáp Tý, the start of the 60-year cycle).

**Update `nap_am` field in chart response:**

```
"nap_am": {
    "name": nap_am_name,     # e.g., "Hải Trung Kim"
    "ngu_hanh": nap_am_element,  # e.g., "Kim" (extracted from name)
}
```

Keep Cục as its own separate field (already correct as `chart["cuc"]`).

### TV-DH-3: Regression Tests (3pts) — BE+QA

**Test cases for Đại Hạn direction:**

| # | Birth | Gender | Year Can | Polarity | Direction | Mệnh | First 3 Đại Hạn |
|---|-------|--------|----------|----------|-----------|-------|-----------------|
| 1 | 18/5/1984 | Nam | Giáp | Dương | Thuận (CW) | Tỵ | Tỵ(3-12)→Ngọ(13-22)→Mùi(23-32) |
| 2 | 18/5/1985 | Nam | Ất | Âm | Nghịch (CCW) | ? | Verify counterclockwise |
| 3 | 18/5/1984 | Nữ | Giáp | Dương | Nghịch (CCW) | Tỵ | Tỵ(3-12)→Thìn→Mão |
| 4 | 18/5/1985 | Nữ | Ất | Âm | Thuận (CW) | ? | Verify clockwise |

**Test cases for Nạp Âm:**

| # | Year | Can-Chi | Expected Nạp Âm |
|---|------|---------|-----------------|
| 1 | 1984 | Giáp Tý | Hải Trung Kim |
| 2 | 1985 | Ất Sửu | Hải Trung Kim |
| 3 | 1990 | Canh Ngọ | Lộ Bàng Thổ |
| 4 | 1993 | Quý Dậu | Kiếm Phong Kim |
| 5 | 2000 | Canh Thìn | Bạch Lạp Kim |

---

## Execution Order

1. BE: Delete fortune_period_service.py, build dai_han from iztro-py palace data
2. BE: Add NAP_AM_TABLE, fix nap_am field in chart response
3. BE: Write tests (Đại Hạn direction + Nạp Âm lookup)
4. TL: Review code + run tests
5. QA: Verify with Boss's test case (18/5/1984 Nam → Đại Hạn thuận + Nạp Âm = Hải Trung Kim)

## Acceptance Criteria

- [ ] 18/5/1984 Nam: Đại Hạn sequence Tỵ(3-12)→Ngọ(13-22)→Mùi(23-32) (thuận/clockwise)
- [ ] 18/5/1984: Nạp Âm = "Hải Trung Kim" (not "Mộc Tam Cục")
- [ ] Cục field still shows "Mộc Tam Cục" separately (not conflated)
- [ ] Dương Nam + Dương Nữ + Âm Nam + Âm Nữ all produce correct direction
- [ ] All tests passing
- [ ] fortune_period_service.py deleted (zero custom Đại Hạn calculation code)
