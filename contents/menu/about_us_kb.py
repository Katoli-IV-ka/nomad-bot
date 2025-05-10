from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Функция для создания Inline клавиатуры
async def about_us_kb(photo_index=0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="←", callback_data=f"photo_left_{photo_index}")
    keyboard.button(text="Назад", callback_data="delete_message")
    keyboard.button(text="→", callback_data=f"photo_right_{photo_index}")

    keyboard.adjust(3)
    return keyboard.as_markup()
