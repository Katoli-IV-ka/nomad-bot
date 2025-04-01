from datetime import timedelta


def calculate_booking_price(check_in, check_out, package: dict) -> int:
    total = 0
    full_days = (check_out - check_in).days
    for i in range(full_days):
        day = check_in + timedelta(days=i)
        if day.weekday() in (0, 1, 2, 3):
            total += 200
        else:
            total += 250
    if package.get("koupel"):
        total += 100
    return total