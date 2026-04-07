# Zi Wei Dou Shu (紫微斗数) Open-Source Library Research

**Date:** 2026-03-16
**Purpose:** Identify open-source ZWDS libraries with complete star placement (108+ stars) for porting/adapting into our Tử Vi MVP.

---

## TL;DR / Recommendation

**Best candidate for porting:** `iztro` (TypeScript/JS, MIT, 3.4k GitHub stars, actively maintained to March 2026).

**Best Python option today:** `py-iztro` (Python, 107 GitHub stars, based on iztro v2.5.0, confirmed 截空+旬空+长生12神+博士12神).

**Key insight:** iztro covers **117 fixed stars + 21 flowing stars (138 total)**, including all four 12-deity cycles (长生/博士/将前/岁前), 截空, and 旬空. This is far more complete than our current py-iztro singleton which only places 14 main stars.

---

## Libraries: Full Comparison Table

| Library | URL | Lang | GH Stars | Forks | License | Last Commit | Stars Placed | 长生12神 | 博士12神 | 截空/旬空 | Notes |
|---------|-----|------|----------|-------|---------|-------------|-------------|---------|---------|---------|-------|
| **iztro** | [SylarLong/iztro](https://github.com/SylarLong/iztro) | TypeScript | 3,400 | 520 | MIT | Mar 2026 | **138** (117 fixed + 21 flowing) | YES | YES | YES | Primary source of truth |
| **py-iztro** | [x-haose/py-iztro](https://github.com/x-haose/py-iztro) | Python | 107 | 26 | Unknown | Jan 2025 | ~138 (iztro v2.5.0 parity) | YES | YES | YES | Best Python option; runs JS engine internally |
| **iztro-py** | [spyfree/iztro-py](https://github.com/spyfree/iztro-py) | Python | 2 | - | Unknown | Mar 2026 | Unknown | Unknown | Unknown | Pure Python, but very new, minimal docs |
| **dart_iztro** | [EdwinXiang/dart_iztro](https://github.com/EdwinXiang/dart_iztro) | Dart/Flutter | 137 | 30 | MIT | Dec 2024 | ~138 (iztro parity claimed) | YES (via iztro) | YES (via iztro) | YES (via iztro) | Good for Flutter apps; credits iztro |
| **Fortel (Java)** | [airicyu/Fortel](https://github.com/airicyu/Fortel) | Java | 32 | 23 | MIT | Jan 2025 | 13+ major + minor (中州派) | YES | YES | Unknown | 中州派 school; JSON output; actively maintained |
| **fortel-ziweidoushu** | [airicyu/fortel-ziweidoushu](https://github.com/airicyu/fortel-ziweidoushu) | TypeScript | 26 | 20 | MIT | Unknown | Partial (中州派) | Unknown | Unknown | Unknown | JS companion to Fortel Java |
| **natal-chart** | [haibolian/natal-chart](https://github.com/haibolian/natal-chart) | JavaScript/Vue | 29 | 11 | None | Apr 2022 | 14 main stars only | NO | NO | NO | Explicitly "基本星系完成" only; abandoned |
| **wlhyl/ziwei** | [wlhyl/ziwei](https://github.com/wlhyl/ziwei) | Rust + TS | 7 | 3 | None | Jun 2023 | Unknown | Unknown | Unknown | Unknown | Actix-web server; niche |
| **chksong/ZiWeiDouShu** | [chksong/ZiWeiDouShu](https://github.com/chksong/ZiWeiDouShu) | Obj-C | 1 | 1 | None | Apr 2018 | Unknown | NO | NO | NO | iOS app stub; no README; dead |
| **gzqyl/free-ziwei** | [gzqyl/free-ziwei](https://github.com/gzqyl/free-ziwei) | Android | 2 | 1 | None | Mar 2020 | Unknown | Unknown | Unknown | NO | Android APK release only; no usable code |

---

## Detailed Library Profiles

### 1. iztro — PRIMARY REFERENCE (TypeScript/JS)

- **URL:** https://github.com/SylarLong/iztro
- **Language:** TypeScript (99.5%)
- **GitHub Stars:** 3,400 | **Forks:** 520
- **License:** MIT
- **Last Commit:** March 5, 2026 (v2.5.8 — actively maintained)
- **Documentation:** https://iztro.com/en_US/ — excellent, multi-language

**Star Coverage (138 total):**
- 14 主星 (Major Stars): 紫微, 天机, 太阳, 武曲, 天同, 廉贞, 天府, 太阴, 贪狼, 巨门, 天相, 天梁, 七杀, 破军
- 14 辅星 (Minor Stars): e.g., 文昌, 文曲, 左辅, 右弼, 天魁, 天钺, 禄存, 天马, etc.
- 37 杂耀 (Miscellaneous Stars)
- 48 神煞 (Celestial Deities) divided into 4 cycles of 12:
  - 长生12神 (Chang Sheng cycle: 长生, 沐浴, 冠带, 临官, 帝旺, 衰, 病, 死, 墓, 绝, 胎, 养)
  - 博士12神 (Bo Shi cycle)
  - 将前12神 (Jiang Qian cycle)
  - 岁前12神 (Sui Qian / Tai Sui cycle)
- 21 流耀 (Flowing/Annual Stars)

**Confirmed included:** 截空 (Jie Kong), 旬空 (Xun Kong)

**Supports:**
- Vòng Tràng Sinh (长生12神): YES
- Vòng Thái Tuế (岁前12神): YES
- Vòng Bác Sĩ (博士12神): YES
- Tuần/Triệt (截空/旬空): YES
- Multiple schools/派: YES (configurable in v2.3.0+)
- Multi-language: Simplified Chinese, Traditional Chinese, English, Japanese, Korean, Vietnamese

**Portability assessment:** TypeScript source is clean and well-structured. Direct port to Python is feasible. The existing py-iztro (see #2) is proof.

---

### 2. py-iztro — BEST PYTHON OPTION

- **URL:** https://github.com/x-haose/py-iztro
- **Language:** Python
- **GitHub Stars:** 107 | **Forks:** 26
- **License:** Not explicitly stated (check repo directly)
- **Last Commit:** January 9, 2025
- **Based on:** iztro v2.5.0

**Key facts:**
- Runs iztro JS logic via a Python JS interpreter bridge
- Usage API is "identical to original" (用法和原版完全一致)
- Confirmed in output examples: 截空, 旬空, 长生12神, 博士12神

**Limitation:** Uses a Python JS interpreter internally — this is a bridge/wrapper, not a pure Python rewrite. May have performance overhead. The `iztro-py` project (spyfree) is the pure Python rewrite but is very early-stage (2 stars, released Mar 2026).

---

### 3. iztro-py — PURE PYTHON REWRITE (Early Stage)

- **URL:** https://github.com/spyfree/iztro-py
- **PyPI:** `pip install iztro-py` (v0.3.4)
- **Language:** Python (pure, no JS interpreter)
- **GitHub Stars:** 2
- **License:** Unknown
- **Last Commit:** March 7, 2026 (very recent)

**Key facts:**
- Pure Python, uses Pydantic models for type safety
- Claims 6-language i18n support matching iztro JS
- Star coverage parity with iztro JS not yet documented/verified
- Too new to assess reliability

---

### 4. dart_iztro — Dart/Flutter Port

- **URL:** https://github.com/EdwinXiang/dart_iztro
- **Language:** Dart
- **GitHub Stars:** 137 | **Forks:** 30
- **License:** MIT
- **Last Commit:** December 28, 2024

**Key facts:**
- Directly credits and ports iztro JS
- Supports: 12-palace charts, fortune cycles, flow stars, true solar time
- Feature parity with iztro JS claimed
- Cross-platform: Android, iOS, macOS, Windows, Linux, Web
- Useful only if we target Flutter; not directly portable to Python

---

### 5. Fortel — Java (中州派 School)

- **URL:** https://github.com/airicyu/Fortel
- **Language:** Java
- **GitHub Stars:** 32 | **Forks:** 23
- **License:** MIT
- **Last Commit:** January 29, 2025

**Key facts:**
- Implements 中州派 (Zhongzhou school) methodology — different from standard
- JSON output format confirmed
- Confirmed output includes: 长生12神 (persist12), 博士12神 (preDoctorStar), 太岁12神 (preAgeStar)
- Has companion JS library: `fortel-ziweidoushu`
- Note: 中州派 star placement rules differ from 三合派 (San He) which is more common in Vietnamese practice

---

## What Our Current py-iztro Singleton Misses

Our current `Astro()` singleton (per pitfalls.md) uses py-iztro but likely only exposes the 14 main stars. The full iztro data includes:

| Category | Vietnamese Name | Count | In Our Current Code? |
|----------|----------------|-------|---------------------|
| 14主星 | Sao chính tinh | 14 | YES (partial) |
| 14辅星 | Sao phụ tinh | 14 | PARTIAL |
| 37杂耀 | Sao tạp diệu | 37 | LIKELY NO |
| 长生12神 | Vòng Tràng Sinh | 12 | NO |
| 博士12神 | Vòng Bác Sĩ | 12 | NO |
| 将前12神 | Vòng Tướng Tinh | 12 | NO |
| 岁前12神 | Vòng Thái Tuế | 12 | NO |
| 截空/旬空 | Tuần/Triệt | 2+2 | NO |
| 21流耀 | Sao lưu niên | 21 | NO |

---

## Recommended Action Plan

### Option A: Extend py-iztro (Quickest)
Use `x-haose/py-iztro` which already wraps iztro v2.5.0 and confirms all the missing star cycles in its output. Pull the raw JSON output and parse all 138 stars.

**Risk:** py-iztro uses a JS interpreter bridge — may be slow or fragile.

### Option B: Direct Port from iztro TypeScript (Most Control)
Port the TypeScript source from `SylarLong/iztro` to pure Python. This is feasible — the TS code is clean, well-tested, and MIT licensed. Estimated effort: 2-3 sprints for complete star coverage.

**Benefit:** Full control, pure Python, no JS dependency, can optimize for Vietnamese naming conventions (we already have the Vietnamese i18n from iztro).

### Option C: Use iztro-py (Wait and See)
Monitor `spyfree/iztro-py` — if it reaches feature parity with iztro JS (pure Python), this becomes the best option. Too early as of March 2026 (v0.3.4, 2 stars).

---

## Sources Consulted

- https://github.com/SylarLong/iztro
- https://github.com/x-haose/py-iztro
- https://github.com/spyfree/iztro-py (via libraries.io)
- https://github.com/EdwinXiang/dart_iztro
- https://github.com/airicyu/Fortel
- https://github.com/airicyu/fortel-ziweidoushu
- https://github.com/haibolian/natal-chart
- https://github.com/wlhyl/ziwei
- https://github.com/chksong/ZiWeiDouShu
- https://github.com/gzqyl/free-ziwei
- https://iztro.com/learn/star.html (star catalog documentation)
- https://iztro.com/en_US/ (iztro official docs)
