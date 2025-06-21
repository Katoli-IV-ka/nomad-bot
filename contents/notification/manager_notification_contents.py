from utils.format_date import format_date_ru

client_notification_photo = "AgACAgIAAxkBAAIBwWfrCtuqOQr0YVZFQF3gIa3Fs9IBAAKq9TEb4TZZS2amRIVvjqXmAQADAgADbQADNgQ"


def manager_notification_text(booking_data):
    name = booking_data['contact'].split("_")[0]
    start_date = format_date_ru(booking_data['start_date'])
    end_date = format_date_ru(booking_data['end_date'])
    phone_number = booking_data['phone']
    cost = booking_data['cost']

    return str(
        f"<b>⚠️ Напоминание\n</b>"
        f"Необходимо запросить полную оплату у клиента или отменить бронь.\n"
        f"\n"
        f"Контакт: {name}\n"
        f"{phone_number}\n"
        f"\n"
        f"Даты бронирования: {start_date} - {end_date}\n"
        f"Общий чек: {cost}\n"
    )