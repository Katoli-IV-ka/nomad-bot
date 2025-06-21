from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_payment_keyboard(notion_page_id, only_payment=False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    if not only_payment:
        keyboard.button(text="🪙 Предоплата", callback_data=f"confirm_prepayment_{notion_page_id}")
    keyboard.button(text="💶 Полная оплата", callback_data=f"confirm_payment_{notion_page_id}")
    keyboard.button(text="🚫 Отмена", callback_data=f"cancel_payment_{notion_page_id}")

    keyboard.adjust(2,1,1)
    return keyboard.as_markup()

