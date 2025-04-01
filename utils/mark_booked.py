from datetime import date

from keyboards.booking_kb import BOOKED_DATES


def mark_booked(date_obj: date, part: str):
    """
    Устанавливает статус даты в BOOKED_DATES.
    - Если дата уже помечена как противоположная половина — делаем full.
    - Если пусто — ставим part (am / pm).
    """
    current = BOOKED_DATES.get(date_obj)
    if current is None:
        BOOKED_DATES[date_obj] = part
    elif (current == "am" and part == "pm") or (current == "pm" and part == "am"):
        BOOKED_DATES[date_obj] = "full"