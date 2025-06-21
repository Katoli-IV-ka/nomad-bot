from . import notify_staff, notify_client, notify_manager

notification_routers = [
    notify_staff.router,
    notify_client.router,
    notify_manager.router
]