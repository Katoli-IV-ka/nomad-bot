from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


about_us_contents = [
    {'media': "AgACAgIAAxkBAAINK2grgqJsq2sAAUu6cnG97UiXNSJiUQACD_gxG_uJYUlZlMriOwABwA0BAAMCAANzAAM2BA",
     'text': None,
    },

    {'media': "AgACAgIAAxkBAAINLWgrgrI1f0-MZLiBtpTPiaWjehvEAAKp6jEbiftgSVy3cBAw7CCPAQADAgADcwADNgQ",
     'text': None,
    },

    {'media': "AgACAgIAAxkBAAIOQmguZ6zqVFCNjCLHqbfyGcnTHtbHAAIM6TEbQ255SRAzjW4gc1CUAQADAgADcwADNgQ",
     'text': str(f'<b>если находитесь в поиске подарка, у нас есть подарочные карты '
                 f'на отдых и проживание в нашем гостевом доме.</b>\n'
                 f'\n'
                 f' ▪️можно выбрать конкретную дату, или выбрать подарочную карту с открытым числом '
                 f'(можно будет в течение 6 месяцев выбрать подходящий день для заселения)\n'
                 f'\n'
                 f' ▪️к сертификату можно добавить купель или оформить подарок без нее.\n'
                 f'\n'
                 f' ▪️при оформлении с вами свяжется наш менеджер и направит электронную подарочную карту '
                 f'в мессенджер или на электронную почту.'),
    },

    {'media': "AgACAgIAAxkBAAIOJ2guXNkuIRAaPrpV-3iCdQ3GvJQ_AAL96DEbQ255SY57QU8kMd0SAQADAgADcwADNgQ",
     'text': None,
    },

    {'media': "AgACAgIAAxkBAAIOL2guXZn6_d_npOwoYdhhFooAAZvzEQAD6TEbQ255SYCaRv7znI_OAQADAgADcwADNgQ",
     'text': None,
    },

]

async def about_us_kb(photo_index=0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="←", callback_data=f"photo_left_{photo_index}")
    keyboard.button(text="Назад", callback_data="delete_message")
    keyboard.button(text="→", callback_data=f"photo_right_{photo_index}")

    keyboard.adjust(3)
    return keyboard.as_markup()
