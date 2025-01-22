from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_server.router import router as item_router
from fastapi_server.models import create_tables, drop_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(item_router)