from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def pay_cash_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Подтвердить оплату наличными", callback_data="request_cash_payment")
    keyboard.button(text="Назад", callback_data="back_to_summary")
    keyboard.adjust(1,1)
    return keyboard.as_markup()