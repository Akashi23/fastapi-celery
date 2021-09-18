from time import sleep
import os


from celery import current_task
from celery.schedules import crontab
from .routes_requests import save_all_route_to_redis


from .celery_app import celery_app

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="0", hour="0"), test_celery.s(), name="Periodic task")


@celery_app.task(acks_late=True)
def test_celery() -> str:
    current_task.update_state(state="PROGRESS", meta={"process_percent": 10})
    received = save_all_route_to_redis()
    current_task.update_state(state="PROGRESS", meta={"process_percent": 90})

    return f"test task return {received}"

celery_app.conf.timezone = 'UTC'

