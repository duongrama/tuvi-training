# Sprint 49: Tu Vi Chart Overhaul Phase 1 — Extract Full Star Data

**Author:** PO | **Date:** 2026-03-16 | **Total:** 8pts (reduced from 15 — data already exists!)
**Scope:** Tu Vi backend (port 17070) — extract ALL 114 stars py-iztro already provides
**Rationale:** Boss + user feedback: "chart is too basic, nearly empty." Discovery: py-iztro provides 114 stars but iztro_service.py only extracts 28. Fix = extract all data.
**Research:** docs/research/tuvi/laso.md + libraries.md

---

## Context — KEY DISCOVERY

**py-iztro already provides 114 stars!** We only extract 28. The library has:

| py-iztro attribute | What it is | Count | Status |
|--------------------|-----------|-------|--------|
| `major_stars` | 14 Chính Tinh | 14 | ✅ Extracted |
| `minor_stars` | 14 Auxiliary (6 cát + 6 sát + 2) | 14 | ✅ Extracted |
| `adjective_stars` | 37 Miscellaneous (Hồng Loan, Đào Hoa, etc.) | 37 | ❌ NOT extracted |
| `changsheng12` | Vòng Tràng Sinh value per palace | 12 | ❌ NOT extracted |
| `boshi12` | Vòng Bác Sĩ value per palace | 12 | ❌ NOT extracted |
| `jiangqian12` | Vòng Tướng Tiền per palace | 12 | ❌ NOT extracted |
| `suiqian12` | Vòng Thái Tuế per palace | 12 | ❌ NOT extracted |
| `heavenly_stem` | Can Chi per palace | metadata | ❌ NOT extracted |
| `is_body_palace` | Thân Cung marker | metadata | ❌ NOT extracted |

**No custom algorithms needed. Just extract what py-iztro already computes.**

---

## Items

### TVO-1: Extract ALL star data from py-iztro (3pts) — BE

Update `iztro_service.py` to extract from each palace:
1. `adjective_stars` → translate names + add to palace stars list (category: "adj")
2. `changsheng12` → add as ring entry (category: "trang_sinh")
3. `boshi12` → add as ring entry (category: "bac_si")
4. `jiangqian12` → add as ring entry (category: "tuong_tien")
5. `suiqian12` → add as ring entry (category: "thai_tue")

**API response per palace should include:**
```json
{
  "stars": [...existing...],
  "adj_stars": [{"name": "Hồng Loan", "brightness": null}],
  "rings": {
    "trang_sinh": "Lâm Quan",
    "bac_si": "Bác Sĩ",
    "tuong_tien": "Tuế Dịch",
    "thai_tue": "Tang Môn"
  }
}
```

### TVO-2: Extract palace metadata from py-iztro (2pts) — BE

Extract per palace:
1. `heavenly_stem` → Palace Thiên Can (translate to Vietnamese: "Ất", "Bính", etc.)
2. Combine with earthly_branch → Can Chi string ("Ất Mão", "Bính Thìn")
3. `is_body_palace` → Thân Cung marker

Add to top-level API response:
```json
{
  "menh_chu": "...",
  "than_chu": "...",
  "palaces": [{ "can_chi": "Ất Mão", "is_body_palace": false, ... }]
}
```

### TVO-3: Add Mệnh Chủ / Thân Chủ + Translate star names (3pts) — BE

1. Calculate Mệnh Chủ from Cung Mệnh's Địa Chi (lookup table in research)
2. Calculate Thân Chủ from birth year's Địa Chi (lookup table in research)
3. Translate ALL adjective_star names from English IDs to Vietnamese
4. Add brightness for adjective stars where available
5. Verify star count: should be 100+ total across 12 palaces

---

## Execution Order

1. TL reads research docs (laso.md + zh/research_zh.md) — writes tech spec with exact placement algorithms
2. BE implements TVO-1 through TVO-5 (create `tu_vi/star_placement.py`)
3. TL reviews — verify star placement against Boss reference chart
4. QA tests with 3 reference charts (Boss 18/5/1984, 13/7/1993, 1/2/1980)
5. PO Playwright-verifies (existing chart should now show 100+ stars)

## Acceptance Criteria

- [ ] API returns 100+ stars across 12 palaces (was 28)
- [ ] Vòng Tràng Sinh, Bác Sĩ, Thái Tuế all placed correctly
- [ ] Mệnh Chủ + Thân Chủ in API response
- [ ] Tuần/Triệt palaces identified
- [ ] Palace Can Chi (e.g., "Ất Mão") in API response
- [ ] Boss reference chart (18/5/1984): all stars match reference
- [ ] Unit tests for all placement algorithms
- [ ] TL code review approved

## Note: Phase 2 (Sprint 50) — Frontend UX (Progressive Disclosure)

**Boss directive:** "If you present everything in too much detail right away, the interface will look very cluttered and ugly."

**UX Strategy: Progressive Disclosure (3 layers)**

### Layer 1: Basic View (Default — what casual users see)
- Clean 4x4 grid, same premium dark theme
- Each palace shows: Địa Chi + Cung Name, 14 main stars with brightness superscript (M/V/Đ/B/H)
- Tứ Hóa colored dots on affected stars
- Center panel: basic birth info + Mệnh + Thân
- Đại Hạn timeline at bottom
- **This is what 80% of users want — simple, beautiful, not overwhelming**

### Layer 2: Hover/Popup Detail (Interactive — on demand)
- Hover (desktop) or tap (mobile) a palace cell → popup/zoom overlay showing:
  - ALL stars in this palace (main + auxiliary + adjective + ring values)
  - Star brightness + element + meaning
  - Tứ Hóa effects explanation
  - Vòng Tràng Sinh position
  - Đại Hạn analysis for this period
  - Tiểu Hạn years that fall here
- **Key UX: information appears when user WANTS it, not dumped upfront**

### Layer 3: Advanced/Professional View (Toggle — for practitioners)
- Toggle button: "Xem Chuyên Sâu" / "Xem Cơ Bản"
- Professional view shows ALL stars inline in each palace cell (like TinhMenhDo)
- Can Chi per palace, all ring labels, Tuần/Triệt markers
- **This is for serious Tử Vi practitioners who want the full picture**

### Mobile Consideration
- Layer 1 works perfectly on mobile (already have bottom sheet from Sprint 39)
- Layer 2: tap → bottom sheet with full palace detail (not hover — mobile has no hover)
- Layer 3: may need horizontal scroll or smaller font on mobile — test at 375px

### Use /ui-ux and /frontend-design skills for implementation
