"""
Interpretation Service - Tử Vi Basic Meanings

Provides static Vietnamese interpretation texts for palaces and stars.
No LLM - pure lookup tables.
"""

from typing import Dict, List, Optional


# 12 Palace meanings
PALACE_MEANINGS = {
    1: {
        "name": "Mệnh",
        "meaning": "Cung Mệnh thể hiện bản mệnh, tính cách, xu hướng cuộc đời, năng lực bẩm sinh và vận mệnh tổng quan. Đây là cung quan trọng nhất trong lá số, quyết định đường đời và số phận của người được luận giải."
    },
    2: {
        "name": "Phụ Mẫu",
        "meaning": "Cung Phụ Mẫu liên quan đến cha mẹ, tổ tiên, mối quan hệ gia đình và di sản. Thể hiện ảnh hưởng của cha mẹ, sự hỗ trợ từ gia đình, và môi trường nuôi dưỡng trong cuộc đời."
    },
    3: {
        "name": "Huynh Đệ",
        "meaning": "Cung Huynh Đệ liên quan đến anh chị em, bạn bè thân thiết và mối quan hệ xã hội. Thể hiện sự hỗ trợ từ người thân, tình anh em ruột thịt và quần thần trong cuộc đời."
    },
    4: {
        "name": "Tử Tức",
        "meaning": "Cung Tử Tức liên quan đến con cái, hậu duệ, sự tiếp nối dòng tộc và mối quan hệ với thế hệ sau. Thể hiện khả năng sinh con, mối quan hệ với con cháu và di sản tinh thần."
    },
    5: {
        "name": "Phúc Đức",
        "meaning": "Cung Phúc Đức liên quan đến phúc lộc, may mắn, đức hạnh và phước báo từ tiền kiếp. Thể hiện vận may trong đời, sự an lành và những phúc phần tích lũy được."
    },
    6: {
        "name": "Điền Trạch",
        "meaning": "Cung Điền Trạch liên quan đến nhà cửa, đất đai, bất động sản và tài sản cố định. Thể hiện mối quan hệ với bất động sản, khả năng sở hữu tài sản và môi trường sống."
    },
    7: {
        "name": "Quan Lộc",
        "meaning": "Cung Quan Lộc liên quan đến sự nghiệp, công danh, chức vụ và danh tiếng xã hội. Thể hiện đường công danh, khả năng thăng tiến và thành công trong sự nghiệp."
    },
    8: {
        "name": "Thiên Di",
        "meaning": "Cung Thiên Di liên quan đến xuất ngoại, du lịch, di cư và mối quan hệ với người nước ngoài. Thể hiện vận đi xa, cơ hội phát triển ở nơi khác và mối liên hệ quốc tế."
    },
    9: {
        "name": "Tài Bạch",
        "meaning": "Cung Tài Bạch liên quan đến tài lộc, tiền bạc, của cải và nguồn thu nhập. Thể hiện khả năng tài chính, cách kiếm tiền và quản lý tài sản trong cuộc đời."
    },
    10: {
        "name": "Tật Ách",
        "meaning": "Cung Tật Ách liên quan đến bệnh tật, tai họa, khó khăn và thử thách trong cuộc đời. Thể hiện những trở ngại cần vượt qua, sức khỏe và những điều cần cẩn trọng."
    },
    11: {
        "name": "Nô Bộc",
        "meaning": "Cung Nô Bộc liên quan đến quần thần, đồng nghiệp, người làm và mối quan hệ trong công việc. Thể hiện mối quan hệ với cấp dưới, đồng nghiệp và khả năng lãnh đạo."
    },
    12: {
        "name": "Phu Thê",
        "meaning": "Cung Phu Thê liên quan đến hôn nhân, vợ chồng, tình yêu và mối quan hệ nam nữ. Thể hiện vận hôn nhân, đối tượng tình duyên và chất lượng mối quan hệ vợ chồng."
    },
}


# 14 Main Star meanings
STAR_MEANINGS = {
    "Tử Vi": {
        "element": "Thổ",
        "meaning": "Tử Vi là sao chúa, đại diện cho quyền uy, địa vị và ảnh hưởng xã hội. Sao này tượng trưng cho người có khả năng lãnh đạo, được kính trọng và có vận mệnh tốt đẹp trong xã hội."
    },
    "Thiên Phủ": {
        "element": "Thổ",
        "meaning": "Thiên Phủ là sao quân sự, đại diện cho quyền lực quân đội và cảnh sát. Sao này tượng trưng cho người có khả năng tổ chức, điều hành và có quyền lực trong các tổ chức."
    },
    "Thái Dương": {
        "element": "Hỏa",
        "meaning": "Thái Dương là sao mặt trời, đại diện cho năng lượng, danh tiếng và sự nghiệp. Sao này tượng trưng cho người năng động, có ambição và được nổi tiếng trong xã hội."
    },
    "Thái Âm": {
        "element": "Thủy",
        "meaning": "Thái Âm là sao mặt trăng, đại diện cho cảm xúc, nội tâm và sức khỏe. Sao này tượng trưng cho người nhạy cảm, có trực giác mạnh và quan tâm đến gia đình."
    },
    "Tham Lang": {
        "element": "Thủy",
        "meaning": "Tham Lang là sao tham lam, đại diện cho ham muốn và đam mê. Sao này tượng trưng cho người có khả năng thuyết phục, giải trí và thu hút người khác."
    },
    "Cự Môn": {
        "element": "Thủy",
        "meaning": "Cự Môn là sao cửa, đại diện cho giao tiếp và nghệ thuật. Sao này tượng trưng cho người có khả năng giao tiếp, nói năng lưu loát và có tài hùng biện."
    },
    "Thiên Tướng": {
        "element": "Thủy",
        "meaning": "Thiên Tướng là sao tướng quân, đại diện cho quân sự và lãnh đạo. Sao này tượng trưng cho người có khả năng chỉ huy, quân sự và tổ chức các hoạt động lớn."
    },
    "Thiên Lương": {
        "element": "Mộc",
        "meaning": "Thiên Lương là sao lương, đại diện cho sự công bằng và lương thiện. Sao này tượng trưng cho người có đạo đức, công bằng và được người khác kính trọng."
    },
    "Thất Sát": {
        "element": "Kim",
        "meaning": "Thất Sát là sao sát, đại diện cho sự hung bạo và quân sự. Sao này tượng trưng cho người có tính cách mạnh mẽ, quyết đoán và có thể trở thành người lãnh đạo."
    },
    "Phá Quân": {
        "element": "Thủy",
        "meaning": "Phá Quân là sao phá, đại diện cho sự phá hoại và thay đổi. Sao này tượng trưng cho người có khả năng phá vỡ kết cấu cũ, tạo ra thay đổi và cải cách."
    },
    "Liêm Trinh": {
        "element": "Hỏa",
        "meaning": "Liêm Trinh là sao liêm, đại diện cho sự liêm chính và trong sáng. Sao này tượng trưng cho người có tính cách trung thực, liêm chính và được tin tưởng."
    },
    "Thiên Đồng": {
        "element": "Thủy",
        "meaning": "Thiên Đồng là sao đồng, đại diện cho sự đồng đều và hài hòa. Sao này tượng trưng cho người có tính cách ôn hòa, hòa đồng và được mọi người yêu mến."
    },
    "Vũ Khúc": {
        "element": "Kim",
        "meaning": "Vũ Khúc là sao vũ, đại diện cho âm nhạc và nghệ thuật. Sao này tượng trưng cho người có tài năng nghệ thuật, âm nhạc và khả năng biểu đạt cảm xúc."
    },
    "Thiên Cơ": {
        "element": "Mộc",
        "meaning": "Thiên Cơ là sao cơ, đại diện cho trí tuệ và kỹ thuật. Sao này tượng trưng cho người thông minh, có khả năng kỹ thuật và tư duy phân tích."
    },
}


# Brightness (Miếu/Đắc/Vượng/Bình/Hãm) interpretations
BRIGHTNESS_MEANINGS = {
    "Miếu": "Sao ở vị trí Miếu là vị trí tốt nhất, sao phát huy toàn bộ năng lượng tích cực, mang lại may mắn, thành công và danh tiếng rực rỡ. Người có sao ở Miếu thường được quý nhân phù trợ.",
    "Vượng": "Sao ở vị trí Vượng là vị trí rất tốt, sao có năng lượng mạnh, mang lại thành công, giàu có và địa vị xã hội. Người có sao ở Vượng thường có cuộc sống sung túc.",
    "Đắc": "Sao ở vị trí Đắc Địa là vị trí tốt, sao phát huy tốt trong môi trường phù hợp, mang lại thành công và ổn định. Người có sao ở Đắc Địa thường có cuộc sống khá giả.",
    "Bình": "Sao ở vị trí Bình Hòa là vị trí trung tính, sao phát huy bình thường không có gì nổi bật. Người có sao ở Bình Hòa cần cố gắng hơn để đạt thành công.",
    "Hãm": "Sao ở vị trí Hãm là vị trí yếu nhất, sao bị suy giảm năng lượng, có thể mang lại khó khăn và thử thách. Người có sao ở Hãm cần cẩn trọng và nỗ lực vượt qua.",
}


PALACE_MEANINGS_BY_NAME = {v["name"]: v for v in PALACE_MEANINGS.values()}


def get_palace_interpretation(palace_index: int) -> Dict:
    """Get interpretation for a palace by sequential index (deprecated — use get_palace_meaning_by_name)."""
    return PALACE_MEANINGS.get(palace_index, {"name": "Unknown", "meaning": "Không có thông tin."})


def get_palace_meaning_by_name(name: str) -> Dict:
    """Get interpretation for a palace by Vietnamese name (correct — position-independent)."""
    return PALACE_MEANINGS_BY_NAME.get(name, {"name": name, "meaning": "Không có thông tin."})


def get_star_interpretation(star_name: str, brightness: str = "Bình") -> Dict:
    """Get interpretation for a star."""
    star_info = STAR_MEANINGS.get(star_name, {
        "element": "Unknown",
        "meaning": "Không có thông tin về sao này."
    })
    brightness_effect = BRIGHTNESS_MEANINGS.get(brightness, BRIGHTNESS_MEANINGS["Bình"])

    return {
        "name": star_name,
        "element": star_info["element"],
        "meaning": star_info["meaning"],
        "brightness": brightness,
        "brightness_effect": brightness_effect
    }


def get_interpretation(palace_index: int, star_name: Optional[str] = None) -> Dict:
    """Get combined interpretation for palace and optional star."""
    result = {
        "palace": get_palace_interpretation(palace_index)
    }

    if star_name:
        result["stars"] = [get_star_interpretation(star_name)]

    return result
