from typing import AsyncGenerator
from urllib.parse import urlparse

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings
from .models import User


parsed_db_url = urlparse(settings.DATABASE_URL)

async_db_connection_url = ("mssql+aioodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server+Native+Client+10.0%7D%3BSERVER%3Dnp%3A%5C%5C.%5Cpipe%5CMSSQL%24SQLEXPRESSRICG%5Csql%5Cquery%3BDATABASE%3DMYOBPremierMirrorDB_test%3BUID%3Dsa%3BPWD%3Dpwd%24123")

# Disable connection pooling for serverless environments like Vercel
engine = create_async_engine(async_db_connection_url, poolclass=NullPool)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=settings.EXPIRE_ON_COMMIT
)


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
