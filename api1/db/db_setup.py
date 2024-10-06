from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATA_USER = config('DATA_USER')
DATA_PASSWORD = config('DATA_PASSWORD')
HOST = config('HOST')
PORT = config('DB_PORT')
DATABASE_NAME = config('DATABASE_NAME')

SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
    DATA_USER,
    DATA_PASSWORD,
    HOST,
    PORT,
    DATABASE_NAME
)

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()

