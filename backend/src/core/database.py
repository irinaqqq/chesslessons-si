from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.core.logger import logger
from src.core.dependencies import get_config

# --- Инициализация ---
config = get_config()

# --- Конфигурация URL ---
DATABASE_URL = config.DATABASE_URL

ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

DATABASE_KWARGS = dict(echo=False, pool_size=20, max_overflow=30, pool_timeout=60)

# --- Создание движков ---
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    **DATABASE_KWARGS
)

# --- Сессии ---
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# --- Декларативная база ---
Base = declarative_base()

# --- Асинхронная сессия ---
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            try:
                await session.rollback()
            except Exception as rollback_exc:
                logger.warning(f"Error during DB rollback: {rollback_exc}")
        finally:
            logger.debug("Async DB session closed.")