from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def summary_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="💳 Оплата картой", callback_data="pay_by_card")
    builder.button(text="💵 Наличный расчёт", callback_data="pay_cash")
    builder.adjust(1)

    builder.button(text="⬅️ Назад", callback_data="back_to_options")
    builder.button(text="🔘 Отмена", callback_data="cancel_booking")
    builder.adjust(2)

    return builder.as_markup()