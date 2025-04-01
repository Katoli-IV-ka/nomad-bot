def get_summary_message(check_in, check_out, package: dict, contact: dict, username: str | None, total: int) -> str:
    # 🗓️ Даты
    check_in_text = check_in.strftime("%d.%m.%Y") + " 15:00"
    check_out_text = check_out.strftime("%d.%m.%Y") + " 12:00"

    # 🛍️ Услуги
    days = (check_out - check_in).days
    base = "для одного" if package.get("one_person") else "для двоих"
    kupel = " + купель" if package.get("koupel") else ""
    child = "с детьми" if package.get("child") else "без детей"
    pet = "с питомцем" if package.get("pet") else "без питомцев"

    # 👤 Контакт
    name = contact.get("first_name", "Без имени")
    phone = contact.get("phone_number", "")
    user = f"\n@{username}" if username else ""

    return (
        f"📆 *Выбранные даты:*\n"
        f"Заселение: {check_in_text}\n"
        f"Выселение:  {check_out_text}\n\n"

        f"🛍 *Пакет услуг:*\n"
        f"{days} {'день' if days == 1 else 'дня' if days < 5 else 'дней'} {base}{kupel} \n"
        f"{child}\n"
        f"{pet}\n\n"

        f"👤 *Контактные данные:*\n"
        f"{name}\n{phone}{user}\n\n"

        f"💳 *Сумма к оплате:* {total}р."
    )