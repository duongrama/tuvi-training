# Sprint 51: Per-Palace LLM Interpretation + Palace Knowledge Docs

**Author:** TL | **Date:** 2026-03-16 | **Total:** 6pts
**Scope:** Tu Vi (port 17070) — per-palace "Luận Giải Cung Này" in popup + 4 palace interpretation docs
**Rationale:** Users want focused answers: "How's my career?" = read Quan Lộc only, not entire chart. LLM needs palace-specific knowledge docs for deep, accurate interpretations.

---

## Items

### TVF-5: Per-Palace "Luận Giải Cung Này" Button (3pts) — FE

**Where:** Bottom of `buildDetailHTML()` output — appears in both desktop popup and mobile bottom sheet.

**Button:** "✨ Luận Giải Cung Này" — gold border style matching existing action buttons.

**On click → `interpretPalace(palace)`:**

1. Build focused question from palace domain:

| cung_name | Domain prompt suffix |
|-----------|---------------------|
| Mệnh | vận mệnh tổng quát, tính cách, xu hướng cuộc đời |
| Phu Thê | tình duyên, hôn nhân, mối quan hệ tình cảm |
| Quan Lộc | sự nghiệp, công danh, phát triển nghề nghiệp |
| Tài Bạch | tài chính, tiền bạc, nguồn thu nhập |
| Tật Ách | sức khỏe, thể chất, những bệnh tật cần lưu ý |
| Tử Tức | con cái, hậu duệ, mối quan hệ với thế hệ sau |
| Huynh Đệ | anh chị em, bạn bè thân, đồng nghiệp |
| Điền Trạch | nhà cửa, bất động sản, tài sản cố định |
| Phúc Đức | phúc đức, đời sống tinh thần, tâm linh |
| Phụ Mẫu | cha mẹ, gia đình, sự hỗ trợ từ bề trên |
| Thiên Di | di chuyển, du lịch, quan hệ xã hội bên ngoài |
| Nô Bộc | thuộc hạ, nhân viên, người giúp đỡ xung quanh |

Question format: `"Luận giải chuyên sâu cung ${palace.cung_name} về ${domain}"`

2. Build focused `chart_data` for the request:
   - Include the target palace (all stars, adj stars, rings, Đại Hạn)
   - Include 3 tam hợp palaces (positions ±4 mod 12 from target) — these influence the target
   - Include Mệnh palace data (always relevant context)
   - Include chart-level: nap_am, cuc, menh_chu, than_chu, tu_hoa

3. Call existing `POST /api/tuvi/interpret/stream` — no BE changes needed:
   ```
   fetch(`/api/tuvi/interpret/stream?device_id=${deviceId}`, {
       method: 'POST',
       headers: {'Content-Type': 'application/json'},
       body: JSON.stringify({
           question: focusedQuestion,
           birth_info: currentTuviData.birth.solar,
           chart_data: focusedChartData,
           static_interpretation: palace.meaning || ''
       })
   })
   ```

4. Stream response into detail panel content area using shared `readSSEStream(response, contentEl)`.

5. Replace panel content with streaming text. Show:
   - Loading: "Đang luận giải cung ${cung_name}..."
   - After stream: add "← Xem lại thông tin cung" button
   - Button restores original `buildDetailHTML(palace)` content

**Freemium gate:** Call `checkServerUsage('tuvi', API_BASE)` before streaming. If not allowed, show paywall. Call `incrementServerUsage` on stream complete (use `usageIncremented` guard pattern from Sprint 44).

### TV-DOC-1: Palace Interpretation Knowledge Docs (3pts) — TL

Create 4 focused palace interpretation reference docs for LLM context injection. These give the LLM domain-specific knowledge for deeper interpretations.

**Location:** `gieo_que/backend/tu_vi/docs/palace_guides/`

**4 docs (highest-demand palaces):**

1. **menh.md** — Cung Mệnh interpretation guide
   - What Mệnh represents (core self, innate destiny)
   - Key star combinations in Mệnh and their meanings
   - How Mệnh Chủ interacts with Mệnh stars
   - Brightness effects specific to Mệnh context
   - Common Tứ Hóa patterns in Mệnh

2. **quan_loc.md** — Cung Quan Lộc interpretation guide
   - Career trajectory indicators (which stars = leadership, which = technical)
   - Timing: how Đại Hạn through Quan Lộc affects career phases
   - Key star combos: Tử Vi+Tham Lang = entrepreneur, Thiên Cơ+Cự Môn = advisory
   - Warning stars in Quan Lộc (Kình Dương = conflict, Hóa Kỵ = obstacles)

3. **phu_the.md** — Cung Phu Thê interpretation guide
   - Relationship/marriage indicators
   - Timing: when marriage likely (Đại Hạn through Phu Thê)
   - Star combos: Thái Âm+Thái Dương = complementary partner
   - Hồng Loan / Thiên Hỷ significance for romance timing
   - Warning: Kình Dương/Đà La in Phu Thê = relationship conflict

4. **tai_bach.md** — Cung Tài Bạch interpretation guide
   - Wealth indicators (Hóa Lộc in Tài Bạch = strong income)
   - Wealth type: salary (Thiên Đồng), business (Vũ Khúc), inheritance (Thiên Phủ)
   - Lộc Tồn in Tài Bạch = steady accumulation
   - Warning: Địa Không/Địa Kiếp = financial loss risk

**Format per doc:** ~50 lines, Vietnamese, structured as:
```
# Cung [Name] — Hướng Dẫn Luận Giải
## Ý Nghĩa Tổng Quan
## Các Sao Quan Trọng
## Tổ Hợp Sao Đáng Chú Ý
## Tứ Hóa Ảnh Hưởng
## Đại Hạn Qua Cung Này
```

**LLM injection:** In `build_tuvi_prompt()`, when a palace-focused question is detected, load the relevant doc and append to the system prompt as context. This gives the LLM domain expertise without increasing the base prompt size.

**Detection in prompt builder:** If question contains "cung Mệnh" → load menh.md. If "cung Quan Lộc" → load quan_loc.md. Simple string match on cung_name.

---

## Execution Order

1. TL writes 4 palace guide docs (TV-DOC-1)
2. FE implements TVF-5 button + interpretPalace() function
3. BE adds palace doc injection to build_tuvi_prompt() (optional — LLM works without it, docs just improve quality)
4. TL reviews
5. QA tests: click Luận Giải on Mệnh, Quan Lộc → verify focused interpretation streams

## Acceptance Criteria

- [ ] "Luận Giải Cung Này" button visible in every palace popup
- [ ] Click → LLM streams focused interpretation for that specific palace domain
- [ ] Freemium gated (checkServerUsage before stream, increment after)
- [ ] "Xem lại thông tin cung" restores star view
- [ ] 4 palace guide docs exist in tu_vi/docs/palace_guides/
- [ ] Mobile bottom sheet: button works, stream renders correctly
- [ ] usageIncremented guard prevents double counting
