from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_payment_keyboard(notion_page_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Подтвердить оплату", callback_data=f"confirm_payment_{notion_page_id}")

    return keyboard.as_markup()

