"""
TV-LLM Service - LLM interpretation for Tử Vi using Grok.
Uses shared LLM service from shared/backend/llm_service.py
"""

import sys
import os
import asyncio
from typing import AsyncGenerator

# Add project root to path for shared imports
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from shared.backend.llm_service import stream_llm_response


def build_tuvi_prompt(
    question: str,
    birth_info: dict,
    chart_data: dict,
    static_interpretation: str
) -> tuple[str, str]:
    """Build prompts for Tử Vi LLM interpretation."""

    # Format birth info
    birth_text = f"Ngày sinh: {birth_info.get('day')}/{birth_info.get('month')}/{birth_info.get('year')}"
    gender_text = "Nam" if birth_info.get('gender') == 'nam' else "Nữ"
    birth_text += f"\nGiới tính: {gender_text}"

    # Extract rich chart data
    nap_am = chart_data.get('nap_am', {})
    menh = nap_am.get('nam', 'N/A')
    ngu_hanh = nap_am.get('ngu_hanh', 'N/A')
    cuc_name = nap_am.get('name', 'N/A')

    # Get palaces data
    palaces = chart_data.get('palaces', [])

    # Build palaces text with all stars
    palaces_text = ""
    for palace in palaces:
        pos = palace.get('position', '?')
        cung_name = palace.get('cung_name', '?')
        dia_chi = palace.get('dia_chi', '?')
        stars = palace.get('stars', [])

        # List stars with brightness
        stars_list = []
        for s in stars:
            brightness = s.get('brightness', 'Bình')
            tu_hoa = f" ({s.get('tu_hoa', '')})" if s.get('tu_hoa') else ""
            stars_list.append(f"{s['name']}[{brightness}]{tu_hoa}")

        stars_str = ", ".join(stars_list) if stars_list else "Trống"

        # Get Đại Hạn info
        dai_han = palace.get('dai_han')
        dh_info = ""
        if dai_han:
            dh_range = dai_han.get('range', [])
            dh_current = " (HIỆN TẠI)" if dai_han.get('is_current') else ""
            dh_info = f" | Đại Hạn: {dh_range[0]}-{dh_range[1]} tuổi ({dai_han.get('can_chi', '')}){dh_current}"

        palaces_text += f"\n**Cung {pos}. {cung_name} ({dia_chi})**: {stars_str}{dh_info}"

    # Get stars data
    stars_dict = chart_data.get('stars', {})
    major_stars = []
    for star_name, star_data in stars_dict.items():
        pos = star_data.get('position', '?')
        brightness = star_data.get('brightness', 'Bình')
        tu_hoa = f" | {star_data.get('tu_hoa', '')}" if star_data.get('tu_hoa') else ""
        major_stars.append(f"{star_name} ở Cung {pos} [{brightness}]{tu_hoa}")

    stars_text = "\n".join(major_stars[:20])  # Top 20 stars

    # Get Tứ Hóa
    tu_hoa = chart_data.get('tu_hoa', {})
    tu_hoa_lines = []
    for key, value in tu_hoa.items():
        tu_hoa_lines.append(f"- {key}: {value.get('star')} tai {value.get('palace')}")
    tu_hoa_str = "\n".join(tu_hoa_lines) if tu_hoa_lines else "khong co"

    # Get Đại Hạn ranges
    dai_han = chart_data.get('dai_han', [])
    dai_han_str = "chua xac dinh"
    for dh in dai_han:
        if dh.get('is_current'):
            dai_han_str = f"Hiện tại: {dh.get('range', [])} tuoi ({dh.get('can_chi', '')})"

    # Get Tiểu Hạn
    tieu_han = chart_data.get('tieu_han', [])
    tieu_han_str = "chua xac dinh" if not tieu_han else f"Hiện tại: {tieu_han}"

    system_prompt = """Bạn là chuyên gia về Tử Vi (Vietnamese Astrology) với kiến thức sâu về kinh dịch, tứ trụ, và tử vi.

Quy tắc:
- Viết bằng tiếng Việt
- TUYỆT ĐỐI không dùng từ tiếng Anh. Viết hoàn toàn bằng tiếng Việt.
- Giọng văn: Học thuật nhưng ấm áp, gần gũi
- Sử dụng "bạn" thay vì "quý vị"
- Kết hợp kiến thức tử vi truyền thống với góc nhìn hiện đại
- Có thể đề cập thời gian (tháng, năm) - đây là tử vi thật"""

    # Build user prompt without f-string to avoid quote issues
    user_prompt = birth_text + "\n"
    user_prompt += f"**Nap Am:** {menh} ({ngu_hanh}) - {cuc_name}\n\n"
    user_prompt += f"**Tu Hoa:** {tu_hoa_str}\n\n"
    user_prompt += f"**Van Han:**\n"
    user_prompt += f"- Dai Han: {dai_han_str}\n"
    user_prompt += f"- Tieu Han: {tieu_han_str}\n\n"
    user_prompt += f"**12 Cung va Sao:**{palaces_text}\n\n"
    user_prompt += f"**Cac sao chinh:**{stars_text}\n\n"
    user_prompt += f"**Cau hoi:** {question}\n\n"
    user_prompt += f"**Luan giai tinh (tu co so du lieu):**\n{static_interpretation}\n\n"
    user_prompt += """**Yeu cau:** Hay bo sung luan giai bang LLM theo cac phan:

## Tong Quan
2-3 cau tom tat xu huong nang luong tong the.

## Cuong Menh
Phan tich chi tiet ve cac sao trong cung Menh va Phu Mau.

## Cac Cung Quan Trong
Phan tich ngan gon tung cung chinh.

## Van Han Chi Tiet
Phan tich Dai Han va Tieu Han hien tai.

## Loi Khuyen
3-4 goi y thuc te.

Viet bang tieng Viet, giong van hoc thuat nhung am ap."""

    return system_prompt, user_prompt


def build_palace_prompt(
    palace_name: str,
    palace_data: dict,
    palace_doc: str,
    chart_summary: dict,
) -> tuple[str, str]:
    """Build system + user prompts for per-palace LLM interpretation."""

    system_prompt = (
        "Bạn là chuyên gia Tử Vi Đẩu Số theo trường phái Nam Phái.\n\n"
        "Tài liệu luận giải cung:\n"
        "---\n"
        + palace_doc
        + "\n---\n\n"
        "Quy tắc:\n"
        "- Viết hoàn toàn bằng tiếng Việt, TUYỆT ĐỐI không dùng từ tiếng Anh.\n"
        "- Xưng hô 'bạn', giọng ấm áp, gần gũi.\n"
        "- Tập trung vào cung được yêu cầu.\n"
        "- Không đề cập thời gian cụ thể trong tương lai.\n"
        "- Không emoji, không đếm số từ."
    )

    cung_menh = chart_summary.get("cung_menh", "")
    nap_am = chart_summary.get("nap_am", {})
    nap_am_name = nap_am.get("name", "") if isinstance(nap_am, dict) else str(nap_am)

    stars = palace_data.get("stars", [])
    stars_lines = []
    for s in stars:
        name = s.get("name", "?")
        brightness = s.get("brightness", "")
        tu_hoa = f" ({s['tu_hoa']})" if s.get("tu_hoa") else ""
        stars_lines.append(f"- {name} [{brightness}]{tu_hoa}")
    stars_text = "\n".join(stars_lines) if stars_lines else "- Cung rỗng (không có chính tinh)"

    trang_sinh = palace_data.get("trang_sinh", "")
    bac_si = palace_data.get("bac_si", "")
    thai_tue = palace_data.get("thai_tue", "")
    tuong_tinh = palace_data.get("tuong_tinh", "")

    user_prompt = (
        f"Luận giải cung **{palace_name}** cho lá số:\n"
        f"- Cung Mệnh: {cung_menh}\n"
        f"- Nạp Âm: {nap_am_name}\n\n"
        f"**Sao trong cung {palace_name}:**\n{stars_text}\n\n"
        f"**Vòng Trường Sinh:** {trang_sinh}\n"
        f"**Vòng Bác Sĩ:** {bac_si}\n"
        f"**Vòng Thái Tuế:** {thai_tue}\n"
        f"**Tướng Tinh:** {tuong_tinh}\n\n"
        f"Hãy luận giải chi tiết cung {palace_name} theo tài liệu Nam Phái đã cung cấp.\n"
        f"Chia thành các mục: Tổng Quan, Sao Chính, Tứ Hóa Ảnh Hưởng, Lời Khuyên."
    )

    return system_prompt, user_prompt


async def stream_tuvi_palace_interpretation(
    palace_name: str,
    palace_data: dict,
    palace_doc: str,
    chart_summary: dict,
):
    """Stream per-palace LLM interpretation using shared framework."""
    system_prompt, user_prompt = build_palace_prompt(
        palace_name=palace_name,
        palace_data=palace_data,
        palace_doc=palace_doc,
        chart_summary=chart_summary,
    )
    return await stream_llm_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )


async def stream_tuvi_interpretation(
    question: str,
    birth_info: dict,
    chart_data: dict,
    static_interpretation: str,
    user_context: str = None
):
    """Stream Tử Vi LLM interpretation using shared framework."""
    system_prompt, user_prompt = build_tuvi_prompt(
        question, birth_info, chart_data, static_interpretation
    )
    # TV allows timeframes - no strip_dates needed
    return await stream_llm_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        user_context=user_context
    )
