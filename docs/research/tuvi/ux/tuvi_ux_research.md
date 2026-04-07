# Tu Vi Birth Chart UX Research

**Date:** 2026-03-16
**Purpose:** Define the optimal UI/UX pattern for displaying a Vietnamese Tu Vi (Purple Star Astrology) birth chart on web, mobile-first.
**Context:** 4x4 grid, 12 palace cells + center panel. 114 stars per chart. 80% casual users / 20% serious practitioners.

---

## 1. Competitive Landscape Analysis

### 1.1 Co-Star (Western, Minimal, Gen Z target)

**Design philosophy:** Radical simplicity. Co-Star deliberately strips away traditional chart visuals in favor of plain-text personality descriptions. The birth chart exists but is secondary to daily "push notification" style readings.

**Key patterns:**
- **No chart grid on landing.** Users see a personality summary first, chart on demand.
- **Black and white palette** with minimal accent color. Typography-driven, almost brutalist.
- **One insight at a time.** Each planetary placement gets its own card/screen rather than showing everything simultaneously.
- **Social comparison** as the hook (compatibility with friends) rather than data completeness.

**Relevance to Tu Vi:** Co-Star proves that casual users respond to personality narratives, not raw data. However, Tu Vi practitioners expect to see the grid. The takeaway is: lead with insight, not raw star lists.

### 1.2 The Pattern (Western, Personality-Focused)

**Design philosophy:** Emotional resonance over astrological accuracy. Uses proprietary algorithms to translate chart data into personality "patterns" described in plain language.

**Key patterns:**
- **No traditional chart visualization at all.** Everything is text cards with timing cycles.
- **Progressive reveal through "worlds"** -- personal, relationship, professional. Users unlock content over time.
- **Dark theme with gradient accents.** Deep navy/purple backgrounds, soft gradients for visual interest.
- **Micro-animations** on card reveals create a sense of mystical unveiling.

**Relevance to Tu Vi:** The "worlds" concept maps well to Tu Vi's 12 palaces (Menh = personal world, Phu The = relationship world, etc.). But The Pattern goes too far in hiding data for serious Tu Vi users.

### 1.3 TinhMenhDao (Vietnamese Tu Vi, Practitioner-Focused)

**Design philosophy:** Maximum data density. Show everything a practitioner needs in the traditional 4x4 grid format.

**Key patterns:**
- **Traditional 4x4 grid** with all 12 outer palaces and center panel. Standard Tu Vi layout.
- **Every star visible** in every palace cell simultaneously. No hiding, no progressive disclosure.
- **Color coding by star type**: main stars (bold/colored), auxiliary stars (smaller/muted), adjective stars (even smaller).
- **Dense text** within each cell: palace name, Dia Chi, Can Chi, all stars with brightness indicators, Dai Han range.
- **Light theme** (white background, colored text). Traditional web aesthetic.
- **Click-to-detail** opens a separate page or section with interpretation text.

**Strengths:** Complete data at a glance for practitioners. Trusted source.
**Weaknesses:** Overwhelming for casual users. Poor mobile experience (requires horizontal scroll or zoom). No progressive disclosure. No visual delight.

**Relevance to Tu Vi:** This is the "Layer 3" professional view we must support. But it cannot be the default.

### 1.4 HOROS (Vietnamese, Modern UI)

**Design philosophy:** Bridge between traditional Tu Vi data and modern app aesthetics.

**Key patterns:**
- **Cleaner grid** than TinhMenhDao but still shows most stars.
- **Color-coded elements** (Ngu Hanh) with consistent palette.
- **Card-based palace cells** with subtle borders and hover effects.
- **Mobile-responsive** grid that stacks or scrolls.

**Relevance to Tu Vi:** Closest competitor to our design direction. We should match their data fidelity while exceeding their visual polish.

### 1.5 Sanctuary (Western, Guided Readings)

**Design philosophy:** Astrology as guided conversation. Live readings with astrologers, not self-service charts.

**Key patterns:**
- **Reader profiles as primary UI** rather than chart data.
- **Chat-based interaction** for readings.
- **Card-based promotional layout** with trust signals (ratings, reviews).

**Relevance to Tu Vi:** The "AI Interpretation" feature in our app serves a similar role to Sanctuary's live readings. Validates our approach of offering both chart visualization and narrative interpretation.

### 1.6 TimePassages (Western, Detailed)

**Design philosophy:** Traditional circular natal chart with interactive elements.

**Key patterns:**
- **Circular chart** (Western style, not grid) with click-to-expand aspects.
- **Side panel** for detailed planet/house information on click.
- **Toggle between chart types** (natal, transit, progressed).
- **Color coding** for elements (fire, earth, air, water).

**Relevance to Tu Vi:** The side-panel-on-click pattern validates our detail panel approach. The chart-type toggle validates our basic/advanced toggle.

### 1.7 Synthesis: Market Positioning

```
Data Density Spectrum:

LOW                                                    HIGH
|                                                        |
Co-Star    The Pattern    Sanctuary    HOROS    TimePassages    TinhMenhDao
(text only) (text cards)  (chat)       (grid)   (circle+panel)  (full grid)

OUR TARGET: ------>  [HERE]  <------
                   (beautiful grid with progressive depth)
```

We occupy a unique position: the visual beauty of Co-Star's dark theme with the data completeness of TinhMenhDao, bridged by progressive disclosure.

---

## 2. Progressive Disclosure Patterns for Data-Dense Interfaces

### 2.1 NNGroup Research Findings

Nielsen Norman Group's research on progressive disclosure establishes these principles:

1. **Two levels maximum is safest.** Designs exceeding 2 disclosure levels "typically have low usability because users often get lost." Our 3-layer plan pushes this limit -- we must ensure each transition is crystal clear.

2. **Correct feature splitting is critical.** The primary display must contain everything users "frequently need." For Tu Vi, this means the 14 main stars ARE the frequently needed data.

3. **Clear progression mechanics.** Users must understand how to access advanced options through visible buttons and clear labeling that sets expectations.

4. **Progressive disclosure improves learnability, efficiency, and error rates** for both novices and experts.

### 2.2 Financial Dashboard Analogy

Financial dashboards face the identical challenge: massive data sets that serve both casual investors and professional traders.

**Patterns that work:**
- **Summary card at top** with key metrics (portfolio value, daily change). Maps to our center panel with Menh/Than/Cuc.
- **Expandable sections** for each asset class. Maps to our palace cells expanding to show detail.
- **Toggle between "simple" and "advanced" view.** Robinhood vs Bloomberg Terminal. Maps directly to our basic/advanced toggle.
- **Sparkline previews** in summary, full charts on drill-down. Maps to showing star count indicators in the grid, full star list in detail panel.

**Key insight from finance:** The toggle should be persistent (remembered across sessions) and prominently placed, not buried in settings.

### 2.3 Medical Records Analogy

Patient portals (MyChart, Epic) handle similar progressive disclosure:

**Patterns that work:**
- **Summary view** with vitals and recent activity.
- **Section-based drill-down** (labs, medications, visits).
- **Color-coded severity indicators** (normal = green, abnormal = red). Maps to our brightness indicators (Mieu = strong, Ham = weak).
- **"Show more" affordance** within each section rather than separate pages.

**Key insight from healthcare:** Inline expansion (accordion) outperforms navigation to separate pages for maintaining context.

### 2.4 Mobile-Specific Progressive Disclosure

Luke Wroblewski's "Off Canvas" research and modern mobile patterns:

- **Bottom sheets** are the mobile-native progressive disclosure pattern. They preserve context (user sees the grid behind the sheet), allow variable depth (half-screen to full-screen), and have a natural gesture vocabulary (swipe down to dismiss).
- **Full-screen modals** break context and should be reserved for complex multi-step flows.
- **Tooltips** are unreliable on mobile (no hover) and should never be the primary disclosure mechanism.
- **Accordion expand** works well for lists but poorly for grids (expanding one cell disrupts the grid layout).

---

## 3. Hover vs Tap vs Expand: Platform-Specific Patterns

### 3.1 Desktop: Hover Popup

**Tooltip-style (small, positioned near trigger):**
- Best for: Brief supplementary info (1-3 lines).
- For Tu Vi: Could show star count and palace meaning on hover.
- Pros: Zero-click access, fast scanning across multiple palaces.
- Cons: Cannot contain rich content, disappears on mouse-out, not accessible via keyboard alone.

**Popover-style (medium, anchored to trigger):**
- Best for: Moderate detail (a card with 5-10 lines).
- For Tu Vi: Could show main stars with brightness, element colors.
- Pros: Richer than tooltip, still contextual.
- Cons: Can overlap adjacent palaces in a tight grid. Positioning logic complex.

**Side panel (persistent, slides from right):**
- Best for: Full detail view with scrollable content.
- For Tu Vi: Full star list, meanings, ring values, Dai Han info.
- Pros: Does not obscure the grid. Persistent until dismissed. Scrollable.
- Cons: Requires explicit open/close. Reduces visible grid width.

**RECOMMENDATION for desktop:** Use a **300ms hover delay to open the side panel** (current implementation). This gives the speed of hover with the depth of a panel. Add keyboard navigation (Tab through palaces, Enter to open panel).

### 3.2 Mobile: Bottom Sheet

**Half-screen bottom sheet (default height ~50vh):**
- Best for: Quick palace detail. User sees grid peeking above.
- Pros: Maintains spatial context. Natural swipe-to-dismiss. Can drag to full-screen for more.
- Cons: Limited initial viewport for content.

**Full-screen bottom sheet (drag up or scroll):**
- Best for: Complete palace detail with all star cards, ring values, interpretation.
- Pros: Maximum content space. Still dismissible by swipe.
- Cons: Loses grid context entirely when full-screen.

**RECOMMENDATION for mobile:** **Half-screen bottom sheet that expands to full on drag-up.** Start at 50% with main stars and meaning. User drags up to see auxiliary stars, ring values, Dai Han details. This is a built-in progressive disclosure within the disclosure.

### 3.3 Grid Handling on Small Screens (<480px)

The 4x4 grid is the core challenge on mobile. Options:

**Option A: Scaled-down grid (current approach)**
- Shrink each cell to fit 4 columns on screen.
- Pros: Preserves the traditional Tu Vi spatial layout, which has meaning (adjacent palaces interact).
- Cons: Cells become tiny. Text unreadable below ~320px. Stars must be hidden or abbreviated.

**Option B: Horizontal scroll grid**
- Keep cell sizes readable, allow horizontal scroll.
- Pros: Readable text. Traditional layout preserved.
- Cons: Users cannot see the full chart at once. Discoverability of off-screen palaces is poor.

**Option C: Stacked card list (no grid)**
- Show palaces as a vertical card list.
- Pros: Maximum readability. Easy to scroll.
- Cons: Destroys the spatial relationship between palaces, which is fundamental to Tu Vi reading.

**Option D: Mini-grid + zoom interaction**
- Show a small overview grid (like a minimap) with tap-to-zoom on individual palaces.
- Pros: Preserves spatial layout AND readability.
- Cons: Two-step interaction for every palace.

**RECOMMENDATION:** **Option A (scaled-down grid) with intelligent content reduction.** On mobile (<480px):
- Palace cells show: Dia Chi, Cung name, main star COUNT (dots), and Menh/Than watermark only.
- Tap opens bottom sheet with full content.
- This preserves the sacred grid layout while being readable.
- The star dots act as "information scent" (NNGroup) telling users there is more to discover.

---

## 4. Visual Hierarchy for Star Data

### 4.1 The 14 Main Stars

The 14 chinh tinh are the backbone of any Tu Vi reading. They must be immediately visible and distinguishable.

**Current approach (in our code):** Color by Ngu Hanh element, superscript brightness label, Tu Hoa dot. This is solid but can be refined.

**Recommended visual hierarchy within a palace cell (basic view):**

```
PRIORITY 1 — Star name (colored by element)
PRIORITY 2 — Brightness indicator (superscript letter: M/V/D/B/H)
PRIORITY 3 — Tu Hoa marker (colored dot)
PRIORITY 4 — Star count for auxiliary stars (shown as "+N" or dots)
```

**Typography treatment:**
- Main stars: `font-weight: 600`, `font-size: 0.6875rem` (11px) on mobile, `0.8125rem` (13px) on desktop.
- Use `letter-spacing: 0.02em` for readability at small sizes.
- Maximum 3 main stars per line in the cell. If a palace has 4+ main stars, wrap to second line.

### 4.2 Color Coding by Element (Ngu Hanh)

The current element colors from the design system are correct:

| Element | Color | Hex | Contrast on #18181B |
|---------|-------|-----|---------------------|
| Kim (Metal) | Gold | `#FFD700` | 8.5:1 (AAA) |
| Moc (Wood) | Green | `#4CAF50` | 4.6:1 (AA) |
| Thuy (Water) | Blue | `#2196F3` | 4.0:1 (AA) |
| Hoa (Fire) | Red | `#F44336` | 3.9:1 (borderline) |
| Tho (Earth) | Orange | `#FF9800` | 5.6:1 (AA) |

**Accessibility concern:** Hoa (Fire) at `#F44336` barely meets AA contrast on dark surfaces. Consider lightening to `#FF5252` (4.6:1) or `#FF6B6B` (5.2:1) for the chart grid specifically.

**Recommendation:** Keep element colors for main stars only. Auxiliary stars should be monochrome (`--text-muted`) to reduce visual noise.

### 4.3 Brightness Indicators

Three competing approaches:

**A. Superscript letter (current: M/V/D/B/H)**
- Pros: Compact. Familiar to Tu Vi practitioners.
- Cons: Meaningless to casual users. Adds visual clutter.

**B. Color intensity / opacity**
- Mieu (brightest) = full opacity. Ham (weakest) = 40% opacity.
- Pros: Intuitive even for beginners (brighter = stronger). Zero extra UI elements.
- Cons: Low-opacity text on dark backgrounds becomes unreadable. Only 5 levels to encode.

**C. Icon system (filled star, half star, empty star)**
- Pros: Universally understood rating metaphor.
- Cons: Takes horizontal space. Not traditional Tu Vi notation.

**RECOMMENDATION:** **Hybrid approach.** Use opacity modulation as the primary indicator (visible to everyone) with the superscript letter as the secondary indicator (visible to practitioners).

```
Mieu:  opacity 1.0,  superscript "M" in gold
Vuong: opacity 0.9,  superscript "V"
Dac:   opacity 0.8,  superscript "D"
Binh:  opacity 0.65, superscript "B"
Ham:   opacity 0.45, superscript "H" in red-tinted
```

In basic view: show opacity only (no superscript). In advanced view: add the superscript letter.

### 4.4 Tu Hoa Markers

Tu Hoa (Loc, Quyen, Khoa, Ky) are among the most important indicators in Tu Vi. They must be instantly recognizable.

**Current approach:** Colored dots after the star name. Good but could be more distinctive.

**RECOMMENDATION:** Use colored dots with consistent, memorable colors:

| Tu Hoa | Color | Symbol |
|--------|-------|--------|
| Hoa Loc (Wealth) | Green `#4CAF50` | Filled circle |
| Hoa Quyen (Power) | Orange `#FF9800` | Filled circle |
| Hoa Khoa (Fame) | Blue `#2196F3` | Filled circle |
| Hoa Ky (Conflict) | Red `#F44336` | Filled circle |

In the detail panel/bottom sheet, expand these to full badges with the Tu Hoa name spelled out.

---

## 5. Center Panel Design

The center panel (2x2 in the grid, positions row 2-3, col 2-3) is prime real estate. It must serve both quick-glance scanning and provide the chart's identity.

### 5.1 Information Priority for Center Panel

```
TIER 1 (Always visible):
  - Chart title ("Tu Vi La So")
  - Solar birth date
  - Lunar birth date
  - Gender indicator

TIER 2 (Visible, secondary):
  - Nap Am (element affinity)
  - Cuc (life cycle)
  - Menh Chu / Than Chu (ruling stars)

TIER 3 (Visible in advanced view):
  - Tu Hoa summary (4 rows: Loc/Quyen/Khoa/Ky with star names)
  - Menh/Than palace badges
```

### 5.2 Visual Treatment

- **Background:** Slightly elevated from grid cells. Use `--surface` with a subtle gold border-top (`2px solid var(--gold-dim)`).
- **Title:** `font-family: var(--font-display)`, `font-size: 1rem`, `color: var(--gold)`, `letter-spacing: 0.15em`.
- **Birth info:** `font-size: 0.75rem`, `color: var(--text-secondary)`, compact vertical stack.
- **Menh/Than badges:** Pill-shaped with `background: rgba(201,169,98,0.15)`, `border: 1px solid var(--border-gold)`.
- **Tu Hoa summary:** 2-column mini-grid with dot + star name. Only in advanced view.

### 5.3 Mobile Center Panel

On mobile, the center panel is quite small. Options:
- **Collapse to just the title + birth date.** Tap to expand (inline or modal) for full center info.
- **Move center info above the grid** as a card, freeing the 2x2 center for visual breathing room or a decorative element (compass rose, Ba Gua diagram).

**RECOMMENDATION:** On mobile, keep the center panel minimal (title + birth date + Menh/Than badges). All other center info is available in a summary card above the grid or via tap.

---

## 6. Dark Theme Astrology UI Patterns

### 6.1 Why Dark Works for Astrology

Dark themes are overwhelmingly dominant in astrology apps (Co-Star, The Pattern, Sanctuary, most Dribbble concepts). Reasons:
- **Night sky metaphor.** Stars shine against darkness. Astrological data literally "lights up" on a dark background.
- **Premium feel.** Dark + gold = luxury, mysticism, authority.
- **Reduced eye strain** for evening/nighttime use (when people typically check horoscopes).
- **OLED battery savings** on mobile.

### 6.2 Our Palette Assessment

The current palette (`#0C0C0E` background, `#C9A962` gold accent, `#18181B` surface) is well-chosen:

- **Background-to-surface contrast** is subtle (just enough to define card boundaries without harshness).
- **Gold accent** works as the primary action/emphasis color without being garish.
- **Element colors** (Kim/Moc/Thuy/Hoa/Tho) provide the only saturated colors, making them stand out naturally.

### 6.3 Refinements for the Chart Grid

**Palace cell treatment:**
```css
.palace {
    background: var(--surface);         /* #18181B */
    border: 1px solid var(--border);    /* #3F3F46 */
    border-radius: var(--radius-md);    /* 0.5rem -- tighter than cards */
}
.palace.menh {
    border-color: var(--gold);
    box-shadow: inset 0 0 12px rgba(201, 169, 98, 0.08);
}
.palace:hover {
    border-color: var(--border-gold);
    background: var(--surface-hover);
}
```

**Avoid:**
- Pure white text in cells (too harsh). Use `--text-secondary` for star names, `--text-primary` only for palace names.
- Gradients inside cells (distracting, increases rendering cost).
- Thick borders (>1px) on cells (creates visual noise in a 12-cell grid).

### 6.4 Glow and Emphasis Effects

For the Menh (Life) palace, use a subtle gold glow:
```css
box-shadow: 0 0 20px rgba(201, 169, 98, 0.12);
```

For the Than (Body) palace, use a dimmer variant:
```css
box-shadow: 0 0 12px rgba(201, 169, 98, 0.06);
```

For active/selected palace (tapped on mobile):
```css
border-color: var(--gold);
box-shadow: 0 0 0 2px var(--gold-glow);
```

---

## 7. Final Recommendation: The Three-Layer Architecture

### 7.1 Confirmed: Three-Layer Progressive Disclosure

The 3-layer plan is validated by research, with one important modification from NNGroup's findings about the 2-level limit: **Layers 1 and 2 must feel like a single smooth interaction, not a separate "mode."**

### 7.2 Layer 1: Clean Grid (Default)

**Who it serves:** 80% casual users. First-time visitors. People sharing charts on social media.

**What is shown per palace cell:**
- Palace name (Cung Menh, Cung Phu The, etc.) -- `--gold`, `font-weight: 500`
- Dia Chi (Ty, Suu, Dan...) -- `--text-muted`, small
- Main stars (14 chinh tinh only) -- colored by element, with opacity-based brightness
- Tu Hoa dots (colored dots next to starred stars)
- Menh/Than watermark (Chinese character, 30% opacity background)
- On mobile (<480px): star names hidden, replaced by colored dots indicating count and element

**Center panel shows:**
- "Tu Vi La So" title
- Birth date (solar + lunar)
- Menh/Than palace indicators
- Nap Am + Cuc

**Interaction:** Tap any palace to open Layer 2.

### 7.3 Layer 2: Palace Detail (Tap/Click)

**Who it serves:** Everyone who wants to understand a specific palace.

**How it opens:**
- Mobile: Bottom sheet (starts at 50% height, draggable to full).
- Desktop: Side panel (slides from right, 360px wide).
- Desktop hover: 300ms delay opens side panel automatically.

**What is shown:**
- Palace header: Dia Chi + Cung Name + Dai Han range
- Palace meaning (one-sentence interpretation)
- Main stars as cards: name (colored), element label, brightness badge, Tu Hoa badge, one-line meaning
- Auxiliary stars as chips: name only, `--text-muted`, smaller
- Adjective stars (Tap Tinh) as even smaller chips
- Ring values (Trang Sinh, Bac Si, Tuong Tinh, Thai Tue) in a 2x2 mini-grid
- Dai Han period if applicable
- Tuan/Triet warnings if applicable

**Interaction:** Swipe down (mobile) or click X / click overlay (desktop) to dismiss and return to grid.

### 7.4 Layer 3: Professional View (Toggle)

**Who it serves:** 20% serious practitioners. Tu Vi students. People comparing with TinhMenhDao.

**How it activates:**
- Toggle button below the chart: "Xem Chuyen Sau" / "Xem Co Ban"
- State persisted in localStorage (already implemented).
- Button uses secondary style (outline), not primary, to avoid accidental activation.

**What changes in the grid:**
- Can Chi appears in palace header
- ALL auxiliary stars shown as small text in each cell (not just main stars)
- Adjective stars shown as even smaller chips
- Ring value abbreviations shown at cell bottom (TS:Truong Sinh, BS:Bac Si...)
- Dai Han age range badge on each cell
- Tuan/Triet overlay marks (Chinese characters)
- Brightness superscript letters appear alongside opacity

**What changes in the center panel:**
- Tu Hoa summary (4 rows with star names)
- Full Menh/Than details

**Important:** Advanced view does NOT replace Layers 1/2. It enhances Layer 1 with more data. Layer 2 (detail panel) still works and shows even more context in advanced mode.

### 7.5 Architecture Summary

```
+------------------+---------------------+----------------------+
|   LAYER 1        |    LAYER 2          |    LAYER 3           |
|   (Default Grid) |    (Tap Detail)     |    (Toggle Advanced) |
+------------------+---------------------+----------------------+
| 14 main stars    | ALL stars           | All stars IN grid    |
| Element colors   | Star meanings       | Can Chi in header    |
| Tu Hoa dots      | Brightness badges   | Ring abbreviations   |
| Menh/Than marks  | Ring values grid    | Dai Han ranges       |
| Palace names     | Dai Han details     | Tuan/Triet marks     |
| (opacity bright) | Tuan/Triet warnings | Brightness letters   |
|                  | Adjective stars     | Adjective chips      |
+------------------+---------------------+----------------------+
| TRIGGER: default | TRIGGER: tap cell   | TRIGGER: toggle btn  |
| AUDIENCE: all    | AUDIENCE: all       | AUDIENCE: 20% expert |
+------------------+---------------------+----------------------+
```

### 7.6 Mobile-Specific Adaptations

| Breakpoint | Grid Behavior | Cell Content | Detail Mechanism |
|------------|---------------|--------------|------------------|
| >768px (desktop) | Full 4x4, cells ~140px | Full Layer 1 content | Side panel (right) |
| 480-768px (tablet) | Full 4x4, cells ~100px | Main stars, abbreviated | Bottom sheet (50%) |
| <480px (phone) | Full 4x4, cells ~80px | Dia Chi + Cung + dots only | Bottom sheet (50%->full) |

**Critical mobile decisions:**
1. **Keep the 4x4 grid on ALL screen sizes.** The spatial layout is fundamental to Tu Vi. Never linearize it.
2. **Use colored dots** as "information scent" on small screens. Each dot = one main star, colored by element. Users intuitively understand "more dots = more stars = tap to see."
3. **Bottom sheet starts at 50%** so the grid remains partially visible, maintaining spatial context.
4. **Swipe between palaces** within the bottom sheet (left/right swipe moves to adjacent palace in grid order) -- future enhancement.

### 7.7 Animation and Transition Specs

**Grid entrance:** Staggered fade-in, clockwise order, 60ms delay per palace (already implemented).

**Layer 2 transitions:**
- Bottom sheet: `transform: translateY(100%) -> translateY(0)`, `transition: 0.3s cubic-bezier(0.32, 0.72, 0, 1)` (iOS-style spring).
- Side panel: `transform: translateX(100%) -> translateX(0)`, `transition: 0.25s ease-out`.
- Overlay: `opacity: 0 -> 0.6`, `transition: 0.2s ease`.

**Layer 3 toggle:**
- Crossfade with subtle scale: `opacity + transform: scale(0.98) -> scale(1)`, `transition: 0.3s ease`.
- Stars that appear in advanced mode should individually fade in with 30ms stagger.

### 7.8 Accessibility Requirements

| Requirement | Implementation |
|-------------|---------------|
| WCAG AA contrast (4.5:1) | All text passes except Hoa red -- lighten to #FF5252 |
| Keyboard navigation | Tab through palaces, Enter to open detail, Escape to close |
| Screen reader | `aria-label` on each palace with Dia Chi + Cung name (already done) |
| Reduced motion | Respect `prefers-reduced-motion` -- disable stagger animations |
| Touch targets | Palace cells minimum 44x44px on mobile (already met by grid sizing) |
| Focus indicators | Gold focus ring (`box-shadow: 0 0 0 2px var(--gold-glow)`) |

---

## 8. Implementation Priorities

### Phase 1 (Current Sprint -- Refine existing)
- [ ] Adjust Hoa element color for AA contrast
- [ ] Implement opacity-based brightness (hide superscripts in basic view)
- [ ] Mobile dot indicators instead of star names on <480px
- [ ] Bottom sheet drag-to-expand (50% -> full)

### Phase 2 (Next Sprint -- Polish)
- [ ] Keyboard navigation (Tab/Enter/Escape)
- [ ] `prefers-reduced-motion` support
- [ ] Swipe between palaces in bottom sheet
- [ ] Center panel responsive collapse on mobile

### Phase 3 (Future -- Delight)
- [ ] Palace highlight on hover showing related palaces (San Phuong Tu Chinh)
- [ ] Animated Tu Hoa flow lines connecting stars across palaces
- [ ] Compare two charts side-by-side (relationship compatibility)
- [ ] Print-friendly view for practitioners

---

## 9. References

- Nielsen Norman Group, "Progressive Disclosure" (nngroup.com/articles/progressive-disclosure/)
- Nielsen Norman Group, "Information Scent" (nngroup.com/articles/information-scent/)
- Luke Wroblewski, "Off Canvas Multi-Device Layouts" (lukew.com)
- Material Design, "Bottom Sheets" component guidelines (m2.material.io)
- Co-Star Astrology app (costarastrology.com) -- minimal approach analysis
- The Pattern app (thepattern.com) -- personality-focused approach analysis
- TinhMenhDao (tinhmenhdao.com) -- traditional practitioner approach analysis
- Astrology Zone (astrologyzone.com) -- card-based content organization
- HOROS Vietnamese astrology -- modern Tu Vi UI reference
