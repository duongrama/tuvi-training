"""
Tu Vi (Vietnamese Astrology) Service - Lunar calendar conversion.

Provides lunar date conversion for birth chart calculations using lunarcalendar.
"""

from datetime import datetime
from typing import Optional
import pytz


# Vietnam timezone
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

# Can Chi for years (60-year cycle)
YEAR_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
YEAR_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Can Chi for months
MONTH_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
MONTH_CHI = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]

# Can Chi for days
DAY_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
DAY_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Can Chi for hours (12 double-hours)
HOUR_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]


def birth_to_lunar(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    is_leap_month: bool = False
) -> dict:
    """
    Convert solar birth date to lunar date.

    Args:
        year: Solar year (e.g., 1990)
        month: Solar month (1-12)
        day: Solar day (1-31)
        hour: Birth hour (0-23)
        minute: Birth minute (0-59)
        is_leap_month: Whether birth month is a leap month (default False)

    Returns:
        dict: Lunar date with can/chi for year, month, day, hour
    """
    from lunarcalendar import Solar, Lunar, Converter

    # Create solar date
    solar = Solar(year, month, day)

    # Convert to lunar
    lunar = Converter.Solar2Lunar(solar)

    # Calculate year can-chi (60-year cycle)
    # Base year: 1984 = Giáp Tý (year 1 of cycle)
    cycle_year = year - 1984
    year_can_index = cycle_year % 10
    year_chi_index = cycle_year % 12

    # Calculate month can-chi
    # Month can depends on year can and month
    month_can_index = (year_can_index * 2 + lunar.month - 1) % 10

    # Calculate day can-chi (using Julian day)
    # Simplified: use day of cycle
    from datetime import date
    julian_day = date(year, month, day).toordinal() + 1721425
    day_can_index = julian_day % 10
    day_chi_index = julian_day % 12

    # Calculate hour can-chi (using day can + hour chi)
    hour_chi_index = ((hour + 1) // 2) % 12  # Double-hour system

    return {
        "solar": {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute
        },
        "lunar": {
            "year": lunar.year,
            "month": lunar.month,
            "day": lunar.day,
            "is_leap": lunar.isleap if hasattr(lunar, 'isleap') else is_leap_month
        },
        "can_chi": {
            "year": f"{YEAR_CAN[year_can_index]} {YEAR_CHI[year_chi_index]}",
            "month": f"{MONTH_CAN[month_can_index]} {MONTH_CHI[lunar.month - 1]}",
            "day": f"{DAY_CAN[day_can_index]} {DAY_CHI[day_chi_index]}",
            "hour": f"{DAY_CAN[day_can_index]} {HOUR_CHI[hour_chi_index]}"
        }
    }


def get_tuvi_chart(birth_data: dict) -> dict:
    """
    Generate basic Tu Vi birth chart data.

    Args:
        birth_data: Output from birth_to_lunar()

    Returns:
        dict: Basic Tử Vi chart information
    """
    lunar = birth_data["lunar"]
    can_chi = birth_data["can_chi"]

    # Basic chart info
    chart = {
        "name": "Tử Vi Đại Quảng",
        "birth_info": {
            "solar": birth_data["solar"],
            "lunar": lunar
        },
        "can_chi": can_chi,
        "cung": {
            "mệnh": "Tý",
            "thân": "Tý"
        },
        "note": "Basic chart - full 12 cung system requires detailed calculation"
    }

    return chart


def get_nap_giap_for_hour(birth_data: dict) -> str:
    """Get Nap Giap (hour stem) based on day can and hour."""
    day_can = birth_data["can_chi"]["day"].split()[0]
    hour = birth_data["solar"]["hour"]

    # Hour chi
    hour_chi = HOUR_CHI[(hour + 1) // 2 % 12]

    # Hour can calculation based on day can
    day_can_idx = YEAR_CAN.index(day_can) if day_can in YEAR_CAN else 0

    # Each 2-hour period shifts the can
    hour_can_idx = (day_can_idx + (hour + 1) // 2) % 10

    return f"{YEAR_CAN[hour_can_idx]} {hour_chi}"
