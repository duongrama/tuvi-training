# Tử Vi (紫微斗數) An Sao Algorithm - Technical Research Report

**Date:** 2026-03-13
**Purpose:** Technical reference for Sprint 11 TV-P0-3 (An Sao 14 Chính Tinh) implementation
**For:** TL, BE developers

---

## Overview

Vietnamese Tử Vi (紫微斗數 / Zi Wei Dou Shu / Purple Star Astrology) is a traditional Chinese-origin astrology system adapted for Vietnamese practice. It uses NO LLM — all calculations are pure traditional math/lookup tables. This report covers the algorithmic details needed for software implementation.

---

## 1. Input Data Required

| Input | Format | Source |
|-------|--------|--------|
| Birth year | Solar → Lunar conversion | User input |
| Birth month | Lunar month (1-12) | Lunar calendar |
| Birth day | Lunar day (1-30) | Lunar calendar |
| Birth hour | 2-hour Địa Chi blocks (Tý=23-01, Sửu=01-03, etc.) | User input |
| Gender | Male/Female | User input |
| Is leap month | Boolean | Lunar calendar |

---

## 2. Calculation Pipeline

```
Solar Date → Lunar Date → Can Chi (Year/Month/Day/Hour)
                                ↓
                        Cung Mệnh (from lunar month + hour)
                                ↓
                        Cục (from Cung Mệnh + year Thiên Can)
                                ↓
                        Tử Vi position (from birth day + Cục number)
                                ↓
                        14 Chính Tinh placement (from Tử Vi + Thiên Phủ positions)
                                ↓
                        Phụ Tinh placement (from year Can/Chi, month, hour)
                                ↓
                        Tứ Hóa transformations (from year Thiên Can)
```

---

## 3. Step 1: Cung Mệnh (Destiny Palace) Calculation

**Formula:** Count from Dần (month 1) forward by birth month, then backward by birth hour.

```
Cung Mệnh position = (month_index - hour_index) mod 12

where:
  month_index: Dần=0, Mão=1, Thìn=2, ..., Sửu=11
  hour_index:  Tý=0, Sửu=1, Dần=2, ..., Hợi=11
```

Alternative formula from Vietnamese sources:
```
Cung Mệnh = 26 - (Địa Chi Tháng + Địa Chi Giờ)  (mod 12)
```

> Source: [Hoc Vien Ly So](https://hocvienlyso.org/tu-hoc-tu-vi-dau-bai-6-lap-cuc.html)

**12 Palace Names (counter-clockwise from Mệnh):**
1. Mệnh (Destiny)
2. Huynh Đệ (Siblings) — or Phụ Mẫu depending on school
3. Phu Thê (Spouse)
4. Tử Tức (Children)
5. Tài Bạch (Wealth)
6. Tật Ách (Health)
7. Thiên Di (Travel)
8. Nô Bộc (Servants)
9. Quan Lộc (Career)
10. Điền Trạch (Property)
11. Phúc Đức (Fortune)
12. Phụ Mẫu (Parents)

**Cung Thân (Body Palace):**
Count forward from Tý by birth month, then forward again by birth hour.
Constraint: Must fall in one of 6 palaces: Mệnh, Thiên Di, Phu Thê, Phúc Đức, Tài Bạch, or Quan Lộc.

---

## 4. Step 2: Cục (Element Group) Determination

**5 Cục Types:**

| Cục | Element | Number |
|-----|---------|--------|
| Thủy Nhị Cục | Water | 2 |
| Mộc Tam Cục | Wood | 3 |
| Kim Tứ Cục | Metal | 4 |
| Thổ Ngũ Cục | Earth | 5 |
| Hỏa Lục Cục | Fire | 6 |

**Determination:** Cross-reference table of Year's Thiên Can (10 stems) x Cung Mệnh position (12 branches).

The Cục number is critical — it determines Tử Vi star's position.

> Source: [Hoc Vien Ly So - Lap Cuc](https://hocvienlyso.org/tu-hoc-tu-vi-dau-bai-6-lap-cuc.html)

---

## 5. Step 3: Tử Vi Star Position

**Formula:** Tử Vi position = f(birth_day, Cục_number)

The position is determined by a lookup table indexed by (birth_day, Cục):
- For each Cục number (2,3,4,5,6), there's a mapping from birth day (1-30) to palace position (0-11)
- The general pattern: `position = (birth_day + Cục_number) mod 12` with adjustments

This is the most complex lookup — traditionally encoded in verse form. The doanguyen/lasotuvi Python library and our existing `tuvi_tables.py` contain these tables.

---

## 6. Step 4: 14 Chính Tinh (Main Stars) Placement

### Tử Vi Group (Bắc Đẩu - North Dipper, 6 stars)

Placed relative to Tử Vi's position. The offsets are NOT uniform — they follow a specific pattern:

| Star | Placement Rule |
|------|---------------|
| **Tử Vi** (紫微) | Base position (calculated from Step 3) |
| **Thiên Cơ** (天機) | -1 from Tử Vi (counter-clockwise) |
| **Thái Dương** (太陽) | -3 from Tử Vi |
| **Vũ Khúc** (武曲) | -4 from Tử Vi |
| **Thiên Đồng** (天同) | -5 from Tử Vi |
| **Liêm Trinh** (廉貞) | +4 from Tử Vi (or -8, equivalent in mod 12) |

> Note: These offsets are approximate. The exact offsets depend on the Tử Vi position and follow a non-linear pattern. Consult the lookup tables in tuvi_tables.py for exact values.

### Thiên Phủ Group (Nam Đẩu - South Dipper, 8 stars)

**Mirror Rule:** Thiên Phủ's position mirrors Tử Vi across an axis. When Tử Vi is at position X, Thiên Phủ is at position (12 - X + 2*anchor) mod 12.

Placed clockwise from Thiên Phủ's position:

| Star | Offset from Thiên Phủ |
|------|----------------------|
| **Thiên Phủ** (天府) | Base (mirror of Tử Vi) |
| **Thái Âm** (太陰) | +1 (clockwise) |
| **Tham Lang** (貪狼) | +2 |
| **Cự Môn** (巨門) | +3 |
| **Thiên Tướng** (天相) | +4 |
| **Thiên Lương** (天梁) | +5 |
| **Thất Sát** (七殺) | +6 |
| **Phá Quân** (破軍) | +8 |

> Source: [Hoc Vien Ly So - Bai 7](https://hocvienlyso.org/tu-hoc-tu-vi-dau-so-sao-tu-vi.html), [Tuvi Saigon - Bai 8](https://tuvisaigon.vn/tu-hoc-tu-vi-dau-bai-8-chom-sao-thien-phu.html)

### Star Brightness (Miếu/Vượng/Đắc Địa/Bình Hòa/Hãm)

Each star has different brightness levels depending on which palace it lands in:

| Level | Vietnamese | Meaning |
|-------|-----------|---------|
| Miếu | 廟 | Exalted (strongest) |
| Vượng | 旺 | Prosperous |
| Đắc Địa | 得地 | Good position |
| Bình Hòa | 平和 | Neutral |
| Hãm | 陷 | Weakened (worst) |

These are stored as a 14x12 lookup table (14 stars x 12 palaces).

---

## 7. Step 5: Phụ Tinh (Auxiliary Stars)

### Lục Cát (6 Benefic Stars)

| Star | Depends On | Placement |
|------|-----------|-----------|
| Tả Phụ | Birth month | Lookup table |
| Hữu Bật | Birth month | Lookup table |
| Văn Xương | Birth hour | Lookup table |
| Văn Khúc | Birth hour | Lookup table |
| Thiên Khôi | Year Thiên Can | Lookup table |
| Thiên Việt | Year Thiên Can | Lookup table |

### Lục Sát (6 Malefic Stars)

| Star | Depends On | Placement |
|------|-----------|-----------|
| Kình Dương | Year Thiên Can | 1 palace before Lộc Tồn |
| Đà La | Year Thiên Can | 1 palace after Lộc Tồn |
| Hỏa Tinh | Year Địa Chi + birth hour | Lookup table |
| Linh Tinh | Year Địa Chi + birth hour | Lookup table |
| Địa Không | Birth hour | Lookup table |
| Địa Kiếp | Birth hour | Lookup table |

### Tứ Hóa (4 Transformation Stars)

Determined ONLY by Year's Thiên Can. Each transforms a main star:

| Thiên Can | Hóa Lộc | Hóa Quyền | Hóa Khoa | Hóa Kỵ |
|-----------|---------|-----------|---------|--------|
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

> Source: [Tracuu Tu Vi](https://tracuutuvi.com/tu-hoa.html)

---

## 8. Reference Implementations

### doanguyen/lasotuvi (Python, MIT License)
- **GitHub:** https://github.com/doanguyen/lasotuvi
- **Stars:** 45, Forks: 63
- **Status:** Stable v1.0 (Dec 2016), not actively maintained
- **Install:** `pip install lasotuvi`
- **Usage:** `lasotuvi.calc_laso(year, month, day, hour, gender)`
- **Files:** Sao.py (stars), ThienBan.py (chart), AmDuong.py (lunar), DiaBan.py (geography)

### SylarLong/iztro (TypeScript, MIT License) - RECOMMENDED
- **GitHub:** https://github.com/SylarLong/iztro
- **Stars:** 3,400+, actively maintained (v2.3.0+)
- **Features:** 12-palace charts, 4 Pillars, multi-level fortune, 6-language support (including Vietnamese)
- **Quality:** Production-grade, plugin architecture for school variations
- **Best for:** Modern reference, comprehensive test cases, multi-language support

### Our Existing Implementation
- **Location:** `/home/hungson175/dev/teams/boitoan_mvps/gieo_que/backend/tu_vi/`
- **Files:** `tuvi_tables.py`, `cung_service.py`, `lunar_service.py`, `main.py`
- **Port:** 17070
- **Status:** TV-P0-1 (lunar) and TV-P0-2 (12 Cung) complete. TV-P0-3 (An Sao) in progress.

---

## 9. Implementation Recommendations

1. **Use iztro as primary reference** for algorithm verification (3.4k stars, well-tested)
2. **Keep doanguyen/lasotuvi as secondary reference** (Python, easier to read)
3. **Validate against known charts** — use online Tử Vi calculators to verify output
4. **Start with 14 Chính Tinh only** (Sprint 11 scope), add Phụ Tinh in later sprint
5. **Store all lookup tables as Python dicts/arrays** — no formula derivation needed
6. **Test with known birthdates** — e.g., 1990-05-15 08:00 Male (already tested in TV-P0-1/P0-2)

---

## Sources

- [Hoc Vien Ly So - 14 Chinh Tinh](https://hocvienlyso.org/14-chinh-tinh.html)
- [Hoc Vien Ly So - Lap Cuc](https://hocvienlyso.org/tu-hoc-tu-vi-dau-bai-6-lap-cuc.html)
- [Hoc Vien Ly So - Sao Tu Vi](https://hocvienlyso.org/tu-hoc-tu-vi-dau-so-sao-tu-vi.html)
- [Tuvi Saigon - Thien Phu Group](https://tuvisaigon.vn/tu-hoc-tu-vi-dau-bai-8-chom-sao-thien-phu.html)
- [Tracuu Tu Vi - Tu Hoa](https://tracuutuvi.com/tu-hoa.html)
- [Tracuu Tu Vi - Luc Sat](https://tracuutuvi.com/luc-sat-tinh.html)
- [HOROS - Major Stars](https://horos.vn/major-stars)
- [Kim Ca - Tu Vi Thien Phu Mirror](https://www.kimca.net/2017/05/1.html)
- [GitHub - doanguyen/lasotuvi](https://github.com/doanguyen/lasotuvi)
- [GitHub - SylarLong/iztro](https://github.com/SylarLong/iztro)
- [AstroFate Wiki - Zi Wei Dou Shu](https://www.astrofate.wiki/en/docs/an-ming-shen-gong-jue)
