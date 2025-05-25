from aiogram.fsm.state import State, StatesGroup

class BookingState(StatesGroup):
    check_in = State()   # Дата заезда
    check_out = State()  # Дата выезда
    options_package_selection = State()
    share_contact = State()
    shooting_share_contact = State()
    summary = State()