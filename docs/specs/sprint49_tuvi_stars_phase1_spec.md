# Sprint 49: Tu Vi Chart Overhaul Phase 1 — Extract iztro-py Hidden Data (BE Only)

**Author:** TL | **Date:** 2026-03-16 | **Total:** 5pts
**Scope:** Tu Vi backend (port 17070) — extract 86 additional stars + metadata already in iztro-py
**Rationale:** iztro-py provides 114 stars but we only extract 28. The remaining 86 are in `changsheng12`, `boshi12`, `jiangqian12`, `suiqian12`, `adjective_stars`, and `heavenly_stem` attributes — just not extracted yet. Zero custom placement logic needed.

---

## What iztro-py Already Provides (Verified)

Each palace object has these attributes we're NOT extracting:

| Attribute | Type | Content | Count |
|-----------|------|---------|-------|
| `changsheng12` | str (Chinese) | Vòng Tràng Sinh stage name | 12 (1/palace) |
| `boshi12` | str (Chinese) | Vòng Bác Sĩ star name | 12 (1/palace) |
| `jiangqian12` | str (Chinese) | Vòng Tướng Tinh star name | 12 (1/palace) |
| `suiqian12` | str (Chinese) | Vòng Thái Tuế star name | 12 (1/palace) |
| `adjective_stars` | list[FunctionalStar] | Grade B misc stars (Hồng Loan, Thiên Diêu, etc.) | ~38 total |
| `heavenly_stem` | str (enum) | Palace Thiên Can (for Can Chi) | 12 (1/palace) |

**Total new: 48 ring stars + 38 adjective stars = 86 stars. Combined with existing 28 = 114.**

---

## Items

### TV-EX-1: Extract All Star Groups + Palace Stem (3pts) — BE

**In `iztro_service.py:get_tuvi_chart()`, for each palace, extract:**

1. **Tràng Sinh:** `translate_chinese(palace.changsheng12)` → add to palace dict as `"trang_sinh"`
2. **Bác Sĩ:** `translate_chinese(palace.boshi12)` → add as `"bac_si"`
3. **Tướng Tinh:** `translate_chinese(palace.jiangqian12)` → add as `"tuong_tinh"`
4. **Thái Tuế:** `translate_chinese(palace.suiqian12)` → add as `"thai_tue"`
5. **Adjective stars:** Extract from `palace.adjective_stars` list — same pattern as existing minor_stars extraction (name, brightness, mutagen)
6. **Palace Can Chi:** `translate_chinese(HEAVENLY_STEM_MAP.get(palace.heavenly_stem, ''))` + `palace.dia_chi` → add as `"can_chi"`

**Translation:** All 4 ring values are Chinese strings (e.g., "临官", "博士", "丧门"). Use existing `translate_chinese()` or add new entries to `ALL_STAR_TRANSLATIONS`.

**New translation entries needed (~48):**
```
Tràng Sinh ring: 长生→Trường Sinh, 沐浴→Mộc Dục, 冠带→Quan Đới, 临官→Lâm Quan,
  帝旺→Đế Vượng, 衰→Suy, 病→Bệnh, 死→Tử, 墓→Mộ, 绝→Tuyệt, 胎→Thai, 养→Dưỡng

Bác Sĩ ring: 博士→Bác Sĩ, 力士→Lực Sĩ, 青龙→Thanh Long, 小耗→Tiểu Hao,
  将军→Tướng Quân, 奏书→Tấu Thư, 飞廉→Phi Liêm, 喜神→Hỷ Thần,
  病符→Bệnh Phù, 大耗→Đại Hao, 伏兵→Phục Binh, 官符→Quan Phù

Tướng Tinh ring: 将星→Tướng Tinh, 攀鞍→Ban An, 岁驿→Tuế Dịch, 息神→Tức Thần,
  华盖→Hoa Cái, 劫煞→Kiếp Sát, 灾煞→Tai Sát, 天煞→Thiên Sát,
  指背→Chỉ Bối, 咸池→Hàm Trì, 月煞→Nguyệt Sát, 亡神→Vong Thần

Thái Tuế ring: 岁建→Tuế Kiến, 晦气→Hối Khí, 丧门→Tang Môn, 贯索→Quán Sách,
  官符→Quan Phù, 小耗→Tiểu Hao, 大耗→Đại Hao, 龙德→Long Đức,
  白虎→Bạch Hổ, 天德→Thiên Đức, 吊客→Điếu Khách, 病符→Bệnh Phù

Adjective stars (add missing): hongluan→Hồng Loan, tianxi→Thiên Hỷ,
  tianxing→Thiên Hình, tianyao→Thiên Diêu, etc.
```

### TV-EX-2: Add Mệnh Chủ + Thân Chủ (1pt) — BE

Simple lookup tables — same as original spec TV-S5. No change needed.

### TV-EX-3: Unit Tests (1pt) — BE

**Test cases (minimum 8):**
1. Boss test case (18/5/1984 Nam): verify trang_sinh, bac_si, thai_tue, tuong_tinh fields exist and are Vietnamese strings
2. Palace can_chi field exists and matches format "X Y" (e.g., "Bính Dần")
3. adjective_stars extracted (count > 0 for at least some palaces)
4. Mệnh Chủ correct for Mệnh at Tỵ → Vũ Khúc
5. Thân Chủ correct for year branch Tý → Hỏa Tinh
6. All 4 ring fields are non-empty Vietnamese strings (not Chinese)
7. Total star count per chart ≥ 100
8. No regression on existing 73 tests

---

## API Response Changes

```json
{
  "palaces": [
    {
      "position": 1,
      "dia_chi": "Tý",
      "can_chi": "Bính Tý",           // NEW
      "cung_name": "...",
      "stars": [...],                  // existing major + minor
      "adjective_stars": [             // NEW — Grade B misc stars
        {"name": "Hồng Loan", "brightness": null, "tu_hoa": null}
      ],
      "trang_sinh": "Mộc Dục",        // NEW — Tràng Sinh stage
      "bac_si": "Lực Sĩ",            // NEW — Bác Sĩ ring
      "tuong_tinh": "Tuế Dịch",       // NEW — Tướng Tinh ring
      "thai_tue": "Tang Môn",          // NEW — Thái Tuế ring
      "dai_han": {...}
    }
  ],
  "menh_chu": "Vũ Khúc",             // NEW
  "than_chu": "Hỏa Tinh",            // NEW
  // existing fields unchanged
}
```

---

## What's NOT Needed (Removed from Original Spec)

- ~~Custom `star_placement.py` module~~ — iztro-py already does all placement
- ~~Tràng Sinh placement algorithm~~ — already computed
- ~~Bác Sĩ direction logic~~ — already computed
- ~~Thái Tuế placement~~ — already computed
- ~~Tuần/Triệt calculation~~ — defer to Phase 2 (needs investigation if iztro-py provides it)
- ~~Ngũ Hổ Độn formula~~ — iztro-py `palace.heavenly_stem` already has it

## Execution Order

1. BE adds translation entries for ~48 ring star names + adjective star names
2. BE extracts 6 new fields per palace in the palace loop
3. BE adds Mệnh Chủ / Thân Chủ lookup
4. BE writes 8 tests
5. TL reviews + runs tests

## Acceptance Criteria

- [ ] All 4 ring fields populated with Vietnamese names in every palace
- [ ] Palace can_chi field shows "Thiên Can + Địa Chi" format
- [ ] Adjective stars extracted with correct Vietnamese names
- [ ] Mệnh Chủ / Thân Chủ in chart response
- [ ] 8+ new tests passing, 73 existing tests no regression
- [ ] Boss test case verified
