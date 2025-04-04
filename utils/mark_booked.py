from datetime import date



def mark_booked(date_obj: date, part: str, booked_dates):
    """
    Устанавливает статус даты в BOOKED_DATES.
    - Если дата уже помечена как противоположная половина — делаем full.
    - Если пусто — ставим part (am / pm).
    """
    current = booked_dates.get(date_obj)
    if current is None:
        booked_dates[date_obj] = part
    elif (current == "am" and part == "pm") or (current == "pm" and part == "am"):
        booked_dates[date_obj] = "full"