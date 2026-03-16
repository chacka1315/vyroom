import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

if DB_URL is None:
    raise Exception("❌ No DATABASE_URL for this env.")

# psycopg3 async requires: postgresql+psycopg://user:pass@host/db
engine = create_async_engine(
    url=DB_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=30,
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
