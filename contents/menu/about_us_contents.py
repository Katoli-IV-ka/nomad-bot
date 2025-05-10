from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


about_us_photos = [
        "AgACAgIAAxkBAAIE0WfuYMW5pJ20R350bRorXUKqwhB-AALH7TEbx1xwS-V8HcyauMHIAQADAgADcwADNgQ",
        "AgACAgIAAxkBAAIE1GfuYOiJ2hx1hw3PlMc0cg1A96YKAALJ7TEbx1xwS1OP0ttivFybAQADAgADcwADNgQ",
        "AgACAgIAAxkBAAIE1mfuYS5K1p7VrlRY_War9YHOhAEkAALK7TEbx1xwSxpbNWjKt4PiAQADAgADcwADNgQ",
        "AgACAgIAAxkBAAIE2GfuYVayvWocZMewtFRLi_evJcOpAALM7TEbx1xwS6y2GI71c-iVAQADAgADcwADNgQ"
]

async def about_us_kb(photo_index=0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="←", callback_data=f"photo_left_{photo_index}")
    keyboard.button(text="Назад", callback_data="delete_message")
    keyboard.button(text="→", callback_data=f"photo_right_{photo_index}")

    keyboard.adjust(3)
    return keyboard.as_markup()
