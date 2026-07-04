from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.core.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте создаём таблицы (если их нет) — на случай, если Alembic не использовался
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # При завершении — ничего не делаем

app = FastAPI(
    title="Meeting Room Booking Service",
    version="2.3.0",
    lifespan=lifespan
)

app.include_router(v1_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Meeting Room Booking API"}
