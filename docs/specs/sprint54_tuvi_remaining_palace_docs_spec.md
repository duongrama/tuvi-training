# Sprint 54: Tu Vi — Remaining 8 Palace Interpretation Docs (X-20)

**Author:** PO | **Date:** 2026-03-16 | **Total:** 8pts
**Scope:** Tu Vi (port 17070) — write interpretation docs for 8 remaining palaces
**Rationale:** Sprint 51 created docs for top 4 palaces (Mệnh, Quan Lộc, Phu Thê, Tài Bạch). 8 remaining palaces still have no interpretation docs — "Luận Giải Cung Này" works but without domain-specific knowledge injection.

---

## Items

### TPD-1: Write 8 Palace Interpretation Docs (6pts) — TL

Create docs for remaining palaces in `gieo_que/backend/tu_vi/docs/interpretations/`:

1. **tat_ach.md** — Cung Tật Ách (health, illness, hidden obstacles)
2. **tu_tuc.md** — Cung Tử Tức (children, creative output)
3. **phu_mau.md** — Cung Phụ Mẫu (parents, superiors, documents)
4. **huynh_de.md** — Cung Huynh Đệ (siblings, peers, colleagues)
5. **no_boc.md** — Cung Nô Bộc (subordinates, employees, friends)
6. **thien_di.md** — Cung Thiên Di (travel, overseas, social change)
7. **dien_trach.md** — Cung Điền Trạch (property, real estate, home)
8. **phuc_duc.md** — Cung Phúc Đức (spiritual fortune, inner life, blessings)

**Same format as existing 4 docs (Nam Phái framework):**
- Palace overview
- Star interpretations (14 main stars in this palace)
- Brightness effects (Miếu vs Hãm)
- Key star combinations
- Tứ Hóa effects
- Supporting palace cross-references

### TPD-2: Wire All 12 Palace Labels in FE (1pt) — FE

Update FE so all 12 palaces show domain-specific labels on the "Luận Giải" button:
- Tật Ách → "Luận Giải Sức Khỏe"
- Tử Tức → "Luận Giải Con Cái"
- Phụ Mẫu → "Luận Giải Phụ Mẫu"
- Huynh Đệ → "Luận Giải Huynh Đệ"
- Nô Bộc → "Luận Giải Giao Tế"
- Thiên Di → "Luận Giải Xuất Hành"
- Điền Trạch → "Luận Giải Nhà Cửa"
- Phúc Đức → "Luận Giải Phúc Đức"

### TPD-3: Test All 12 Palaces (1pt) — QA

Verify all 12 palaces produce domain-specific interpretation when "Luận Giải" is clicked.

---

## Acceptance Criteria

- [ ] 12/12 palace interpretation docs exist (4 existing + 8 new)
- [ ] Each doc is 40-80 lines of genuine Nam Phái content
- [ ] All 12 palaces show domain-specific label on Luận Giải button
- [ ] All 12 palace interpretations stream correctly
