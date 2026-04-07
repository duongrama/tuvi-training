# Sprint 50: Tu Vi Frontend UX — TL Tech Spec for FE

**Author:** TL | **Date:** 2026-03-16 | **Total:** 13pts
**Constraint:** Plain CSS only — Tu Vi has NO Tailwind. All styles via CSS variables + explicit properties.

---

## TVF-1: Palace Detail Popup (5pts)

### Current State
- `openDetailPanel(palace)` exists — desktop shows side panel, mobile shows bottom sheet
- `buildDetailHTML(palace)` renders main stars + aux stars + Đại Hạn note
- Only shows stars from `palace.stars` (major + minor = 28 total)

### Changes Needed

**Extend `buildDetailHTML()` to render ALL new data:**

1. **Header:** Show Can Chi + Cung Name + Đại Hạn range
   - Format: `"Kỷ Tỵ · Mệnh · Đại Hạn 3-12 tuổi"`
   - Data: `palace.can_chi`, `palace.cung_name`, `palace.dai_han.range`

2. **Main Stars section** (existing — enhance with Tứ Hóa dots)
   - Already renders. Just ensure Tứ Hóa dot appears (see TVF-3).

3. **NEW: Adjective Stars section** (after aux stars)
   - Render from `palace.adjective_stars` array
   - Format: chip/tag layout (same as aux stars pattern)
   - Each chip: star name, optional brightness badge

4. **NEW: Star Rings section**
   - 4 ring values displayed as labeled pairs
   - Layout: 2×2 grid of label+value
   - Data fields: `palace.trang_sinh`, `palace.bac_si`, `palace.tuong_tinh`, `palace.thai_tue`
   - Example rendering:
     ```
     Tràng Sinh: Lâm Quan    Bác Sĩ: Bác Sĩ
     Tướng Tinh: Tuế Dịch    Thái Tuế: Tang Môn
     ```

5. **NEW: Tuần/Triệt warning** (if applicable)
   - If `palace.tuan === true`: show warning chip "旬空 Tuần" in gold
   - If `palace.triet === true`: show warning chip "截路 Triệt" in red
   - Note: Tuần/Triệt fields may not be in API yet (Sprint 49 deferred). If absent, skip.

6. **Đại Hạn section** (existing — enhance)
   - Show actual age range: `palace.dai_han.range[0]`–`palace.dai_han.range[1]`
   - Show Can Chi: `palace.dai_han.can_chi`
   - Show "Đại Hạn hiện tại" badge if `palace.dai_han.is_current`

### Desktop Hover Enhancement
Currently popup opens on CLICK only. Add hover behavior for desktop:
- `el.addEventListener('mouseenter', ...)` → show popup after 300ms delay
- `el.addEventListener('mouseleave', ...)` → hide after 200ms delay
- Keep click behavior as fallback
- Use a hover timer to prevent flickering (cancel on mouseleave before 300ms)
- Position popup near the hovered cell (not fixed side panel)
- Use CSS: `position: absolute`, calculate top/left from cell bounding rect
- Max width: 320px, max height: 70vh, overflow-y: auto

### Mobile Bottom Sheet (existing — no change)
Already works via `openBottomSheet(html)`. Same HTML content, different container.

---

## TVF-2: Center Panel Enhancement (3pts)

### Current State
Center panel (grid-row 2/4, grid-column 2/4) shows birth info only.

### New Content Layout

```
┌─────────────────────────┐
│   Lá Số Tử Vi           │
│                         │
│ Ngày: 18/5/1984 (DL)   │
│ Âm lịch: 18/4/甲子     │
│ Giờ: Tý (23-01h)       │
│ Giới tính: Nam          │
│                         │
│ ─── Thông Tin Chính ─── │
│ Nạp Âm: Hải Trung Kim  │
│ Cục: Mộc Tam Cục       │
│ Mệnh Chủ: Vũ Khúc      │
│ Thân Chủ: Hỏa Tinh     │
│                         │
│ ─── Tứ Hóa ──────────  │
│ 🟢 Lộc: Liêm Trinh     │
│ 🔴 Quyền: Phá Quân     │
│ 🔵 Khoa: Vũ Khúc       │
│ ⚫ Kỵ: Thái Dương       │
└─────────────────────────┘
```

### Data Sources
- `chart.menh_chu` → "Vũ Khúc" (NEW from Sprint 49)
- `chart.than_chu` → "Hỏa Tinh" (NEW from Sprint 49)
- `chart.tu_hoa` → existing object `{hoa_loc: {star, palace}, hoa_quyen: ...}`
- `chart.nap_am` → existing
- `chart.cuc` → existing

### CSS
- Use CSS variables: `--gold` for accent, `--surface-2` for section dividers
- Font size: 0.75rem for labels, 0.85rem for values
- On mobile (<600px): center panel hidden (existing behavior, chart fills full width)

---

## TVF-3: Tứ Hóa Visual Markers (2pts)

### Where to Show
1. **In palace grid cells** — next to star names in both basic and advanced view
2. **In detail popup** — already showing as badge (existing)
3. **In center panel** — Tứ Hóa summary (TVF-2)

### Rendering Pattern
For each star in `palace.stars`, check `star.tu_hoa`:
- `"Hóa Lộc"` → append `<span class="tu-hoa-dot tu-hoa-loc"></span>`
- `"Hóa Quyền"` → `<span class="tu-hoa-dot tu-hoa-quyen"></span>`
- `"Hóa Khoa"` → `<span class="tu-hoa-dot tu-hoa-khoa"></span>`
- `"Hóa Kỵ"` → `<span class="tu-hoa-dot tu-hoa-ky"></span>`

### CSS for Dots
```
.tu-hoa-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-left: 2px;
    vertical-align: super;
}
.tu-hoa-loc    { background: #4CAF50; }  /* green */
.tu-hoa-quyen  { background: #F44336; }  /* red */
.tu-hoa-khoa   { background: #2196F3; }  /* blue */
.tu-hoa-ky     { background: #616161; }  /* dark gray */
```

### Already Exists (Partial)
`getTuHoaClass(tu_hoa)` and the star-tu-hoa span already exist in `buildDetailHTML`. The grid cell rendering (lines 186-218) also has `thClass` logic. Verify it's rendering correctly — may just need CSS dot styles added.

---

## TVF-4: Advanced View Toggle (3pts)

### Toggle Button
- Position: below the chart grid, centered
- Text: "🔍 Xem Chuyên Sâu" (default) ↔ "📋 Xem Cơ Bản"
- Style: same as existing action buttons (gold border, transparent bg)
- State persisted in `localStorage.setItem('tuvi_advanced_view', 'true'/'false')`

### Basic View (Default — `is_advanced = false`)
Current behavior — 14 main stars only, clean layout. No changes needed.

### Advanced View (`is_advanced = true`)
When toggled ON, each palace cell adds extra content:

1. **Can Chi in header:** Change header from `"Tỵ · Mệnh"` to `"Kỷ Tỵ · Mệnh"`
   - Use `palace.can_chi` field

2. **Adjective stars:** Append small chips below aux stars
   - Font size: 0.55rem (smaller than aux 0.6rem)
   - Color: `var(--text-dim)` (muted)
   - From `palace.adjective_stars`

3. **Ring labels:** Show 4 ring values as tiny labels at bottom of cell
   - Format: `TS:Lâm Quan BS:Bác Sĩ` (abbreviated)
   - Font size: 0.5rem, color: `var(--text-dim)`
   - Abbreviations: TS=Tràng Sinh, BS=Bác Sĩ, TT=Tướng Tinh, TT=Thái Tuế

4. **Đại Hạn range:** Show age range in top-right corner of cell
   - Format: `3-12` in small gold text
   - Position: absolute, top: 2px, right: 4px
   - Font size: 0.5rem

5. **Tuần/Triệt overlay:** If palace has `tuan` or `triet`:
   - Add semi-transparent overlay with icon/text
   - CSS: `position:absolute; top:0; right:0; font-size:0.5rem; color:var(--error);`

### Toggle Mechanics
```
function toggleAdvancedView() {
    isAdvanced = !isAdvanced;
    localStorage.setItem('tuvi_advanced_view', String(isAdvanced));
    renderChart(currentTuviData);  // re-render with new mode
}
```

In `renderChart()`, check `isAdvanced` flag. In the palace element building loop:
- If `isAdvanced`: add `el.classList.add('advanced')` + render extra content
- If not: skip extra content (current behavior)

### CSS for Advanced Mode
```
.palace.advanced { font-size: 0.65rem; }
.palace.advanced .palace-main-stars { font-size: 0.6rem; }
.palace.advanced .adj-chips { display: flex; flex-wrap: wrap; gap: 1px; }
.palace.advanced .adj-chip { font-size: 0.5rem; color: var(--text-dim); }
.palace.advanced .ring-labels { font-size: 0.45rem; color: var(--text-dim); }
.palace.advanced .dai-han-badge {
    position: absolute; top: 2px; right: 4px;
    font-size: 0.5rem; color: var(--gold); opacity: 0.7;
}
```

---

## Implementation Order

1. **TVF-3** (Tứ Hóa dots) — smallest, touches existing code minimally
2. **TVF-2** (center panel) — independent, no grid changes
3. **TVF-4** (advanced toggle) — needs grid changes, builds on TVF-3
4. **TVF-1** (hover popup) — most complex, extends existing detail panel

---

## TVF-5: Per-Palace "Luận Giải Cung Này" Button (3pts)

### Where
Add button at bottom of `buildDetailHTML()` output — inside both desktop popup and mobile bottom sheet.

### Button
- Text: "✨ Luận Giải Cung Này"
- Style: gold border button (same as existing "Luận Giải Lá Số")
- `onclick`: call `interpretPalace(palace)` with the current palace object

### `interpretPalace(palace)` Function
1. Build a targeted question from palace cung_name:
   ```
   PALACE_DOMAINS = {
     'Mệnh': 'vận mệnh tổng quát, tính cách, cuộc đời',
     'Phu Thê': 'tình duyên, hôn nhân, mối quan hệ',
     'Quan Lộc': 'sự nghiệp, công danh, công việc',
     'Tài Bạch': 'tài chính, tiền bạc, thu nhập',
     'Tật Ách': 'sức khỏe, thể chất, bệnh tật',
     'Tử Tức': 'con cái, hậu duệ',
     'Huynh Đệ': 'anh chị em, bạn bè, đồng nghiệp',
     'Điền Trạch': 'nhà cửa, bất động sản, tài sản',
     'Phúc Đức': 'phúc đức, tâm linh, đời sống tinh thần',
     'Phụ Mẫu': 'cha mẹ, gia đình, nguồn gốc',
     'Thiên Di': 'di chuyển, du lịch, quan hệ xã hội',
     'Nô Bộc': 'thuộc hạ, nhân viên, quan hệ xung quanh',
   }
   question = `Luận giải chuyên sâu cung ${palace.cung_name} về ${domain}`
   ```
2. Build `chart_data` focusing on this palace: include the palace's stars, rings, adj stars, Đại Hạn, and the 3 related palaces (tam hợp: positions offset by ±4)
3. Call existing `/api/tuvi/interpret/stream` with this focused question
4. Stream response into the detail popup/bottom sheet content area (replace stars content with streaming interpretation, add "← Quay lại" button to restore star view)

### No BE Changes Needed
The existing `POST /api/tuvi/interpret/stream` accepts `question` + `chart_data`. FE constructs the focused question and passes relevant palace data. LLM system prompt already says "Luận giải bằng tiếng Việt."

### Streaming Target
Render LLM stream into the detail panel content area. Use shared `readSSEStream()`:
```
await readSSEStream(response, contentEl)
```
Show loading state while streaming. When done, add "← Xem lại thông tin cung" button to restore `buildDetailHTML()`.

---

## Critical Reminders for FE

1. **NO TAILWIND.** All CSS must be explicit properties with CSS variables.
2. **Test on mobile.** Bottom sheet must still work. Advanced view should be usable on 375px width.
3. **Preserve existing functionality.** Don't break: chart rendering, side panel, bottom sheet, timeline, form submit.
4. **API data is ready.** All fields used in this spec exist in the Sprint 49 API response. No backend changes needed.
5. **Use `palace.cung_name`** from API, never hardcoded names. (Sprint 48 lesson)
