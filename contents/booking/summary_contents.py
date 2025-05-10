from datetime import timedelta

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


summary_photo = "AgACAgIAAxkBAAIByWfrCv-oNYvy842u29I6r1GG6etVAAKu9TEb4TZZS7UhzXPay0zqAQADAgADcwADNgQ"

accept_summary_photo = "AgACAgIAAxkBAAIBw2frCujhFPLA8Xe2f_hL-ntRO2nJAAKr9TEb4TZZSy0fEuO6tM0qAQADAgADcwADNgQ"


accept_summary_text = str(
    f"<b>Заявка принята</b>\n"
    f"\n"
    f"▪️В ближайшее время с вами свяжется наш администратор — подтвердит "
    f"бронь и вышлет информацию по оплате.\n"
    f"\n"
    f"▪️Оплата в онлайн формате проводится в течение 1-2 дней "
    f"(в случае неоплаты, бронь не фиксируется).\n"
)


def get_summary_text(check_in, check_out, package: dict,
                     contact_name: str, phone_number: str, username: str | None,
                     total: int) -> str:
    # 🗓️ Даты
    check_in_text = check_in.strftime("%d.%m.%Y") + " 15:00"
    if check_in == check_out:
        check_out = check_out + timedelta(days=1)
    check_out_text = check_out.strftime("%d.%m.%Y") + " 11:00"

    # 🛍️ Услуги
    days = (check_out - check_in).days
    base = "для одного" if package.get("one_person") else "для двоих"
    kupel = " + купель" if package.get("koupel") else ""
    child = "с детьми" if package.get("child") else "без детей"
    pet = "с питомцем" if package.get("pet") else "без питомцев"

    # 👤 Контакт
    user = f"\n@{username}" if username else ""

    return (
        f"📆 *Выбранные даты:*\n"
        f"Заселение: {check_in_text}\n"
        f"Выселение:  {check_out_text}\n\n"

        f"🛍 *Пакет услуг:*\n"
        f"{days} {'день' if days == 1 else 'дня' if days < 5 else 'дней'} {base}{kupel} \n"
        f"{child}\n"
        f"{pet}\n\n"

        f"👤 *Контактные данные:*\n"
        f"{contact_name}\n{phone_number}{user}\n\n"

        f"💳 *Сумма к оплате:* {total}р."
    )


def get_summary_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="☀️ Подтвердить бронирование", callback_data="accept_summary")
    builder.button(text="🔙 Назад", callback_data="to_options")
    builder.button(text="🚫 Отмена", callback_data="cancel_booking")
    builder.adjust(1,2)

    return builder.as_markup()



