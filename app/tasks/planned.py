from app.tasks.celeryfile import celery


@celery.task(name="periodic_task")
def periodic_task():
    print("periodic_task")
