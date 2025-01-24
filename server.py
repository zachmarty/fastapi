from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_server.router import router as item_router
from fastapi_server.models import create_tables, drop_tables
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi_server.orm import SchedulerORM
from fastapi_server.router import get_and_save_product


scheduler = AsyncIOScheduler()


async def get_schedules():
    schedules = await SchedulerORM.get_all()
    return schedules


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await drop_tables()
    await create_tables()
    schedules = await get_schedules()
    for schedule in schedules:
        scheduler.add_job(
            get_and_save_product, "interval", minutes=30, args=[schedule.article]
        )
        print("schedule", schedule.article, "added")
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(item_router)
