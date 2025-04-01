import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import calendar
from datetime import date

# 🔒 Список забронированных дат (Заменить на реальные данные из БД)
BOOKED_DATES = {
    datetime.date(2025, 5, 3): "pm",    # вечер занят → утром можно выехать (☀️)
    datetime.date(2025, 5, 4): "am",    # утро занят → вечером можно заехать (🌑)
    datetime.date(2025, 5, 5): "full"   # весь день занят (⛺️)
}

def generate_calendar(year: int, month: int, check_in=None, check_out=None) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    month_name = date(year, month, 1).strftime("%B %Y")

    # Переключатели месяца
    prev_month = (month - 1) or 12
    prev_year = year - 1 if month == 1 else year
    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    builder.row(
        InlineKeyboardButton(text="⬅️", callback_data=f"switch|{prev_year}|{prev_month}"),
        InlineKeyboardButton(text=month_name, callback_data="noop"),
        InlineKeyboardButton(text="➡️", callback_data=f"switch|{next_year}|{next_month}")
    )

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text=" ", callback_data="noop"))
                continue

            current_date = date(year, month, day)
            selected = (
                check_in and check_out and check_in <= current_date <= check_out
            ) or (check_in == current_date)

            if selected:
                text = "📍"
                cb = f"select|{year}|{month}|{day}"

            elif current_date in BOOKED_DATES:
                status = BOOKED_DATES[current_date]
                if status == "full":
                    text = "🌴"
                    cb = "noop"
                elif status == "am":
                    text = "🦉"
                    cb = f"select|{year}|{month}|{day}"
                elif status == "pm":
                    text = "🌻"
                    cb = f"select|{year}|{month}|{day}"
            else:
                text = str(day)
                cb = f"select|{year}|{month}|{day}"

            row.append(InlineKeyboardButton(text=text, callback_data=cb))
        builder.row(*row)

    builder.row(
        InlineKeyboardButton(text="Подтвердить даты", callback_data="confirm")
    )

    return builder.as_markup()
