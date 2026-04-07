"""
Hợp Tuổi Compatibility Service (Sprint 98 — COMP-1)

Birth-year-only compatibility scoring — no iztro-py required.
Input: two birth years. Output: zodiac verdict + element verdict + score.
"""
import json
from pathlib import Path
from typing import Dict, Tuple

_DATA_DIR = Path(__file__).parent / "data"

with open(_DATA_DIR / "nap_am.json", "r", encoding="utf-8") as f:
    _NAP_AM_DATA = {e["year_offset"]: e for e in json.load(f)["cycle"]}

_CHIS = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ",
         "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

_TAM_HOP = [
    {"Tý", "Thìn", "Thân"},
    {"Dần", "Ngọ", "Tuất"},
    {"Mão", "Mùi", "Hợi"},
    {"Dậu", "Tỵ", "Sửu"},
]

_LUC_HOP = [{"Tý", "Sửu"}, {"Dần", "Hợi"}, {"Mão", "Tuất"},
            {"Thìn", "Dậu"}, {"Ngọ", "Mùi"}, {"Thân", "Tỵ"}]

_LUC_XUNG = [{"Tý", "Ngọ"}, {"Dần", "Thân"}, {"Mão", "Dậu"},
             {"Thìn", "Tuất"}, {"Tỵ", "Hợi"}, {"Mùi", "Sửu"}]

_LUC_HAI = [{"Tý", "Mùi"}, {"Sửu", "Ngọ"}, {"Dần", "Tỵ"},
            {"Mão", "Thìn"}, {"Thân", "Hợi"}, {"Dậu", "Tuất"}]

_ELEM_TUONG_SINH = {
    "Kim": "Thủy", "Mộc": "Hoả", "Thủy": "Mộc",
    "Hoả": "Thổ", "Thổ": "Kim",
}

_ELEM_TUONG_KHAC = {
    "Kim": "Mộc", "Mộc": "Thổ", "Thủy": "Hoả",
    "Hoả": "Kim", "Thổ": "Thủy",
}

_ZODIAC_NAMES = {c: c for c in _CHIS}


def year_to_zodiac(year: int) -> Tuple[str, str]:
    chi = _CHIS[(year - 4) % 12]
    return chi, chi


def year_to_nap_am(year: int) -> Dict:
    offset = (year - 1984) % 60
    entry = _NAP_AM_DATA[offset]
    return {"nap_am": entry["nap_am"], "element": entry["element"],
             "can_chi": entry["can_chi"]}


def _verdict_type(chi1: str, chi2: str) -> str:
    if chi1 == chi2:
        return "cung_tuoi"
    for g in _TAM_HOP:
        if chi1 in g and chi2 in g:
            return "tam_hop"
    for p in _LUC_HOP:
        if chi1 in p and chi2 in p:
            return "luc_hop"
    for p in _LUC_XUNG:
        if chi1 in p and chi2 in p:
            return "luc_xung"
    for p in _LUC_HAI:
        if chi1 in p and chi2 in p:
            return "luc_hai"
    return "trung_tinh"


_ZODIAC_LABELS = {
    "tam_hop": "Tam Hợp", "luc_hop": "Lục Hợp",
    "luc_xung": "Lục Xung", "luc_hai": "Lục Hại",
    "cung_tuoi": "Cùng Tuổi", "trung_tinh": "Trung Tính",
}

_ZODIAC_DETAILS = {
    "tam_hop": "{a}-{b} thuộc nhóm Tam Hợp, có sự hoà hợp về tính cách.",
    "luc_hop": "{a}-{b} là cặp Lục Hợp, bổ sung cho nhau về năng lượng.",
    "luc_xung": "{a}-{b} thuộc cặp Lục Xung, có nhiều xung đột cần điều hoà.",
    "luc_hai": "{a}-{b} thuộc cặp Lục Hại, cần thận trọng trong mối quan hệ.",
    "cung_tuoi": "Hai người cùng tuổi {a}, có sự đồng điệu nhưng cũng cạnh tranh.",
    "trung_tinh": "{a}-{b} — không thuộc nhóm hợp/xung đặc biệt.",
}

_ZODIAC_SCORES = {
    "tam_hop": 25, "luc_hop": 22, "cung_tuoi": 20,
    "trung_tinh": 15, "luc_hai": 10, "luc_xung": 5,
}

_ELEM_LABELS = {
    "tuong_sinh": "Tương Sinh", "tuong_sinh_nguoc": "Tương Sinh",
    "tuong_khac": "Tương Khắc", "tuong_khac_nguoc": "Tương Khắc",
    "cung_ngu_hanh": "Cùng Ngũ Hành", "trung_tinh": "Trung Tính",
}

_ELEM_SCORES = {
    "tuong_sinh": 25, "tuong_sinh_nguoc": 22,
    "cung_ngu_hanh": 20, "trung_tinh": 15,
    "tuong_khac": 5, "tuong_khac_nguoc": 8,
}


def _elem_verdict(e1: str, e2: str) -> Tuple[str, str, str]:
    if e1 == e2:
        return "cung_ngu_hanh", _ELEM_LABELS["cung_ngu_hanh"], \
            f"Cả hai cùng mệnh {e1}, có sự đồng điệu về tính cách."
    if _ELEM_TUONG_SINH.get(e1) == e2:
        return "tuong_sinh", _ELEM_LABELS["tuong_sinh"], \
            f"{e1}→{e2} — {e1} sinh {e2}, hai người hỗ trợ nhau phát triển."
    if _ELEM_TUONG_SINH.get(e2) == e1:
        return "tuong_sinh_nguoc", _ELEM_LABELS["tuong_sinh_nguoc"], \
            f"{e2}→{e1} — {e2} sinh {e1}, hai người có sự tương hỗ lẫn nhau."
    if _ELEM_TUONG_KHAC.get(e1) == e2:
        return "tuong_khac", _ELEM_LABELS["tuong_khac"], \
            f"{e1}→{e2} — {e1} khắc {e2}, có xu hướng xung đột về tính cách."
    if _ELEM_TUONG_KHAC.get(e2) == e1:
        return "tuong_khac_nguoc", _ELEM_LABELS["tuong_khac_nguoc"], \
            f"{e2}→{e1} — {e2} khắc {e1}, có sự mâu thuẫn tiềm ẩn."
    return "trung_tinh", _ELEM_LABELS["trung_tinh"], \
        f"{e1} và {e2} không có quan hệ ngũ hành đặc biệt."


def _rating(score: int) -> str:
    if score >= 45: return "Rất Hợp"
    if score >= 35: return "Hợp"
    if score >= 25: return "Bình thường"
    if score >= 15: return "Không Hợp"
    return "Xung Đột"


def score_hop_tuoi(year_a: int, year_b: int) -> Dict:
    chi_a = year_to_zodiac(year_a)[0]
    chi_b = year_to_zodiac(year_b)[0]
    nap_a = year_to_nap_am(year_a)
    nap_b = year_to_nap_am(year_b)

    z_type = _verdict_type(chi_a, chi_b)
    z_score = _ZODIAC_SCORES[z_type]
    e_type, e_label, e_detail = _elem_verdict(nap_a["element"], nap_b["element"])
    e_score = _ELEM_SCORES[e_type]

    combined = z_score + e_score

    return {
        "person_a": {"year": year_a, "zodiac": chi_a, "zodiac_name": f"Tuổi {chi_a}",
                       "nap_am": nap_a["nap_am"], "element": nap_a["element"]},
        "person_b": {"year": year_b, "zodiac": chi_b, "zodiac_name": f"Tuổi {chi_b}",
                       "nap_am": nap_b["nap_am"], "element": nap_b["element"]},
        "zodiac_verdict": {"type": z_type, "label": _ZODIAC_LABELS[z_type],
                            "detail": _ZODIAC_DETAILS[z_type].format(a=chi_a, b=chi_b),
                            "score": z_score},
        "element_verdict": {"type": e_type, "label": e_label,
                            "detail": e_detail, "score": e_score},
        "combined_score": combined,
        "combined_rating": _rating(combined),
        "summary": f"Tuổi {chi_a} và tuổi {chi_b} có quan hệ {_ZODIAC_LABELS[z_type]}. "
                    f"Ngũ hành {nap_a['element']} và {nap_b['element']}: {e_label}.",
    }
