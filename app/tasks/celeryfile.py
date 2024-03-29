from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks", "app.tasks.planned"],
)


celery.conf.beat_schedule = {
    "any_name": {
        "task": "periodic_task",
        "schedule": 10,
        # 'schedule': crontab(minute='30', hour='15')
    }
}
