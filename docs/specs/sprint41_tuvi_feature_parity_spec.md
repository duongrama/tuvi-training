# Sprint 41: Tu Vi Feature Parity

**Author:** PO | **Date:** 2026-03-15 | **Total:** 16pts
**App:** Tu Vi (port 17070) | **Folder:** `gieo_que/backend/tu_vi/`
**Rationale:** Tu Vi just got premium UX (Sprint 39) but lacks daily engagement, share, and push — features all other apps have. Tu Vi is #2 demand (10/10 VN) and deserves full feature parity.

---

## Context

Tu Vi was originally excluded from daily/streak/push because it's "algorithmic, not generative." But:
1. Tu Vi HAS an LLM interpretation ("Luận Giải") — it IS generative
2. Tu Vi can generate a "Daily Fortune" based on current Tiểu Hạn + Nguyệt Hạn
3. Share-as-image is universally useful (users love sharing their birth charts)
4. Sprint 39 made the UI premium — now it needs the engagement loop to retain users

---

## Items

### TV-FP-1: Daily Fortune (5pts) — BE + FE

**Backend:** Add daily fortune endpoint using shared daily_service pattern.

`GET /api/tuvi/daily?device_id=X`
- Calculates user's current Tiểu Hạn palace + stars for today
- Calls LLM once per day (cached) with: "Based on [user's Mệnh] and current Tiểu Hạn in [Palace] with [stars], give a brief daily fortune for today"
- Returns: { fortune_text, palace_name, key_star, date, streak_count }
- Streak tracking via shared daily_service

**Frontend:**
- Add "Vận Hạn Hôm Nay" card at top of page (before input form)
- Shows daily fortune text (streaming, 2-3 paragraphs max)
- Streak counter badge
- Collapse/expand — expanded by default on first visit, collapsed after
- Needs birth data stored (from profile or last chart) — if no birth data saved, show "Nhập ngày sinh để xem vận hạn hôm nay"

### TV-FP-2: Share as Image (5pts) — BE + FE

**Backend:** Add share endpoint using shared share_service pattern.

`POST /api/tuvi/share`
- Input: chart_data (palaces, birth info, Mệnh, Thân)
- Generates image: birth chart summary card (1080x1920 story format)
  - Dark theme background
  - Name + birth date
  - Mệnh palace + key stars
  - Thân palace + key stars
  - Current Đại Hạn/Tiểu Hạn summary
  - "Bói Toán · Tử Vi" branding at bottom
- Returns: image URL

**Frontend:**
- Add share button below chart (gold outline, "Chia sẻ lá số")
- On click: generate image → show preview → Web Share API (WhatsApp/Zalo)
- Clone pattern from Gieo Quẻ's share.js

### TV-FP-3: Push Notifications (3pts) — BE + FE

**Backend:** Wire Tu Vi into shared push_service.

- Register service worker (sw.js)
- Add manifest.json
- Subscribe endpoint: `POST /api/push/subscribe`
- Morning cron: send daily fortune preview as push notification
- Clone pattern from other apps' push implementation

**Frontend:**
- Add soft opt-in banner after first chart view: "Nhận vận hạn hàng ngày?"
- Never prompt on page load (UX rule from TL lessons)

### TV-FP-4: History Sidebar Enhancement (3pts) — FE

Tu Vi already has history via profile, but lacks the sidebar pattern other apps use.

- Add collapsible history sidebar (clone from Gieo Quẻ pattern)
- Shows recent chart lookups: date, name/birth info, Mệnh palace
- Click entry → re-renders that chart (no API call needed if cached)
- "Xóa lịch sử" option

---

## Execution Order

1. TL reviews spec
2. BE builds TV-FP-1 (daily) + TV-FP-2 (share backend) + TV-FP-3 (push backend)
3. FE builds TV-FP-1 (daily UI) + TV-FP-2 (share UI) + TV-FP-3 (push UI) + TV-FP-4 (history)
4. TL reviews
5. QA tests
6. PO accepts

---

## Acceptance Criteria

- [ ] Daily fortune loads with cached LLM response, shows streak
- [ ] Share generates dark-themed chart summary image
- [ ] Push opt-in banner appears after first chart, never on page load
- [ ] History sidebar shows recent chart lookups
- [ ] All features use shared services (daily_service, share_service, push_service)
- [ ] Freemium: daily fortune is free, LLM interpretation gated (existing behavior preserved)
