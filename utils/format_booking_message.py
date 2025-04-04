def format_booking_message(booking):
    """
    Формирует сообщение о бронировании из данных.

    :param booking: Словарь с данными бронирования
    :return: Строка с сообщением
    """
    # Даты
    start_date = booking["start_date"].strftime("%d.%m.%Y")
    end_date = booking["end_date"].strftime("%d.%m.%Y")

    # Пакет услуг
    service_package = []
    if booking["kids"]:
        service_package.append("с одним ребёнком")
    if booking["pets"]:
        service_package.append("с питомцем")
    if booking["kupel"]:
        service_package.append("купель")
    if "1" in booking["payment_method"].lower():
        service_package.append("на двоих")

    # Стоимость и способ оплаты
    cost = booking["cost"]

    if booking["payment_method"] == "Cash":
        payment_method = "Наличный расчёт"
    elif booking["payment_method"] == "Card":
        payment_method = "Оплата по карте"
    else:
        payment_method = "Не известный статус"

    # Формируем сообщение
    message = f"🏕 Ваша бронь с {start_date} по {end_date}\n\n"
    message += f"🛍 Пакет услуг:\n- " + "\n- ".join(service_package) + "\n\n"
    message += f"Дата бронирования:\n\n"
    message += f"💵 Данные для оплаты:\n{cost} р.\n{payment_method}"

    return message
