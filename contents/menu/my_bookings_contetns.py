from datetime import datetime, timedelta
from typing import List, Dict

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

my_bookings_empty_text = 'Список ваших бронирований пуст, хотите забронировать дату?'

my_bookings_photo = "AgACAgIAAxkBAAINIWgrgfyz0qQaVjVA2ZHUMN8xuJ7aAAKi6jEbiftgSZpI9sLiC2SXAQADAgADcwADNgQ"

def format_bookings_overview(bookings: List[Dict]) -> str:
    """
    Формирует сообщение с кратким обзором первых четырёх бронирований.

    :param bookings: Список словарей с данными бронирования,
                     каждый словарь должен содержать ключи 'start_date', 'end_date', 'cost'.
                     Поля 'start_date' и 'end_date' могут быть либо datetime.date/str в формате 'YYYY-MM-DD'.
    :return: Строка с сообщением
    """
    # Заголовок
    msg_lines = ["<b>Ваши бронирования:</b>", ""]

    # Проходим по первым четырём записям (или меньше, если их меньше)
    for b in bookings[:4]:
        # Приводим даты к строке в формате DD.MM.YYYY
        sd = b["start_date"]
        ed = b["end_date"] + timedelta(days=1)
        if isinstance(sd, str):
            sd = datetime.strptime(sd, "%Y-%m-%d").date()
        if isinstance(ed, str):
            ed = datetime.strptime(ed, "%Y-%m-%d").date()
        sd_str = sd.strftime("%d.%m.%Y")
        ed_str = ed.strftime("%d.%м.%Y".replace("м", "m"))  # исправляем опечатку в шаблоне

        # Добавляем блок по одному бронированию
        msg_lines.append(f"Дата заезда: {sd_str}")
        msg_lines.append(f"Дата выезда: {ed_str }")
        msg_lines.append(f"Стоимость: {b['cost']} р.")
        msg_lines.append("")  # пустая строка между записями

    # Финальная строка
    msg_lines.append(
        "За дополнительной информацией можно обращаться в наш инстаграм аккаунт: @nomad_cabin"
    )

    return "\n".join(msg_lines)

def get_to_booking_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Бронировать", callback_data="booking")
    return keyboard.as_markup()