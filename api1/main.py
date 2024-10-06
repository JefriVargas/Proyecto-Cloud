from fastapi import FastAPI
from db.db_setup import Base, async_engine

from routers import user

from utils.middlewares import setup_middlewares

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

# @app.on_event('startup')
# async def on_startup():
#     await create_tables()

setup_middlewares(app)
app.include_router(user.router)
