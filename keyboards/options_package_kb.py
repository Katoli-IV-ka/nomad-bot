from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def options_package_keyboard(data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    def mark(option_key: str, label: str, exclusive=False):
        active = data.get(option_key)
        icon = "☑️" if active else ""
        return icon + " " + label, f"package_options|{option_key}|{int(exclusive)}"

    # Ряд: для одного / для двоих (взаимоисключающие)
    for label, callback_data in [
        mark("one_person", "Для одного", exclusive=True),
        mark("two_person", "Для двоих", exclusive=True)
    ]:
        builder.button(text=label, callback_data=callback_data)

    # Ряд: ребёнок / питомец
    for label, callback_data in [
        mark("child", "Буду с 1 ребёнком"),
        mark("pet", "Буду с питомцем")
    ]:
        builder.button(text=label, callback_data=callback_data)

    # Отдельные опции
    for label, callback_data in [
        mark("koupel", "Добавить купель"),
        mark("film", "Бронирование для съемок")
    ]:
        builder.button(text=label, callback_data=callback_data)

    # Кнопка продолжения
    builder.button(text="Продолжить", callback_data="continue_booking")
    builder.adjust(2, 2, 1, 1, 1)

    return builder.as_markup()

