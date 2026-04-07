# Lá Số Tử Vi — Deep Research (Synthesized from EN/VI/ZH sources)

**Date:** 2026-03-16 | **Author:** PO
**Purpose:** Technical spec for Tu Vi chart overhaul — from basic (28 stars) to professional-grade (~110 stars)
**Source research:** `./en/`, `./vi/`, `./zh/` subdirectories

---

## 1. Current State vs Target

### What We Have (iztro-py provides)
- 14 main stars (Chính Tinh) ✅
- 14 auxiliary stars (6 auspicious + 6 inauspicious + Lộc Tồn + Thiên Mã) ✅
- Brightness (Miếu/Vượng/Đắc/Bình/Hãm) for main stars ✅
- Tứ Hóa at API level ✅
- Can Chi per palace (in dai_han.can_chi) ✅
- **Total: 28 stars**

### What's Missing (from Boss feedback + competitor analysis)
- ~80 more auxiliary stars (Vòng Tràng Sinh, Vòng Thái Tuế, etc.)
- Tuần & Triệt markers
- Mệnh Chủ / Thân Chủ stars
- Can Chi displayed per palace cell
- Tứ Hóa markers on individual stars
- Hover/popup detail for each palace
- Tiểu Hạn & Lưu Niên display
- Palace scoring system (optional, low priority)
- Brightness for ALL stars (not just main)

---

## 2. Complete Star Catalog (~108-120 stars)

### Grade A — 28 Stars (Most Important, ALREADY IMPLEMENTED)

#### 14 Chính Tinh (Main Stars)
Tử Vi系: Tử Vi, Thiên Cơ, Thái Dương, Vũ Khúc, Thiên Đồng, Liêm Trinh
Thiên Phủ系: Thiên Phủ, Thái Âm, Tham Lang, Cự Môn, Thiên Tướng, Thiên Lương, Thất Sát, Phá Quân

#### 6 Cát Tinh (Auspicious)
Tả Phụ, Hữu Bật, Văn Xương, Văn Khúc, Thiên Khôi, Thiên Việt

#### 6 Hung Tinh (Inauspicious)
Kình Dương, Đà La, Hỏa Tinh, Linh Tinh, Địa Không, Địa Kiếp

#### 2 Key Stars
Lộc Tồn, Thiên Mã

### Grade B — ~29 Stars (NEED TO IMPLEMENT)

#### Vòng Tràng Sinh (12 stages — placed from Cục element + Mệnh position)
Trường Sinh, Mộc Dục, Quan Đới, Lâm Quan, Đế Vượng, Suy, Bệnh, Tử, Mộ, Tuyệt, Thai, Dưỡng

**Placement rule:** Starting position depends on Cục (五行局):
- Thủy Nhị Cục → start from Thân (clockwise for Dương, counter for Âm)
- Mộc Tam Cục → start from Hợi
- Kim Tứ Cục → start from Tỵ
- Thổ Ngũ Cục → start from Thân
- Hỏa Lục Cục → start from Dần

#### Vòng Lộc Tồn (Bác Sĩ ring — 12 stars from Lộc Tồn position)
Bác Sĩ, Lực Sĩ, Thanh Long, Tiểu Hao, Tướng Quân, Tấu Thư, Phi Liêm, Hỉ Thần, Bệnh Phù, Đại Hao, Phục Binh, Quan Phù

**Placement rule:** Start from Lộc Tồn position, go clockwise for Dương Nam/Âm Nữ, counter for Âm Nam/Dương Nữ.

#### 5 Additional Important Stars
Thiên Quan, Thiên Phúc, Thiên Trù (kitchen god), Thiên Đức, Nguyệt Đức

### Grade C — ~36 Stars (Three groups of 12)

#### Vòng Thái Tuế (12 stars — placed from birth year branch)
Thái Tuế, Thiếu Dương, Tang Môn, Thiếu Âm, Quan Phủ, Tử Phủ, Tuế Phá, Long Đức, Bạch Hổ, Phúc Đức, Điếu Khách, Trực Phù/Bệnh Phù

**Placement rule:** Thái Tuế placed at birth year's Địa Chi, then go clockwise through all 12.

#### Vòng Tứ Hóa derived stars (Hồng Loan ring — 12 stars)
Hồng Loan, Thiên Hỉ, Thiên Hình, Thiên Diêu, Thiên Y, Thiên Thọ, etc.
Hồng Loan at (Mão - birth year branch) position, Thiên Hỉ opposite.

#### Miscellaneous Grade C
Thiên Không, Đào Hoa, Hoa Cái, Thai Phụ, Phong Cáo, Giải Thần, etc.
Ân Quang, Thiên Quý, Tam Thai, Bát Tọa, etc.

### Special: Tuần and Triệt (截路空亡)

**Tuần (旬空):** Based on Can Chi of birth day — identifies which 2 Địa Chi are "empty". Stars in these palaces are weakened.

**Triệt (截路):** Based on birth year's Thiên Can pair — identifies 2 palaces with "path interruption". Stars in these palaces lose some power.

**Display:** Mark affected palaces with 旬 or 截 symbol.

---

## 3. Mệnh Chủ and Thân Chủ

### Mệnh Chủ (Life Master Star)
Determined by the Địa Chi of Cung Mệnh:

| Mệnh position | Mệnh Chủ |
|---------------|----------|
| Tý | Tham Lang |
| Sửu | Cự Môn |
| Dần | Lộc Tồn |
| Mão | Văn Khúc |
| Thìn | Liêm Trinh |
| Tỵ | Vũ Khúc |
| Ngọ | Phá Quân |
| Mùi | Vũ Khúc |
| Thân | Liêm Trinh |
| Dậu | Văn Khúc |
| Tuất | Lộc Tồn |
| Hợi | Cự Môn |

### Thân Chủ (Body Master Star)
Determined by the birth year's Địa Chi:

| Birth year branch | Thân Chủ |
|------------------|----------|
| Tý, Ngọ | Hỏa Tinh |
| Sửu, Mùi | Thiên Tướng |
| Dần, Thân | Thiên Lương |
| Mão, Dậu | Thiên Đồng |
| Thìn, Tuất | Văn Xương |
| Tỵ, Hợi | Thiên Cơ |

**Display in center panel:** "Mệnh chủ: [star] | Thân chủ: [star]"

---

## 4. Can Chi Per Palace

Each palace has its own Heavenly Stem (Thiên Can), determined by the Thiên Can of Cung Mệnh's position. This is calculated using the 五虎遁 (Five Tiger Escape) formula:

| Birth year stem | 寅 palace stem |
|----------------|---------------|
| Giáp, Kỷ | Bính |
| Ất, Canh | Mậu |
| Bính, Tân | Canh |
| Đinh, Nhâm | Nhâm |
| Mậu, Quý | Giáp |

From the stem at Dần, proceed clockwise: Dần→Mão→Thìn→... assigning stems in order.

**Display:** Each palace cell shows "Ất Mão", "Bính Thìn", etc. — NOT just "Mão", "Thìn".

---

## 5. Tứ Hóa Complete Table

| Thiên Can | Hóa Lộc | Hóa Quyền | Hóa Khoa | Hóa Kỵ |
|-----------|---------|-----------|---------|--------|
| Giáp | Liêm Trinh | Phá Quân | Vũ Khúc | Thái Dương |
| Ất | Thiên Cơ | Thiên Lương | Tử Vi | Thái Âm |
| Bính | Thiên Đồng | Thiên Cơ | Văn Xương | Liêm Trinh |
| Đinh | Thái Âm | Thiên Đồng | Thiên Cơ | Cự Môn |
| Mậu | Tham Lang | Thái Âm | Hữu Bật | Thiên Cơ |
| Kỷ | Vũ Khúc | Tham Lang | Thiên Lương | Văn Khúc |
| Canh | Thái Dương | Vũ Khúc | Thiên Phủ | Thiên Đồng |
| Tân | Cự Môn | Thái Dương | Văn Khúc | Văn Xương |
| Nhâm | Thiên Lương | Tử Vi | Tả Phụ | Vũ Khúc |
| Quý | Phá Quân | Cự Môn | Thái Âm | Tham Lang |

**Display per star:** Stars with Tứ Hóa should show colored dot:
- Lộc = green dot (Lộc)
- Quyền = red dot (Quyền)
- Khoa = blue dot (Khoa)
- Kỵ = dark dot (Kỵ)

---

## 6. Đại Hạn Age Calculation

### Starting age
The starting age equals the Cục number:
- Thủy Nhị Cục: starts at age **2**
- Mộc Tam Cục: starts at age **3**
- Kim Tứ Cục: starts at age **4**
- Thổ Ngũ Cục: starts at age **5**
- Hỏa Lục Cục: starts at age **6**

Each Đại Hạn spans 10 years.

### Direction
- Dương Nam or Âm Nữ → THUẬN (clockwise)
- Âm Nam or Dương Nữ → NGHỊCH (counter-clockwise)

### Age type
Vietnamese tradition uses **tuổi ta** (add 1 to Western age). TinhMenhDo uses tuổi ta. Our app should too.

### Competitor note
TinhMenhDo shows: "3-12", "13-22", etc. (Cục value based). Some apps show "2-11" for Thủy Nhị Cục. Need to verify which is standard.

---

## 7. Tiểu Hạn & Lưu Niên

### Tiểu Hạn (Annual Minor Cycle)
Determined by birth year Địa Chi + current age. Each year, a different palace becomes the Tiểu Hạn palace.

### Lưu Niên (Yearly Star Overlay)
In a given year, additional stars are overlaid based on that year's Can Chi:
- Lưu Niên Tứ Hóa (use the year's Thiên Can → Tứ Hóa table)
- Lưu Niên Thái Tuế ring rotates
- Additional flow-year stars

**Display:** Show "Tiểu Hạn 2026: [Palace]" and optionally overlay yearly stars.

---

## 8. UI Requirements (from Boss + Competitor Feedback)

### 8.1 Palace Cell — Must Show
1. **Địa Chi + Cung name** (e.g., "Mão — Mệnh")
2. **Can Chi** (e.g., "Ất Mão") — currently missing
3. **Main stars** with brightness superscript (Liêm Trinh^M, Tham Lang^V)
4. **Auxiliary stars** (smaller text below main stars)
5. **Tứ Hóa dots** on stars that have them (colored circles)
6. **Tuần/Triệt markers** if this palace is affected
7. **Đại Hạn range** (e.g., "3-12")

### 8.2 Hover/Popup Detail (NEW)
When user hovers/clicks a palace cell, show popup with:
- Full list of ALL stars in this palace with brightness
- Star meanings and interpretations
- Đại Hạn analysis for this period
- Tiểu Hạn years that fall in this palace
- Tứ Hóa effects
- Vòng Tràng Sinh position for this palace

### 8.3 Center Panel — Must Show
- Dương/Âm date
- Nạp Âm (birth year)
- Cục
- 命 Mệnh position + 身 Thân position
- **Mệnh Chủ:** [star name]
- **Thân Chủ:** [star name]
- **Tứ Hóa summary:** Lộc→[star], Quyền→[star], Khoa→[star], Kỵ→[star]
- Năm xem (current year) info

### 8.4 Timeline
- Đại Hạn timeline (existing, fix age format)
- **Tiểu Hạn** year labels
- Current year highlighted

---

## 9. Implementation Priority

### Phase 1 — Data Completeness (P0, immediate)
1. **Add ~80 missing stars** (backend): Implement placement algorithms for:
   - Vòng Tràng Sinh (12 stars) — most important missing ring
   - Vòng Bác Sĩ/Lộc Tồn (12 stars)
   - Vòng Thái Tuế (12 stars)
   - Remaining Grade B stars (~17)
   - Grade C stars (~36)
   - Tuần/Triệt calculation
2. **Add Mệnh Chủ / Thân Chủ** to API response
3. **Add Can Chi per palace** to API response (not just in dai_han)

### Phase 2 — Frontend Display (P0, after Phase 1)
1. **Show Can Chi** in each palace cell
2. **Show ALL stars** (not just main + a few auxiliary)
3. **Tứ Hóa colored dots** on affected stars
4. **Tuần/Triệt markers** on affected palaces
5. **Hover/popup** with full palace detail
6. **Center panel** with Mệnh Chủ, Thân Chủ, full Tứ Hóa

### Phase 3 — Polish (P1)
1. Tiểu Hạn & Lưu Niên display
2. Palace scoring system
3. Brightness table for ALL auxiliary stars
4. Print/export lá số as image

---

## 10. Technical Decision: py-iztro Already Has 114 Stars!

**UPDATE (2026-03-16):** Investigation found py-iztro already provides 114 stars. We only extract 28.

**Hidden attributes per palace:**
- `adjective_stars` — ~37 miscellaneous stars (Hồng Loan, Đào Hoa, etc.)
- `changsheng12` — Vòng Tràng Sinh value
- `boshi12` — Vòng Bác Sĩ value
- `jiangqian12` — Vòng Tướng Tiền value
- `suiqian12` — Vòng Thái Tuế value
- `heavenly_stem` — Palace Thiên Can

**Fix:** Update `iztro_service.py` to extract ALL data. No new library or custom algorithms needed.

See also: `./libraries.md` for full library audit.

## 11. UX Strategy: Progressive Disclosure (Boss Directive)

**Problem:** 114 stars in 12 cells = cluttered, ugly, overwhelming for casual users.
**Solution:** 3-layer progressive disclosure:

1. **Basic View (default):** 14 main stars + brightness + Tứ Hóa dots. Clean, beautiful.
2. **Hover/Popup (on demand):** Tap/hover a cell → detailed popup with ALL stars, rings, meanings.
3. **Professional View (toggle):** "Xem Chuyên Sâu" button → TinhMenhDo-level full display.

**Principle:** Information appears when user WANTS it. Don't dump 114 stars on first load.

---

## Sources
- `./zh/research_zh.md` — Chinese 紫微斗数 sources (661 lines, most authoritative)
- `./vi/research_vi.md` — Vietnamese Tử Vi sources (663 lines, localized conventions)
- Boss feedback + competitor review (TinhMenhDo comparison)
- iztro-py library audit (28 stars confirmed)
