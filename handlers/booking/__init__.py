from . import cancel_booking
from .sammary import accept_summary
from .contact import share_contact
from .contact import to_contact
from .options import select_options, to_select_options, accept_options
from .date import input_date, confirm_date

routers_from_booking = [
    input_date.router,
    confirm_date.router,

    to_select_options.router,
    select_options.router,
    accept_options.router,

    to_contact.router,
    share_contact.router,

    cancel_booking.router,

    accept_summary.router,

]