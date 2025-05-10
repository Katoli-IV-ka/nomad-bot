from . import about_us, our_contacts, my_booking, booking, command_start

routers_from_menu = [
    command_start.router,
    about_us.router,
    our_contacts.router,
    my_booking.router,
    booking.router,
]