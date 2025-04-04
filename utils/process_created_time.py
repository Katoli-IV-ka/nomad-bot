import datetime


def process_created_time(created_time: str) -> str:
    """
    Преобразует время из формата 2025-04-04T21:32:00.000 в Минское время
    с точностью до минут, без использования pytz.

    :param created_time: Время в формате "2025-04-04T21:32:00.000"
    :return: Время с точностью до минут в формате "YYYY-MM-DD HH:MM"
    """
    # Удаляем символ 'Z' в конце строки и преобразуем её в объект datetime
    created_time = created_time.rstrip('Z')
    created_time_obj = datetime.datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S.%f")

    # Переводим в Минское время (UTC+3)
    minsk_time = created_time_obj + datetime.timedelta(hours=3)

    # Форматируем в строку с точностью до минут
    formatted_time = minsk_time.strftime("%Y-%m-%d %H:%M")

    return formatted_time
