from keyboards.menu_kb import reply_menu_keyboard, menu_keyboard

start_message = {
    "photo": "AgACAgIAAxkBAAIBy2frCwgummI8aLSuDkAhkFsxp94hAAKv9TEb4TZZS2ezt3UE4RvuAQADAgADcwADNgQ",
    "caption": f"<b>Nomad cabin</b>\n"
               f"\n"
               f"Аренда дома для отдыха\n"
               f" - дом в аренду, 30 км от Бреста\n"
               f" - позвольте природе восстановить ваши силы \n"
               f"\n"
               f"Здесь вы можете забронировать дату...\n",
    "reply_markup": menu_keyboard(),
    "parse_mode": "HTML",
}


