# Sprint 39: Tu Vi UI/UX Complete Revamp

**Author:** PO (research-driven) | **Date:** 2026-03-15 | **Total:** 21pts
**App:** Tu Vi (port 17070) | **Folder:** `gieo_que/backend/tu_vi/frontend/`
**Boss Directive:** "UI UX is shitty, revamp the whole fucking app"

---

## Research Summary

Studied 11 apps: Thái Âm, Tử Vi Trọn Đời, LUHO, lichngaytot.com, tracuutuvi.com, Co-Star, The Pattern, Sanctuary, TimePassages + 2 more. Key takeaways:

1. **Best Vietnamese app (Thái Âm):** Dark mode, frosted glass cards, step-by-step input, bold orange accent
2. **Co-Star pattern:** Chart cells = navigation (tap → detail). Minimal text in cells, detail in panels
3. **The Pattern:** Life timeline as emotional journey, psychological language over technical terms
4. **Mobile solution:** Mini-grid with tap-to-expand (Solution D) — show palace names only, hide stars until tapped

---

## Current Problems (Why It's Shitty)

1. **Grid = spreadsheet** — all 12 palaces look identical, no visual hierarchy
2. **Government form inputs** — bare number fields for year/month/day/hour/minute
3. **Mobile broken** — falls back to vertical list, loses spatial palace relationships
4. **Stars crammed** — 15+ star names in tiny cells, unreadable
5. **No emotional connection** — feels like a database viewer, not a mystical chart
6. **Timeline boring** — horizontal scroll of identical boxes
7. **Mệnh palace doesn't stand out** — most important palace has a thin gold border, that's it
8. **Center panel is `Center-panel` (typo)** — CSS class has capital C, inconsistent
9. **5-row grid layout** — PALACE_GRID uses 5 rows (Tý and Hợi on row 5), should be standard 4x4

---

## Revamp Scope (5 Areas)

### TV-R1: Input Form Revamp (3pts) — FE

**Replace government form with ceremonial input experience.**

- Decorative ornament divider above title (gold lines + symbol)
- Date inputs: 3 large centered number fields (Day / Month / Year) with labels below
  - Font: Cormorant Garamond 24px, centered text
  - Remove spinner arrows (`-moz-appearance: textfield`)
  - Focus: gold border + `box-shadow: 0 0 0 2px rgba(201, 169, 98, 0.15)`
- **Hour selection: 12 Dia Chi buttons in 4x3 grid** (CRITICAL — most Vietnamese users know birth hour as "giờ Tý/Sửu/Dần..." not "0-23")
  - Each button: Dia Chi name (16px bold) + hour range below (11px muted)
  - Selected: gold border + gold-tinted background
  - Data mapping: Tý→0, Sửu→2, Dần→4, Mão→6, Thìn→8, Tỵ→10, Ngọ→12, Mùi→14, Thân→16, Dậu→18, Tuất→20, Hợi→22
- Gender: Two pill buttons with celestial icons (☉ Nam / ☽ Nữ)
- Submit button: Full-width, Cormorant Garamond 18px, letter-spacing 0.08em
- After submit: form collapses upward (animation), "Sửa thông tin" button appears above chart

### TV-R2: Birth Chart Grid Revamp (5pts) — FE

**Transform spreadsheet into mystical chart.**

**Fix PALACE_GRID to standard 4x4:**
```
Row 1: Tỵ(6), Ngọ(7), Mùi(8), Thân(9)
Row 2: Thìn(5), [CENTER], [CENTER], Dậu(10)
Row 3: Mão(4), [CENTER], [CENTER], Tuất(11)
Row 4: Dần(3), Sửu(2), Tý(1), Hợi(12)
```
Center panel: `grid-column: 2/4; grid-row: 2/4`

**Palace cell redesign (3 zones):**
1. **Header:** Dia Chi (left, 15px display font) + Cung Name (right, 10px muted uppercase)
2. **Main stars:** 12px body font, element-colored (Kim=#FFD700, Moc=#4CAF50, Thuy=#2196F3, Hoa=#F44336, Tho=#FF9800)
   - Brightness as superscript: Miếu(gold) > Vượng(gold-dim) > Đắc(white) > Bình(muted) > Hãm(red)
   - Tứ Hóa as 6px colored dot after star name (Lộc=green, Quyền=red, Khoa=blue, Kỵ=gray)
3. **Aux stars:** 10px muted, compact flow, separated by dashed border-top

**Mệnh palace — DRAMATIC highlight:**
- 2px gold border + gold glow (`box-shadow: 0 0 20px rgba(201, 169, 98, 0.15)`)
- Subtle gold gradient background
- 命 character watermark (top-right, 11px, 50% opacity)

**Thân palace — secondary emphasis:**
- Silver border + subtle silver gradient
- 身 character watermark

**Center panel:** Radial gold glow behind content. Show: title, birth date (solar + lunar), Nạp Âm, Cục, Mệnh/Thân badges.

**Staggered entrance animation:** Palaces appear clockwise with 60ms delay each, center panel last (750ms).

### TV-R3: Mobile Responsive (5pts) — FE

**CRITICAL: Keep 4x4 grid on mobile, but compress cells.**

On screens < 600px:
- **Hide all star names in grid cells** — show only Dia Chi + Cung Name + star count dots
- Palace cells: 8px padding, ~90px wide on 375px screen
- Tap any cell → **bottom sheet** (not side panel) slides up at 85% screen height
  - Drag handle bar at top (36px wide, 4px tall, gray)
  - Border-radius 16px 16px 0 0 on panel top
- Center panel: compact (12px padding, 15px title)
- Star count shown as small gold dots (4px each) — visible only on mobile

**This preserves spatial relationships (which palace is opposite which) while solving the density problem.**

### TV-R4: Fortune Timeline Revamp (3pts) — FE

**Replace boring scroll strip with life journey visualization.**

- Section title: "Đường Vận Mệnh" (Cormorant Garamond, gold)
- Horizontal scroll track with scroll-snap-type: x mandatory
- Each Đại Hạn period = segment card (72px wide, rounded)
  - Shows: age range (12px bold) + Dia Chi (14px display) + palace name (10px muted)
  - Past periods: opacity 0.5
  - Future periods: opacity 0.7
  - **Current Đại Hạn: HERO treatment** — wider (100px), gold gradient background, 2px gold border, golden glow, gold dot indicator below
  - Current Tiểu Hạn: purple border overlay
- Auto-scroll to center current period on render
- Summary banner below timeline: "Đại Hạn: [Palace] (age range) | Tiểu Hạn [year]: [Palace]"
- Custom scrollbar: 4px gold thumb on dark track

### TV-R5: AI Interpretation & Detail Panel Polish (5pts) — FE

**Detail panel (when tapping palace):**
- Star cards: each main star in its own rounded card with name (element-colored), brightness badge, Tứ Hóa badge, meaning text
- Section dividers: ornamental lines with text centered ("─── Chính Tinh ───", "─── Phụ Tinh ───")
- Aux stars as rounded chips (compact)
- Đại Hạn section showing which life period this palace governs

**AI interpretation panel:**
- CTA button: ornamental outline style ("═══ Luận Giải Lá Số ═══")
- Panel fade-slide-in animation (0.4s)
- Three pulsing gold dots for loading (not text "Đang luận giải...")
- Golden blinking cursor bar (2px wide) during streaming
- Markdown headings styled: h2=20px gold, h3=17px gold
- Blockquotes: gold left-border, tinted background

---

## Design System Compliance

Fix current divergences:
- `--surface: #1A1A2E` → `#18181B` (match design system)
- Add missing tokens: `--border-gold`, `--gold-dim`, `--gold-glow`
- Fix `Center-panel` typo → `center-panel` (lowercase)
- Add `@media (prefers-reduced-motion: reduce)` to disable animations
- Add `.sr-only` utility for accessibility
- Add `role="button"` + `tabindex="0"` + `aria-label` on palace cells

---

## What NOT To Change

- Backend API stays the same — this is pure frontend
- Star calculation logic untouched
- AI interpretation endpoint unchanged
- Profile modal (Sprint 38 X5-4) — keep as-is, just ensure it matches new styles

---

## Execution Order

1. TL reviews this spec, adds any technical notes
2. FE implements TV-R1 (input form) + TV-R2 (grid) first — these are the biggest impact
3. FE implements TV-R3 (mobile) — test on 375px
4. FE implements TV-R4 (timeline) + TV-R5 (detail panel + AI)
5. TL code reviews
6. QA tests on desktop + mobile viewport
7. PO Playwright-verifies

---

## Acceptance Criteria

- [ ] 4x4 grid renders correctly (not 5 rows)
- [ ] Mệnh palace has dramatic gold highlight with 命 watermark
- [ ] Hour input uses 12 Dia Chi buttons, not number field
- [ ] Mobile (375px): grid stays 4x4 with compressed cells, tap → bottom sheet
- [ ] Timeline auto-scrolls to current Đại Hạn
- [ ] Staggered entrance animation on chart render
- [ ] Design system colors match (--surface: #18181B)
- [ ] All palace cells are keyboard-accessible (tabindex, aria-label)
