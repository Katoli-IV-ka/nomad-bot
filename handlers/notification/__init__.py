from . import notify_staff, notify_client

notification_routers = [
    notify_staff.router,
    notify_client.router,
]