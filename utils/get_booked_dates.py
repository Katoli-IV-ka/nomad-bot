import datetime

from database.notion_connect import get_clean_rows


async def get_booking_dates():
    bookings = get_clean_rows()

    # Получаем текущую дату и месяц
    current_date = datetime.date.today()
    current_month = current_date.month
    current_year = current_date.year

    # Результирующий словарь
    result = {}

    # Обрабатываем каждую запись
    for booking in bookings:

        # Преобразуем строки в даты
        start_date = datetime.datetime.strptime(booking['start_date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(booking['end_date'], '%Y-%m-%d').date()
        # Если дата начала не из текущего месяца или прошедшая, пропускаем её
        if start_date.month < current_month or (start_date.month == current_month and start_date.year < current_year):
            continue

        # Перебираем все даты в диапазоне и применяем нужную логику
        current_day = start_date
        while current_day <= end_date:
            # Если это первая дата диапазона
            if current_day == start_date:
                result[current_day] = "pm"
            # Если это последняя дата диапазона
            elif current_day == end_date:
                result[current_day] = "am"
            # Для всех других дат
            else:
                result[current_day] = "full"

            # Переходим к следующему дню
            current_day += datetime.timedelta(days=1)

    return result



