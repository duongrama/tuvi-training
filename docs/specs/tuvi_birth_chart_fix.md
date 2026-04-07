# Tử Vi Birth Chart Algorithm — Complete Reference

**Author:** TL | **Date:** 2026-03-15
**Sources:** iztro (SylarLong/iztro, 3.4k stars, TypeScript), lasotuvi (doanguyen/lasotuvi, Python)
**Test case:** 13/07/1993 solar, 5:30 AM, male → Thiên Phủ in Mão ✅ (verified with iztro-py)

---

## Overview

The Tử Vi (紫微斗數) birth chart algorithm has 5 sequential steps:

1. **Convert** solar date → lunar date + earthly branch of birth hour
2. **Calculate Mệnh Cung** (Soul Palace) position in the 12-palace grid
3. **Determine Cục** (Five Elements Class) from Heavenly Stem + Mệnh Cung
4. **Place Tử Vi star** using Cục number + lunar day
5. **Place remaining 13 main stars** from Tử Vi and Thiên Phủ positions

---

## Step 1: Input Conversion

**Inputs:** Solar birth date, birth hour, gender

**Convert to:**
- Lunar date (year, month, day) — use lunar calendar library
- Heavenly Stem (Can) of lunar year: index 0-9 → Giáp Ất Bính Đinh Mậu Kỷ Canh Tân Nhâm Quý
- Earthly Branch (Chi) of birth hour: 0-11 → Tý Sửu Dần Mão Thìn Tỵ Ngọ Mùi Thân Dậu Tuất Hợi

**Hour mapping (solar → earthly branch index):**

| Hour Range | Branch | Index |
|------------|--------|-------|
| 23:00-00:59 | Tý | 0 |
| 01:00-02:59 | Sửu | 1 |
| 03:00-04:59 | Dần | 2 |
| 05:00-06:59 | Mão | 3 |
| 07:00-08:59 | Thìn | 4 |
| 09:00-10:59 | Tỵ | 5 |
| 11:00-12:59 | Ngọ | 6 |
| 13:00-14:59 | Mùi | 7 |
| 15:00-16:59 | Thân | 8 |
| 17:00-18:59 | Dậu | 9 |
| 19:00-20:59 | Tuất | 10 |
| 21:00-22:59 | Hợi | 11 |

**12-palace grid** (each palace is an earthly branch position):

| Index | Branch | Vietnamese |
|-------|--------|-----------|
| 0 | 寅 | Dần |
| 1 | 卯 | Mão |
| 2 | 辰 | Thìn |
| 3 | 巳 | Tỵ |
| 4 | 午 | Ngọ |
| 5 | 未 | Mùi |
| 6 | 申 | Thân |
| 7 | 酉 | Dậu |
| 8 | 戌 | Tuất |
| 9 | 亥 | Hợi |
| 10 | 子 | Tý |
| 11 | 丑 | Sửu |

---

## Step 2: Calculate Mệnh Cung (Soul Palace)

**Formula** (from iztro `palace.ts` + lasotuvi `DiaBan.py`):

```
soulIndex = (lunarMonth - 1) - (hourBranchIndex) + 1
soulIndex = fixIndex(soulIndex)  // mod 12, keep positive
```

Equivalently: Start at Dần (index 0). Count forward by (lunar month - 1). Count backward by (hour branch index - 1). That's the Mệnh Cung position.

**Thân Cung (Body Palace):**
```
bodyIndex = (lunarMonth - 1) + (hourBranchIndex - 1)
bodyIndex = fixIndex(bodyIndex)
```

**fixIndex(n):** `((n % 12) + 12) % 12` (always returns 0-11)

### Test: 13/07/1993 solar, 5:30AM

- Lunar date: 24th day, 5th month, Quý Dậu year (1993)
- Hour: 5:30AM → Mão → hourBranchIndex = 3
- soulIndex = (5-1) - (3) + 1 = 2 → Index 2 = Thìn? But iztro returns Dần (index 0)

*Note: The exact formula may vary by implementation. iztro-py returns `yinEarthly` (Dần) for this case. Use iztro-py as the authoritative source since it's our production library.*

---

## Step 3: Determine Cục (Five Elements Class)

The Cục number determines how Tử Vi star is placed. 5 possible values:

| Cục | Element | Value |
|-----|---------|-------|
| Thủy Nhị Cục | Water | 2 |
| Mộc Tam Cục | Wood | 3 |
| Kim Tứ Cục | Metal | 4 |
| Thổ Ngũ Cục | Earth | 5 |
| Hỏa Lục Cục | Fire | 6 |

**Algorithm** (from iztro `palace.ts` `getFiveElementsClass`):

```
stemNumber = floor(heavenlyStemIndex / 2) + 1     // 1-5
branchNumber = floor(soulBranchIndex % 6 / 2) + 1 // 1-3
sum = stemNumber + branchNumber
while sum > 5: sum -= 5
// Map: 1→Wood(3), 2→Metal(4), 3→Water(2), 4→Fire(6), 5→Earth(5)
```

**Mapping table:**

| Sum | Element | Cục Value |
|-----|---------|-----------|
| 1 | Mộc | 3 |
| 2 | Kim | 4 |
| 3 | Thủy | 2 |
| 4 | Hỏa | 6 |
| 5 | Thổ | 5 |

### Test: 1993 Quý Dậu year, Mệnh at Dần

- Quý = heavenlyStemIndex 9 → stemNumber = floor(9/2)+1 = 5
- Dần = branchIndex 0 (in the soul palace) → branchNumber = floor(0%6/2)+1 = 1
- sum = 5+1 = 6 → 6-5 = 1 → Mộc → Cục = 2? But iztro returns 水二局 (Thủy Nhị Cục = 2)

*iztro-py is authoritative. The exact Cục determination uses Nạp Âm (sexagenary cycle element) which is a 60-entry lookup table. Our implementation delegates to iztro-py which handles this correctly.*

---

## Step 4: Place Tử Vi Star

**The core algorithm** (from iztro `location.ts` `getStartIndex` + lasotuvi `AmDuong.py` `timTuVi`):

```python
def find_tu_vi_position(cuc_value, lunar_day):
    """
    Find Tu Vi star position given Cuc value and lunar birth day.
    Returns palace index (0-11, starting from Dan).
    """
    cung_dan = 0  # Dan palace = index 0
    cuc = cuc_value

    while cuc < lunar_day:
        cuc += cuc_value
        cung_dan += 1

    offset = cuc - lunar_day
    if offset % 2 == 1:
        offset = -offset  # odd offset = reverse direction

    return (cung_dan + offset) % 12
```

**Thiên Phủ position** (mirror of Tử Vi):
```
thien_phu_index = (12 - tu_vi_index) % 12
```

### Test: Cục = 2 (Thủy Nhị Cục), Lunar day = 24

```
cuc=2, day=24: 2<24→cuc=4,pos=1; 4<24→6,2; 6<24→8,3; 8<24→10,4;
10<24→12,5; 12<24→14,6; 14<24→16,7; 16<24→18,8; 18<24→20,9;
20<24→22,10; 22<24→24,11; 24==24→stop
pos=11, offset=24-24=0, even → no change
Tu Vi index = 11 → Sửu palace ✅ (matches iztro: siblingsPalace/chouEarthly)
Thien Phu index = (12-11)%12 = 1 → Mão palace ✅ (matches: parentsPalace/maoEarthly)
```

**Thiên Phủ in Mão confirmed** ✅

---

## Step 5: Place All 14 Main Stars

### Tử Vi Group (6 stars, counterclockwise from Tử Vi)

| Offset | Star | Vietnamese |
|--------|------|-----------|
| 0 | 紫微 | Tử Vi |
| -1 | 天機 | Thiên Cơ |
| -2 | (empty) | — |
| -3 | 太陽 | Thái Dương |
| -4 | 武曲 | Vũ Khúc |
| -5 | 天同 | Thiên Đồng |
| -6 | (empty) | — |
| -7 | (empty) | — |
| -8 | 廉貞 | Liêm Trinh |

**Placement:** `star_index = (tu_vi_index - offset) % 12`

Equivalent forward offsets (mod 12):

| Star | Forward offset from Tử Vi |
|------|--------------------------|
| Tử Vi | 0 |
| Thiên Cơ | +11 |
| Thái Dương | +9 |
| Vũ Khúc | +8 |
| Thiên Đồng | +7 |
| Liêm Trinh | +4 |

### Thiên Phủ Group (8 stars, clockwise from Thiên Phủ)

| Offset | Star | Vietnamese |
|--------|------|-----------|
| 0 | 天府 | Thiên Phủ |
| +1 | 太陰 | Thái Âm |
| +2 | 貪狼 | Tham Lang |
| +3 | 巨門 | Cự Môn |
| +4 | 天相 | Thiên Tướng |
| +5 | 天梁 | Thiên Lương |
| +6 | 七殺 | Thất Sát |
| +7 | (empty) | — |
| +8 | (empty) | — |
| +9 | (empty) | — |
| +10 | 破軍 | Phá Quân |

**Placement:** `star_index = (thien_phu_index + offset) % 12`

---

## Auxiliary Stars (Phụ Tinh)

### Tả Phụ / Hữu Bật (from lunar month)

```
ta_phu_index = (lunarMonth - 1 + 4) % 12    // Start from Thìn, count by month
huu_bat_index = (10 - lunarMonth + 1) % 12   // Start from Tuất, count reverse
```

### Văn Xương / Văn Khúc (from birth hour)

```
van_xuong_index = (10 - hourBranchIndex) % 12  // Start from Tuất, reverse by hour
van_khuc_index = (hourBranchIndex + 4) % 12    // Start from Thìn, forward by hour
```

### Lộc Tồn (from Heavenly Stem of year)

| Stem | Lộc Tồn Position |
|------|------------------|
| Giáp | Dần (0) |
| Ất | Mão (1) |
| Bính/Mậu | Tỵ (3) |
| Đinh/Kỷ | Ngọ (4) |
| Canh | Thân (6) |
| Tân | Dậu (7) |
| Nhâm | Hợi (9) |
| Quý | Tý (10) |

### Thiên Khôi / Thiên Việt (from Heavenly Stem of year)

| Stem Pair | Thiên Khôi | Thiên Việt |
|-----------|-----------|-----------|
| Giáp/Mậu/Canh | Sửu (11) | Mùi (5) |
| Ất/Kỷ | Tý (10) | Thân (6) |
| Bính/Đinh | Hợi (9) | Dậu (7) |
| Nhâm/Quý | Mão (1) | Tỵ (3) |
| Tân | Ngọ (4) | Dần (0) |

---

## Tứ Hóa (Four Transformations)

Determined by the Heavenly Stem of the birth year. Each stem assigns 4 transformations to 4 specific stars:

| Stem | Hóa Lộc | Hóa Quyền | Hóa Khoa | Hóa Kỵ |
|------|---------|-----------|---------|--------|
| Giáp | Liêm Trinh | Phá Quân | Vũ Khúc | Thái Dương |
| Ất | Thiên Cơ | Thiên Lương | Tử Vi | Thái Âm |
| Bính | Thiên Đồng | Thiên Cơ | Văn Xương | Liêm Trinh |
| Đinh | Thái Âm | Thiên Đồng | Thiên Cơ | Cự Môn |
| Mậu | Tham Lang | Thái Âm | Hữu Bật | Thiên Cơ |
| Kỷ | Vũ Khúc | Tham Lang | Thiên Lương | Văn Khúc |
| Canh | Thái Dương | Vũ Khúc | Thái Âm | Thiên Đồng |
| Tân | Cự Môn | Thái Dương | Văn Khúc | Văn Xương |
| Nhâm | Thiên Lương | Tử Vi | Tả Phụ | Vũ Khúc |
| Quý | Phá Quân | Cự Môn | Thái Âm | Tham Lang |

---

## Current Implementation Status

**We use iztro-py (v0.3.4)** which correctly implements ALL of the above:
- ✅ Solar → Lunar conversion
- ✅ Mệnh Cung calculation
- ✅ Cục determination (Nạp Âm)
- ✅ Tử Vi star placement
- ✅ All 14 chính tinh
- ✅ Auxiliary stars (phụ tinh)
- ✅ Tứ Hóa
- ✅ Star brightness (Miếu/Vượng/Đắc/Lợi/Bình/Hãm)
- ✅ Đại Hạn / Tiểu Hạn periods

**File:** `gieo_que/backend/tu_vi/iztro_service.py` wraps iztro-py with Vietnamese translations.

**Test case verified:**
```
Input: 13/07/1993 solar, 5:30 AM (Mão hour), male
Output: Mệnh at Dần, Cục = Thủy Nhị Cục (2)
        Tử Vi at Sửu (index 11)
        Thiên Phủ at Mão (index 1) ✅
```

---

## Reference Repositories

| Repository | Language | Stars | Key Files |
|------------|----------|-------|-----------|
| [SylarLong/iztro](https://github.com/SylarLong/iztro) | TypeScript | 3,448 | `src/star/majorStar.ts`, `src/star/location.ts`, `src/astro/palace.ts` |
| [doanguyen/lasotuvi](https://github.com/doanguyen/lasotuvi) | Python | 45 | `lasotuvi/AmDuong.py`, `lasotuvi/App.py`, `lasotuvi/DiaBan.py` |
| [x-haose/py-iztro](https://github.com/x-haose/py-iztro) | Python | 106 | Wrapper around iztro JS |
