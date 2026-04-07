# Sprint 50: Tu Vi Chart Overhaul Phase 2 — Frontend UX (Progressive Disclosure)

**Author:** PO | **Date:** 2026-03-16 | **Total:** 13pts
**Scope:** Tu Vi frontend (port 17070) — redesign chart display with 3-layer progressive disclosure
**Rationale:** API now returns 114 stars. Boss directive: "Don't show everything upfront — too cluttered. Basic view default, hover for detail, toggle for advanced."
**Research:** docs/research/tuvi/laso.md section 11, lt-memory/po/ux_principles.md

---

## UX Strategy: 3-Layer Progressive Disclosure

### Layer 1: Basic View (Default) — What 80% of users see
- Clean 4x4 grid (existing dark theme)
- Each palace shows: Địa Chi + Cung Name + Can Chi (e.g., "Kỷ Tỵ — Mệnh")
- **14 main stars only** with brightness superscript (Liêm Trinh^M, Tham Lang^V)
- Tứ Hóa colored dots on affected main stars (Lộc=green, Quyền=red, Khoa=blue, Kỵ=dark)
- 命/身 watermarks on Mệnh/Thân palaces (already have this)
- Đại Hạn range in corner of each cell
- Center panel: birth info + Nạp Âm + Cục + Mệnh Chủ + Thân Chủ + Tứ Hóa summary

### Layer 2: Hover/Tap Detail Popup — On demand
- **Desktop:** hover over palace cell → popup overlay
- **Mobile:** tap palace cell → bottom sheet slides up (existing pattern from Sprint 39)
- Popup shows:
  1. Palace name + Can Chi + Đại Hạn period
  2. ALL main stars with brightness + meaning
  3. ALL auxiliary stars (minor + adjective) with meanings
  4. Ring positions: Tràng Sinh, Bác Sĩ, Tướng Tinh, Thái Tuế values
  5. Tứ Hóa effects explanation (if any star has Hóa)
  6. Tuần/Triệt warning (if palace is affected)
  7. Star element + brightness effect text

### Layer 3: Advanced View (Toggle) — For practitioners
- Button: "Xem Chuyên Sâu" ↔ "Xem Cơ Bản"
- Shows ALL stars inline in each palace cell (like TinhMenhDo)
- Smaller text, denser layout
- Can Chi prominently displayed
- Ring values shown as small labels
- Tuần/Triệt markers on affected palaces

---

## Items

### TVF-1: Palace Hover/Tap Detail Popup (5pts) — FE

**What:** When user hovers (desktop) or taps (mobile) a palace cell, show a detail overlay.

**Requirements:**
- Desktop: hover → floating popup positioned near the cell
- Mobile: tap → bottom sheet (reuse existing bottom-sheet pattern from Sprint 39)
- Content: all stars (main + adjective), ring values, Tứ Hóa effects, brightness meanings
- Smooth animation (fade in, no layout jumps)
- Click outside / swipe down to dismiss
- Data comes from API `palaces[].adjective_stars`, `trang_sinh`, `bac_si`, `tuong_tinh`, `thai_tue`

### TVF-2: Center Panel Enhancement (3pts) — FE

**What:** Update center panel to show all new metadata.

**Requirements:**
- Add: Mệnh Chủ, Thân Chủ (from API `menh_chu`, `than_chu`)
- Add: Tứ Hóa summary (Lộc→Star, Quyền→Star, Khoa→Star, Kỵ→Star)
- Show Can Chi for Mệnh palace (e.g., "Cung Mệnh: Kỷ Tỵ")
- Keep existing: Dương/Âm date, Nạp Âm, Cục, 命/身 positions

### TVF-3: Tứ Hóa Visual Markers on Stars (2pts) — FE

**What:** Show colored dots next to stars that have Tứ Hóa transformations.

**Requirements:**
- Lộc = small green dot/circle
- Quyền = small red dot/circle
- Khoa = small blue dot/circle
- Kỵ = small dark/gray dot/circle
- Already have star `tu_hoa` field in API — just need visual rendering
- Must be visible in both basic and advanced view

### TVF-4: Advanced View Toggle (3pts) — FE

**What:** Button to switch between basic (clean) and advanced (full) view.

**Requirements:**
- Toggle button below chart: "Xem Chuyên Sâu" ↔ "Xem Cơ Bản"
- Basic view: 14 main stars only (default)
- Advanced view: ALL stars shown inline (main + adjective + ring labels)
- Can Chi displayed in each cell header (e.g., "Kỷ Tỵ")
- Tuần/Triệt markers: dim overlay or icon on affected palaces
- Remember toggle state in localStorage
- Smaller font in advanced mode to fit more stars

---

## Execution Order

1. TL reads spec + reviews API data structure
2. FE implements TVF-1 (popup) — most impactful
3. FE implements TVF-2 (center panel) + TVF-3 (Tứ Hóa dots)
4. FE implements TVF-4 (advanced toggle)
5. Use /ui-ux and /frontend-design skills for popup design
6. TL reviews
7. QA tests both basic and advanced views
8. PO Playwright-verifies with Boss reference chart

### TVF-5: Per-Palace "Luận Giải" in Popup (3pts) — FE+BE

**What:** Replace single "Luận Giải Lá Số" with per-palace targeted interpretation.

**Problem:** Current button does general overview of entire chart. Users want focused answers: "How's my career?" → read Quan Lộc palace. "Love life?" → read Phu Thê palace.

**Requirements:**
- In the hover/popup detail (TVF-1), add "Luận Giải Cung Này" button
- When clicked, send to LLM: this palace's stars + brightness + Tứ Hóa + supporting palaces' data
- LLM interprets specifically for that life domain (career, love, health, etc.)
- Keep existing "Luận Giải Lá Số" as "Tổng Quan" option for general reading
- Palace-to-domain mapping:
  - Quan Lộc → career interpretation
  - Phu Thê → love/marriage
  - Tài Bạch → wealth/money
  - Tật Ách → health
  - Mệnh → overall destiny
  - etc.

---

## Acceptance Criteria

- [ ] Hover (desktop) or tap (mobile) → popup with ALL stars + ring values
- [ ] Popup has "Luận Giải Cung Này" button → LLM interprets that specific palace
- [ ] Center panel shows Mệnh Chủ, Thân Chủ, Tứ Hóa summary
- [ ] Tứ Hóa colored dots visible on affected stars
- [ ] Advanced toggle works — shows 114 stars inline
- [ ] Basic view is clean and not cluttered (14 main stars only)
- [ ] Mobile bottom sheet works for palace detail
- [ ] Boss reference chart (18/5/1984): all data visible in popup/advanced view
