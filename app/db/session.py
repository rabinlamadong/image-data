from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import Settings


def get_engine(db_url: str):
    return create_engine(db_url)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def create_session_manager(_settings: Settings) -> async_sessionmaker[AsyncSession]:
    postgres_url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    engine = create_async_engine(
        postgres_url.format(
            user=_settings.DB_USER,
            password=_settings.DB_PASSWORD,
            host=_settings.DB_HOST,
            port=_settings.DB_PORT,
            database=_settings.DB_NAME,
        ),
        pool_size=_settings.DB_POOL_SIZE,
        max_overflow=0,
        pool_recycle=60,
    )
    return async_sessionmaker(engine, expire_on_commit=False)
