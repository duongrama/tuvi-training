# Sprint 51: Tu Vi Palace Interpretation — Knowledge Base + Per-Palace LLM

**Author:** PO | **Date:** 2026-03-16 | **Total:** 13pts
**Scope:** Tu Vi (port 17070) — create interpretation docs for top 4 palaces + wire per-palace LLM
**Rationale:** Chart shows data but no targeted interpretation. Users click a palace and want to know "What does this mean for my career/love/health?" Need progressive disclosure docs (like Gieo Quẻ categories) + per-palace LLM endpoint.
**School:** Nam Phái (Southern School) — see docs/research/tuvi/DECISIONS.md
**Research:** docs/research/tuvi/laso.md, zh/research_zh.md, vi/research_vi.md

---

## Context

Gieo Quẻ already has this pattern:
- `gieo_que/docs/categories/{category}.md` — domain-specific interpretation guides
- LLM classifies question → loads category doc → injects into system prompt
- Pattern works but only 1/10 categories is filled (tinh_duyen)

For Tu Vi, the 12 palaces ARE the categories. Each palace governs a life domain. When user clicks "Luận Giải" on a palace, inject that palace's interpretation doc into LLM context.

---

## Items

### TVI-1: Create 4 Palace Interpretation Docs (5pts) — TL

Create `gieo_que/backend/tu_vi/docs/interpretations/` with docs for the 4 most-asked palaces:

1. **menh.md** — Cung Mệnh (overall destiny, personality)
2. **quan_loc.md** — Cung Quan Lộc (career, achievement)
3. **phu_the.md** — Cung Phu Thê (love, marriage, relationships)
4. **tai_bach.md** — Cung Tài Bạch (wealth, income, finances)

**Each doc must contain (Nam Phái framework):**
- Palace overview — what life domain, how to read it
- Star interpretations: what each of the 14 main stars means IN THIS PALACE
- Brightness effects: how Miếu vs Hãm changes meaning for key stars
- Key star combinations: VCD (đồng cung pairs), Tam Hợp influences
- Tứ Hóa effects: what Lộc/Quyền/Khoa/Kỵ means in this palace
- Supporting palaces: which other palaces to cross-reference (e.g., for Quan Lộc also check Mệnh + Tài Bạch)

**Source:** Use research docs (vi/research_vi.md, zh/research_zh.md) + search for authoritative Nam Phái interpretation references. Each doc should be 200-400 lines of genuine domain knowledge, NOT generic filler.

### TVI-2: Per-Palace LLM Interpretation Endpoint (3pts) — BE

Create API endpoint: `POST /api/tuvi/interpret/palace`

**Request:**
```json
{
  "year": 1984, "month": 5, "day": 18, "hour": 0,
  "gender": "male", "calendar_type": "solar",
  "palace_name": "quan_loc"
}
```

**Behavior:**
1. Generate chart (existing logic)
2. Extract target palace data (stars, brightness, rings, Tứ Hóa)
3. Extract supporting palace data (per doc's cross-reference)
4. Load palace interpretation doc from `docs/interpretations/{palace_name}.md`
5. Inject palace doc + palace data into LLM system prompt
6. Stream interpretation via SSE (existing streaming pattern)

**LLM prompt structure:**
```
[System] You are a Tu Vi (Tử Vi Đẩu Số) master following Nam Phái (Southern School).
[Palace doc injected here — progressive disclosure]
[User's specific palace data: stars, brightness, Tứ Hóa, rings]
[Supporting palaces data]
[Instruction] Interpret this palace for the user. Focus on {life domain}. Vietnamese only. Casual "bạn" tone.
```

### TVI-3: Frontend "Luận Giải Cung Này" Button (3pts) — FE

Wire the popup's "Luận Giải" button to the new endpoint.

**Requirements:**
- Add "Luận Giải Cung Này" button in palace popup (from TVF-1)
- On click: call `/api/tuvi/interpret/palace` with palace_name
- Stream response into popup/bottom sheet (reuse existing streaming pattern)
- Show loading state while LLM generates
- Each palace gets its own domain label:
  - Mệnh → "Luận Giải Vận Mệnh"
  - Quan Lộc → "Luận Giải Sự Nghiệp"
  - Phu Thê → "Luận Giải Tình Duyên"
  - Tài Bạch → "Luận Giải Tài Lộc"
  - Others → "Luận Giải Cung Này" (generic, docs not yet written)

### TVI-4: Unit Tests (2pts) — BE

- Test palace doc loading (file exists, correct content)
- Test LLM prompt construction (palace data correctly injected)
- Test endpoint returns SSE stream
- Mock LLM calls (no real API in tests)

---

## Execution Order

1. TL writes interpretation docs (TVI-1) — this is the hardest part, requires domain expertise
2. BE implements endpoint (TVI-2) in parallel
3. FE wires button (TVI-3) after BE endpoint ready
4. BE writes tests (TVI-4)
5. TL reviews all
6. QA tests: click palace → LLM streams interpretation for that life domain
7. PO Playwright-verifies

## Acceptance Criteria

- [ ] 4 palace interpretation docs exist (menh, quan_loc, phu_the, tai_bach)
- [ ] Each doc is 200+ lines of genuine Nam Phái interpretation content
- [ ] "Luận Giải Cung Này" button in popup streams LLM interpretation
- [ ] Interpretation is focused on the specific life domain (not generic)
- [ ] Vietnamese casual tone, streaming, structured sections
- [ ] Unit tests pass with mocked LLM
- [ ] TL code review approved
