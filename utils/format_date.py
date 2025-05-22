import datetime


def format_date_ru(date_str: str) -> str:
    """
    Преобразует строку вида "YYYY-MM-DD" в формат "D месяц́а" на русском.
    """
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    months_genitive = {
        1: "января",
        2: "февраля",
        3: "марта",
        4: "апреля",
        5: "мая",
        6: "июня",
        7: "июля",
        8: "августа",
        9: "сентября",
        10: "октября",
        11: "ноября",
        12: "декабря",
    }
    return f"{dt.day} {months_genitive[dt.month]}"