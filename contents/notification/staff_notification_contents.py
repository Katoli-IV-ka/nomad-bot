async def staff_notification_text(booking_data=None, before_booking:bool=False):
    if before_booking:
        return str(
            f"🔔 Напоминание.\n"
            f"Сегодня в 11:00 выезжают гости, необходимо проверить дом.\n"
        )
    parts = [f"{' - для одного' if booking_data['num_quests'] == '1' else ' - для двоих'}"]
    if booking_data.get("kids"):
        parts.append(" - с ребёнком")
    if booking_data.get("pets"):
        parts.append(" - с питомцем")
    if booking_data.get("koupel"):
        parts.append(" - купель")

    return (
        f"🔔 Напоминание о ближайшем бронировании.\n\n"
        f"Завтра заезд:\n"
        f"📆 C {booking_data['start_date']} по {booking_data['end_date']}\n\n"
        f"✨ Пакет услуг:\n"
        f"{chr(10).join(parts)}\n"
        f"\n"
        "Пожалуйста, убедитесь, что всё готово к заезду."
    )


