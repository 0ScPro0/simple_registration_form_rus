from .models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

# --------------------------------------------------------------SQLAlchemy----------------------------------------------------

# Create the SQLAlchemy engine
engine = create_async_engine("sqlite+aiosqlite:///database/database.db", echo = True)

# Create an async session maker
session_maker = async_sessionmaker(bind = engine, class_ = AsyncSession, expire_on_commit = False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)