from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Импорты из проекта (src/) ---
from src.models import * 
from src.core.database import Base
from src.core.dependencies import get_config

# --- Конфигурация Alembic ---
config = context.config

# Настройка логгирования Alembic из alembic.ini
if config.config_file_name:
    fileConfig(config.config_file_name)

# --- Получение URL БД из .env через get_config ---
db_url = get_config().DATABASE_URL
config.set_main_option("sqlalchemy.url", db_url)

# --- Метаданные моделей для автогенерации миграций ---
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (генерация SQL без подключения к БД)."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,  # сравнение типов колонок
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме (с реальным подключением к БД)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Выбор режима запуска ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
