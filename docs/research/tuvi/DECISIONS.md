# Tu Vi App — Key Decisions (Based on CMO + UX + Technical Research)

**Date:** 2026-03-16 | **Author:** PO
**Inputs:** CMO target_users.md, UX tuvi_ux_research.md, Technical laso.md + zh/ + vi/

---

## 1. School Choice: 南派 (Nam Phái / Southern School)

**Decision:** Use Nam Phái (Southern School) as the primary interpretation framework.

**Why:**
- Most mainstream, widely recognized in Vietnam — matches TinhMenhDo
- Focuses on star combinations + Miếu Vượng brightness — what iztro-py already computes
- Least controversial — practitioners won't argue with the calculations
- Accessible to casual users (star-based reading) while deep enough for practitioners
- Our library (iztro-py/iztro) implements this school

**NOT implementing (for now):**
- 飛星派 (Flying Star) — too advanced for 60-70% casual user base
- 北派 (Northern) — Tứ Hóa emphasis can be added as optional advanced layer later

## 2. Interpretation Documentation Structure

**Pattern:** Same as Gieo Quẻ progressive disclosure (`docs/categories/`)

**For Tu Vi:** Create `docs/tuvi/interpretations/` with per-palace docs:
```
docs/tuvi/interpretations/
├── menh.md          # Cung Mệnh — overall destiny
├── phu_the.md       # Cung Phu Thê — love/marriage
├── quan_loc.md      # Cung Quan Lộc — career
├── tai_bach.md      # Cung Tài Bạch — wealth
├── tat_ach.md       # Cung Tật Ách — health
├── tu_tuc.md        # Cung Tử Tức — children
├── phu_mau.md       # Cung Phụ Mẫu — parents
├── huynh_de.md      # Cung Huynh Đệ — siblings/peers
├── no_boc.md        # Cung Nô Bộc — subordinates
├── thien_di.md      # Cung Thiên Di — travel/social
├── dien_trach.md    # Cung Điền Trạch — property
├── phuc_duc.md      # Cung Phúc Đức — spiritual fortune
└── INDEX.md         # Palace index + cross-reference
```

**Each doc contains (Nam Phái framework):**
1. Palace overview — what life domain it governs
2. Star-specific interpretations — what each of the 14 main stars means IN THIS PALACE
3. Brightness effects — how Miếu/Hãm changes the meaning
4. Star combinations — VCD (đồng cung), Tam Hợp, Đối cung patterns
5. Tứ Hóa effects — what Lộc/Quyền/Khoa/Kỵ means in this palace
6. Supporting palaces — which other palaces to cross-reference

**LLM gets:** Palace doc injected when user clicks "Luận Giải Cung Này"

## 3. UX Design for Target Segments

### 60-70% Casual (Gen Z entertainment)
- **Basic view** is their entire experience — must be beautiful, shareable
- Quick result: enter birthday → see chart → share image
- Social proof: "Cung Mệnh tại Mão — Thiên Phủ tọa thủ" as identity label (like Co-Star personality)
- Shareable card with main stars + palace summary

### 20-25% Life-decision (Millennials)
- **Hover/tap popup** is their sweet spot — palace detail on demand
- "Luận Giải Cung Này" for specific questions (career, love, health)
- Yearly forecast (Tiểu Hạn) is the highest-converting paid feature per CMO

### 5-10% Practitioners
- **Advanced toggle** shows all 114 stars inline
- Can Chi per palace visible
- Tuần/Triệt markers
- They validate our accuracy — if An Sao is wrong, they destroy credibility publicly

## 4. Priority After Sprint 50

1. **Sprint 50** (active): Frontend progressive disclosure (TVF-1→5)
2. **Sprint 51**: Create interpretation docs for top 4 palaces (Mệnh, Quan Lộc, Phu Thê, Tài Bạch) — most asked-about life domains
3. **Sprint 52**: Wire "Luận Giải Cung Này" to LLM with progressive disclosure docs
4. **Then**: X-21/X-22/X-23 Gieo Quẻ fixes

## 5. Market Gap (from CMO + UX)

"No competitor occupies the beautiful grid + progressive depth space for Vietnamese Tu Vi."
- TinhMenhDo: all data, terrible mobile UX
- HOROS: modern design, paywalls everything
- **Our position:** Beautiful chart (casual) + deep interpretation on demand (serious) — free basic, paid yearly forecast
