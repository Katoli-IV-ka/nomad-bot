from aiogram import Dispatcher

from handlers.dev import routers_from_dev
from handlers.menu import routers_from_menu
from handlers.booking import routers_from_booking
from handlers.verification import routers_from_verification
from handlers.notification import notification_routers

from handlers import delete_message

def loader(dp: Dispatcher):
    dp.include_routers(
        *routers_from_dev,
        *routers_from_menu,
        *routers_from_booking,
        *routers_from_verification,
        *notification_routers,

        delete_message.router,
    )
