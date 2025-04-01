from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def share_contact_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Поделиться контактом", request_contact=True)
    keyboard.adjust(1,1)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)