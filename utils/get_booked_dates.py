from database.notion_connect import get_clean_rows


import datetime

async def get_booking_dates():
    allowed_status = [
        'Waiting visit',
        'Up-to-date booking',
        'Completed booking',
        'On verification',
        'Waiting payment'
    ]

    bookings = get_clean_rows(status=allowed_status)

    # Получаем текущую дату, месяц и год
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year

    result = []

    for booking in bookings:
        # Парсим строки в date
        start_date = datetime.datetime.strptime(booking['start_date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(booking['end_date'], '%Y-%m-%d').date()

        # Пропускаем, если начало не в текущем месяце или годе
        if (start_date.year < current_year) or \
           (start_date.year == current_year and start_date.month < current_month):
            continue

        # Итерируем от начала до (сдвинутого) конца включительно
        current_day = start_date
        while current_day <= end_date:
            result.append(current_day)
            current_day += datetime.timedelta(days=1)

    return result



