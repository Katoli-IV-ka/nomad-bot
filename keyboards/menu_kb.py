from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def reply_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Бронирование")
    keyboard.button(text="Информация о доме")
    keyboard.button(text="Мои бронирования")
    keyboard.button(text="Наши контакты")

    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)

def menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Бронирование", callback_data="booking")
    keyboard.button(text="Информация о доме", callback_data="about_us")
    keyboard.button(text="Мои бронирования", callback_data="my_booking")
    keyboard.button(text="Наши контакты", callback_data="our_contacts")

    keyboard.adjust(2)

    return keyboard.as_markup()