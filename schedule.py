from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from handlers.notification.notify_client import notify_client
from handlers.notification.notify_staff import notify_staff

scheduler = AsyncIOScheduler(
    job_defaults={
        'misfire_grace_time': 60*60,  #1 час просрочки
    }
)


async def notify():
    await notify_staff()
    await notify_client()

scheduler.add_job(
    func=notify,
    trigger=CronTrigger.from_crontab("0 7 * * *") #""
)






