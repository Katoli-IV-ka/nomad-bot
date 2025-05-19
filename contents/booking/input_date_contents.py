import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
from datetime import date

input_date_photo = "AgACAgIAAxkBAAINJ2grgnqe3UTaYZaurvGeXavEQLEbAAKl6jEbiftgSQ38ymU6m4XvAQADAgADcwADNgQ"

input_date_text = str(
    f"вы можете выбрать любую свободную дату в календаре\n"
    f"🔐 — даты с замочком уже забронированы другими гостями\n"
    f"\n"
    f"cтоимость проживания:\n"
    f"с понедельника по четверг — 240 byn\n"
    f"с пятницы по воскресенье — 290 byn\n"
    f"от двух дней бронирования — скидка 20% на весь чек\n"
    f"\n"
    f"правила заселения:\n"
    f"заезд — с 15:00\n"
    f"выезд — до 11:00 следующего дня\n"
)

def input_date_keyboard(booked_dates: set[date],
                        check_in: date = None,
                        check_out: date = None,
                        year: int = datetime.date.today().year,
                        month: int = datetime.date.today().month) -> InlineKeyboardMarkup:
    """
    Построение календаря:
     - 🔒 если день в booked_dates
     - 📍 если попал в [check_in..check_out]
     - иначе — число
    """
    builder = InlineKeyboardBuilder()
    mn = date(year, month, 1).strftime("%B %Y")
    prev_m = month - 1 or 12
    prev_y = year - (1 if month == 1 else 0)
    next_m = month + 1 if month < 12 else 1
    next_y = year + (1 if month == 12 else 0)

    # переключатели
    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=f"switch|{prev_y}|{prev_m}"),
        InlineKeyboardButton(text=mn, callback_data="noop"),
        InlineKeyboardButton(text="➡️", callback_data=f"switch|{next_y}|{next_m}")
    )

    cal = calendar.Calendar(firstweekday=0)
    for week in cal.monthdayscalendar(year, month):
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="noop"))
                continue

            d_ = date(year, month, day)
            if d_ in booked_dates:
                text, cb = "🔒", "noop"
            else:
                # если в выбранном диапазоне
                if check_in and check_out and check_in <= d_ <= check_out:
                    text = "📍"
                elif check_in and check_in == d_ and check_out is None:
                    text = "📍"
                else:
                    text = str(day)
                cb = f"select|{year}|{month}|{day}"

            row.append(InlineKeyboardButton(text=text, callback_data=cb))
        builder.row(*row)

    # кнопки снизу
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="delete_message"),
        InlineKeyboardButton(text="Подтвердить", callback_data="confirm_date")
    )

    return builder.as_markup()


def input_date_alerts(check_in=None, check_out=None):
    if check_in and check_out:
        return  {
          "text": f"Даты бронирования с {check_in} по {check_out}",
        }
    elif not check_in and not check_out:
        return {
            "text": f"Сначала выберите даты",
        }
    else:
        return  {
          "text": f"Дата бронирования: {check_in}",
        }