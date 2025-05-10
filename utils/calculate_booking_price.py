from datetime import timedelta
from config import PRICES

def calculate_booking_price(check_in, check_out, package: dict) -> int:
    """
    Считает стоимость бронирования:
      – Пн–Чт: PRICES['weekday_price']
      – Пт–Вс: PRICES['weekend_price']
      – + PRICES['koupel_price'] (если package['koupel'])
      – + PRICES['child_fee'] (если package['child'])
      – + PRICES['pet_fee'] (если package['pet'])
      – Скидка PRICES['discount_rate'] при брони >= PRICES['discount_threshold_days'] суток
    """
    # определяем полные дни
    if check_in == check_out:
        days = 1
    else:
        days = (check_out - check_in).days

    total = 0
    for i in range(days):
        day = check_in + timedelta(days=i)
        if day.weekday() < 4:  # 0..3 = Пн–Чт
            total += PRICES["weekday_price"]
        else:                  # 4..6 = Пт–Вс
            total += PRICES["weekend_price"]

    # дополнительные сборы
    if package.get("koupel"):
        total += PRICES["koupel_price"]
    if package.get("child"):
        total += PRICES["child_fee"]
    if package.get("pet"):
        total += PRICES["pet_fee"]

    # применяем скидку, если дней достаточно
    if days >= PRICES["discount_threshold_days"]:
        total = round(total * (1 - PRICES["discount_rate"]))

    return total
