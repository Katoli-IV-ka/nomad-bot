from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

options_photo = "AgACAgIAAxkBAAIOL2guXZn6_d_npOwoYdhhFooAAZvzEQAD6TEbQ255SYCaRv7znI_OAQADAgADcwADNgQ"

def get_options_text(package: dict) -> str:
    text = "Вы выбрали:\n"

    mapping = {
        "one_person": "👤 Для одного",
        "two_person": "👥 Для двоих",
        "child": "🧒 С ребёнком",
        "pet": "🐶 С питомцем",
        "koupel": "🛁 Купель",
    }

    for key, label in mapping.items():
        if package.get(key):
            text += f"• {label}\n"

    return text or ""

def get_options_keyboard(data: dict = {}) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    def mark(callback_key: str, btn_text: str, exclusive=False):
        active = data.get(callback_key)
        icon = "☑️" if active else ""
        text = icon + " " + btn_text

        callback = f"package_options|{callback_key}|{int(exclusive)}"
        return {"text": text, "callback_data": callback}

    # Ряд: для одного / для двоих (взаимоисключающие)
    keyboard.button(**mark("one_person", "Для одного", exclusive=True))
    keyboard.button(**mark("two_person", "Для двоих", exclusive=True))

    # Ряд: ребёнок / питомец
    keyboard.button(**mark("child", "Буду с 1 ребёнком"))
    keyboard.button(**mark("pet", "Буду с питомцем"))

    # Отдельные опции
    keyboard.button(**mark("koupel", "Добавить купель"))

    # Кнопка продолжения
    keyboard.button(text="Назад", callback_data="back_to_booking")
    keyboard.button(text="Продолжить", callback_data="accept_options")

    keyboard.adjust(2, 2, 1, 2)
    return keyboard.as_markup()


async def to_options_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Назад", callback_data="to_options")
    return keyboard.as_markup()
