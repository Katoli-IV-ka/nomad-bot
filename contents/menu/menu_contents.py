from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_photo = "AgACAgIAAxkBAAINKWgrgpLYcRxPZzIsqisPYD02kj-eAAKn6jEbiftgSRV0nm_tWZKOAQADAgADcwADNgQ"

menu_text = str(
    f"<b>Nomad cabin</b>\n"
    f"\n"
    f"Аренда дома для отдыха\n"
    f" - дом в аренду, 30 км от Бреста\n"
    f" - позвольте природе восстановить ваши силы \n"
    f"\n"
    f"Здесь вы можете забронировать дату...\n",
)

def menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Бронирование", callback_data="booking")
    keyboard.button(text="О доме", callback_data="about_us")
    keyboard.button(text="Моя бронь", callback_data="my_booking")
    keyboard.button(text="Наши контакты", callback_data="our_contacts")

    keyboard.adjust(2,2)

    return keyboard.as_markup()


