from aiogram import Dispatcher

from handlers.admin import routers_from_admin
from handlers.user import routers_from_user
from handlers.booking import routers_from_booking

def loader(dp: Dispatcher):
    dp.include_routers(
        *routers_from_admin,
        *routers_from_user,
        *routers_from_booking,
    )
