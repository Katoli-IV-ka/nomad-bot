from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

request_contact_text = str(
    'Пожалуйста, поделитесь вашим контактом.\n'
    'Для этого нажмите внизу экрана кнопку "Поделиться контактом" 👇🏻'
)

share_contact_photo = 'AgACAgIAAxkBAAINI2grgiJaxKsaTrNzLj7Yab0FtoWPAAKj6jEbiftgSTa2pHZJM6bWAQADAgADcwADNgQ'

def share_contact_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Отправить свой контакт", request_contact=True)
    return keyboard.as_markup(
        one_time_keyboard=True,
        resize_keyboard=False,
        is_persistent=True,
    )