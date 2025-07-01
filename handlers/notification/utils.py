import datetime
from datetime import date, timedelta

from database.notion_connect import get_clean_rows, get_bookings_ending_on, get_bookings_start_on, \
    get_bookings_starting_within


def get_prepayment_only() -> list[dict]:
    return get_bookings_starting_within(
        days=7,
        status=["Prepayment received"]
    )

def get_tomorrow_bookings() -> list[dict]:
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    status = ['Waiting visit']
    return get_bookings_start_on(start_on=tomorrow, status=status)

def get_ending_bookings() -> list[dict]:
    tomorrow = (date.today() - timedelta(days=1)).isoformat()
    status = ['Up-to-date booking']
    return get_bookings_ending_on(end_on=tomorrow, status=status)

async def get_next_booking_start_date() -> datetime.date | None:
    bookings = get_clean_rows()
    tomorrow = (date.today() + timedelta(days=1))

    # Извлекаем все start_date >= сегодня
    future_starts = [
        datetime.datetime.strptime(b['start_date'], '%Y-%m-%d').date()
        for b in bookings
        if datetime.datetime.strptime(b['start_date'], '%Y-%m-%d').date() >= tomorrow
    ]

    return min(future_starts) if future_starts else None