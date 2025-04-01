from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Бронирование")
    keyboard.button(text="Информация о доме")
    keyboard.button(text="Мои бронирования")
    keyboard.button(text="Связаться с менеджером")

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)