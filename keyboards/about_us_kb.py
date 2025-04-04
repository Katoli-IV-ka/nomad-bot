from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

moon_phases = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔"]


# Функция для создания Inline клавиатуры
async def about_us_kb(photo_index=0, moon_phase_index=0) -> InlineKeyboardMarkup:
    # Кнопки для навигации по фотографиям
    keyboard = InlineKeyboardBuilder()

    # Левая и правая стрелки для переключения фотографий
    keyboard.button(text="←", callback_data=f"photo_left_{photo_index}")
    # Кнопка для переключения эмодзи луны
    keyboard.button(text=moon_phases[moon_phase_index], callback_data=f"moon_{moon_phase_index}")
    keyboard.button(text="→", callback_data=f"photo_right_{photo_index}")

    keyboard.button(text="В меню", callback_data="delete_message")

    # Добавляем кнопки в клавиатуру
    keyboard.adjust(3, 1)

    return keyboard.as_markup()
