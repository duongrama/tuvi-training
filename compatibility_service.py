"""
Sprint 64 CMP-1: Tu Vi Compatibility Scoring Service.

Pure functions — no IO, no LLM, no DB. Easily unit-tested.
"""
from typing import Tuple, List

# ── Element extraction ─────────────────────────────────────────────────────────

_ELEMENT_MAP = {"金": "Kim", "木": "Mộc", "水": "Thủy", "火": "Hỏa", "土": "Thổ"}


def extract_element(five_elements_class: str) -> str:
    """Extract Vietnamese element name from iztro-py five_elements_class (e.g. '金四局' → 'Kim')."""
    return _ELEMENT_MAP.get(five_elements_class[:1], "Thổ")


# ── Zodiac Chinese → Vietnamese branch name ────────────────────────────────────

ZODIAC_BRANCH_MAP = {
    "鼠": "Tý",  "牛": "Sửu", "虎": "Dần", "兔": "Mão",
    "龙": "Thìn","龍": "Thìn","蛇": "Tỵ",  "马": "Ngọ", "馬": "Ngọ",
    "羊": "Mùi", "猴": "Thân","鸡": "Dậu", "雞": "Dậu",
    "狗": "Tuất","猪": "Hợi", "豬": "Hợi",
}


def zodiac_to_branch(zodiac_cn: str) -> str:
    """Map iztro-py .zodiac Chinese char to Vietnamese earthly branch name."""
    return ZODIAC_BRANCH_MAP.get(zodiac_cn, "Tý")


# ── Compatibility tables ───────────────────────────────────────────────────────

_TAM_HOP = [
    {"Thân", "Tý", "Thìn"},
    {"Dần", "Ngọ", "Tuất"},
    {"Tỵ", "Dậu", "Sửu"},
    {"Hợi", "Mão", "Mùi"},
]
_LUC_HOP = [
    {"Tý", "Sửu"}, {"Dần", "Hợi"}, {"Mão", "Tuất"},
    {"Thìn", "Dậu"}, {"Tỵ", "Thân"}, {"Ngọ", "Mùi"},
]
_LUC_XUNG = [
    {"Tý", "Ngọ"}, {"Sửu", "Mùi"}, {"Dần", "Thân"},
    {"Mão", "Dậu"}, {"Thìn", "Tuất"}, {"Tỵ", "Hợi"},
]

# Ngũ Hành generating / destructive pairs (A → B)
_TUONG_SINH = {
    ("Kim", "Thủy"), ("Thủy", "Mộc"), ("Mộc", "Hỏa"),
    ("Hỏa", "Thổ"), ("Thổ", "Kim"),
}
_TUONG_KHAC = {
    ("Kim", "Mộc"), ("Mộc", "Thổ"), ("Thổ", "Thủy"),
    ("Thủy", "Hỏa"), ("Hỏa", "Kim"),
}

# Phu Thê star classification (English iztro-py star IDs)
_AUSPICIOUS_STARS = {"tianfuMaj", "tianxiangMaj", "tianliangMaj", "taiyinMaj"}
_MIXED_STARS      = {"ziweiMaj", "wuquMaj", "tanlangMaj"}
_CHALLENGING_STARS = {"qishaMaj", "pojunMaj", "lianzhenMaj"}

# English earthly branch enum → Vietnamese
_BRANCH_ENUM_MAP = {
    "ziEarthly": "Tý",   "chouEarthly": "Sửu", "yinEarthly": "Dần",
    "maoEarthly": "Mão", "chenEarthly": "Thìn", "siEarthly": "Tỵ",
    "wuEarthly": "Ngọ",  "weiEarthly": "Mùi",  "shenEarthly": "Thân",
    "youEarthly": "Dậu", "xuEarthly": "Tuất",  "haiEarthly": "Hợi",
}


# ── Factor 1: Ngũ Hành Tương Sinh/Khắc ─────────────────────────────────────────

def score_ngu_hanh(elem_a: str, elem_b: str) -> Tuple[int, str]:
    """Score Ngũ Hành compatibility. Checks both directions for Tương Sinh."""
    if elem_a == elem_b:
        return 20, f"{elem_a} đồng hành — Tương Hòa"
    if (elem_a, elem_b) in _TUONG_SINH or (elem_b, elem_a) in _TUONG_SINH:
        gen = f"{elem_a}→{elem_b}" if (elem_a, elem_b) in _TUONG_SINH else f"{elem_b}→{elem_a}"
        return 25, f"{gen} — Tương Sinh"
    if (elem_a, elem_b) in _TUONG_KHAC or (elem_b, elem_a) in _TUONG_KHAC:
        clash = f"{elem_a}→{elem_b}" if (elem_a, elem_b) in _TUONG_KHAC else f"{elem_b}→{elem_a}"
        return 5, f"{clash} — Tương Khắc"
    return 15, f"{elem_a} & {elem_b} — Trung tính"


# ── Factor 2: Zodiac Compatibility ─────────────────────────────────────────────

def score_zodiac_compat(branch_a: str, branch_b: str) -> Tuple[int, str]:
    """Score zodiac branch compatibility via Tam Hợp / Lục Hợp / Lục Xung."""
    pair = {branch_a, branch_b}
    for triad in _TAM_HOP:
        if pair.issubset(triad):
            return 25, f"{branch_a}-{branch_b} — Tam Hợp"
    for lhop in _LUC_HOP:
        if pair == lhop:
            return 22, f"{branch_a}-{branch_b} — Lục Hợp"
    for lxung in _LUC_XUNG:
        if pair == lxung:
            return 5, f"{branch_a}-{branch_b} — Lục Xung"
    return 15, f"{branch_a}-{branch_b} — Trung tính"


# ── Factor 3: Phu Thê Palace Stars ─────────────────────────────────────────────

def _score_single_spouse_palace(star_names: List[str]) -> int:
    """Score one person's Phu Thê palace stars."""
    for sn in star_names:
        if sn in _AUSPICIOUS_STARS:
            return 25
        if sn in _MIXED_STARS:
            return 15
        if sn in _CHALLENGING_STARS:
            return 8
    return 15  # neutral / no recognized stars


def score_phu_the(stars_a: List[str], stars_b: List[str]) -> Tuple[int, str]:
    """Average Phu Thê palace star scores for both people."""
    from tu_vi.iztro_service import ENGLISH_STAR_TRANSLATIONS
    sa = _score_single_spouse_palace(stars_a)
    sb = _score_single_spouse_palace(stars_b)
    avg = (sa + sb) // 2
    detail_a = ENGLISH_STAR_TRANSLATIONS.get(stars_a[0], stars_a[0]) if stars_a else "không có sao"
    detail_b = ENGLISH_STAR_TRANSLATIONS.get(stars_b[0], stars_b[0]) if stars_b else "không có sao"
    return avg, f"A: {detail_a} ({sa}đ), B: {detail_b} ({sb}đ)"


# ── Factor 4: Mệnh Palace Harmony ──────────────────────────────────────────────

def score_menh_harmony(branch_a: str, branch_b: str) -> Tuple[int, str]:
    """Score compatibility of two Mệnh palace earthly branches."""
    if branch_a == branch_b:
        return 20, f"{branch_a} — Đồng Chi"
    pair = {branch_a, branch_b}
    for triad in _TAM_HOP:
        if pair.issubset(triad):
            return 25, f"{branch_a}-{branch_b} — Tam Hợp"
    for lhop in _LUC_HOP:
        if pair == lhop:
            return 22, f"{branch_a}-{branch_b} — Lục Hợp"
    for lxung in _LUC_XUNG:
        if pair == lxung:
            return 5, f"{branch_a}-{branch_b} — Lục Xung"
    return 15, f"{branch_a}-{branch_b} — Trung tính"


# ── Rating ─────────────────────────────────────────────────────────────────────

def get_rating(score: int) -> str:
    if score >= 80:
        return "Rất hợp"
    if score >= 60:
        return "Khá hợp"
    if score >= 40:
        return "Bình thường"
    if score >= 20:
        return "Cần cân nhắc"
    return "Nhiều thử thách"


# ── Full computation ───────────────────────────────────────────────────────────

def compute_compatibility(chart_a, chart_b, name_a: str = "", name_b: str = "") -> dict:
    """Compute full compatibility result from two iztro-py charts.

    Returns dict with score, rating, factors, person_a summary, person_b summary.
    """
    from tu_vi.iztro_service import ENGLISH_STAR_TRANSLATIONS

    # Extract elements
    elem_a = extract_element(chart_a.five_elements_class)
    elem_b = extract_element(chart_b.five_elements_class)

    # Zodiac → Vietnamese branch
    zod_a = zodiac_to_branch(chart_a.zodiac)
    zod_b = zodiac_to_branch(chart_b.zodiac)

    # Phu Thê palace stars (English IDs)
    spouse_a = [s.name for p in chart_a.palaces if p.name == "spousePalace"
                for s in p.major_stars]
    spouse_b = [s.name for p in chart_b.palaces if p.name == "spousePalace"
                for s in p.major_stars]

    # Mệnh palace earthly branch → Vietnamese
    menh_a = _BRANCH_ENUM_MAP.get(chart_a.earthly_branch_of_soul_palace, "Tý")
    menh_b = _BRANCH_ENUM_MAP.get(chart_b.earthly_branch_of_soul_palace, "Tý")

    # Cục names
    from tu_vi.iztro_service import CUC_NAMES
    cuc_a = CUC_NAMES.get(chart_a.five_elements_class, {"name": "Kim Tứ Cục"})["name"]
    cuc_b = CUC_NAMES.get(chart_b.five_elements_class, {"name": "Kim Tứ Cục"})["name"]

    # Score 4 factors
    f1_score, f1_detail = score_ngu_hanh(elem_a, elem_b)
    f2_score, f2_detail = score_zodiac_compat(zod_a, zod_b)
    f3_score, f3_detail = score_phu_the(spouse_a, spouse_b)
    f4_score, f4_detail = score_menh_harmony(menh_a, menh_b)

    total = f1_score + f2_score + f3_score + f4_score

    # Vietnamese star name for display
    spouse_a_vn = [ENGLISH_STAR_TRANSLATIONS.get(s, s) for s in spouse_a[:1]]
    spouse_b_vn = [ENGLISH_STAR_TRANSLATIONS.get(s, s) for s in spouse_b[:1]]

    return {
        "score": total,
        "rating": get_rating(total),
        "factors": {
            "ngu_hanh":     {"score": f1_score, "detail": f1_detail},
            "zodiac":       {"score": f2_score, "detail": f2_detail},
            "phu_the":      {"score": f3_score, "detail": f3_detail},
            "menh_harmony": {"score": f4_score, "detail": f4_detail},
        },
        "person_a": {
            "name": name_a,
            "menh": menh_a,
            "cuc": cuc_a,
            "zodiac": zod_a,
            "element": elem_a,
        },
        "person_b": {
            "name": name_b,
            "menh": menh_b,
            "cuc": cuc_b,
            "zodiac": zod_b,
            "element": elem_b,
        },
    }
