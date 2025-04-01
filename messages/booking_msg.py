from keyboards.booking_kb import generate_calendar

booking_calendar_message = {
    "text": "booking calendar msg",
    "reply_markup": generate_calendar(),
}