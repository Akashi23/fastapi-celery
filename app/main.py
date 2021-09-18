import os
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from worker.celery_app import celery_app
from config import REDIS_STORE
from redis import Redis
import json

log = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_instance = Redis.from_url(REDIS_STORE)

#For testing

# @app.on_event("startup")
# async def startup_event():
#     task_name = None
#     # set correct task name based on the way you run the example
#     if not bool(os.getenv('DOCKER')):
#         task_name = "app.worker.celery_worker.test_celery"
#     else:
#         task_name = "app.app.worker.celery_worker.test_celery"

#     task = celery_app.send_task(task_name)
#     log.info(f"HHH {task}")


@app.get("/{route}")
async def root(route: str):
    """Use Route for getting data about flight price"""
    try:
        calendar: dict = json.loads(redis_instance.get(route))
    except ValueError as e:
        log.warning(e)
        raise HTTPException(status_code=404, detail="Route not found")
    log.info("Successful received! route:{route}")
    return calendar
