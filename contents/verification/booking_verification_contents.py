from datetime import timedelta

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

booking_confirmation_photo = "AgACAgIAAxkBAAINSmgrki7oFHM9g47mUpDZPwPK1o3BAALp8DEbgJJYSc0rmjVuWlPyAQADAgADcwADNgQ"

def booking_confirmation_text(check_in, check_out, package: dict,
                         contact_name: str, phone_number: str, username: str | None,
                         total: int) -> str:
    # 🗓️ Даты
    check_in_text = check_in.strftime("%d.%m.%Y")
    if check_in == check_out:
        check_out = check_out + timedelta(days=1)
    check_out_text = check_out.strftime("%d.%m.%Y")

    # 🛍️ Услуги
    days = (check_out - check_in).days
    base = "для одного" if package.get("one_person") else "для двоих"
    kupel = " + купель" if package.get("koupel") else ""
    child = "с детьми" if package.get("child") else "без детей"
    pet = "с питомцем" if package.get("pet") else "без питомцев"

    # 👤 Контакт
    user = f"\n@{username}" if username else ""

    return (
        f"<b>Даты:</b> {check_in_text} - {check_out_text}\n\n"

        f"<b>Пакет услуг:</b>\n"
        f"{days} {'день' if days == 1 else 'дня' if days < 5 else 'дней'} {base}{kupel} \n"
        f"{child}\n"
        f"{pet}\n\n"

        f"<b>Контакт:</b> {contact_name}\n"
        f"{phone_number}\n\n"

        f"<b>К оплате:</b> {total}р."
    )


def booking_confirmation_keyboard(notion_page_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Подтвердить", callback_data=f"wait_payment_{notion_page_id}")
    keyboard.button(text="Отказать", callback_data=f"reject_booking_{notion_page_id}")

    return keyboard.as_markup(one_time_keyboard=True)

