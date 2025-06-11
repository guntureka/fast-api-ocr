import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import SchedulerNotRunningError
from fastapi import FastAPI

from app.api.index import api_router
from app.core.config import settings

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("RUN_MAIN") == "true" and settings.ENVIRONMENT == "development":
        scheduler.start()

    yield

    try:
        if scheduler.running:
            scheduler.shutdown()
    except SchedulerNotRunningError:
        # Scheduler sudah tidak jalan, abaikan error ini
        pass


app = FastAPI(title="Alibaba Energy Expert API", debug=True, lifespan=lifespan)

app.include_router(api_router)
