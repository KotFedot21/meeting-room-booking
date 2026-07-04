import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path, чтобы импортировать app
sys.path.append(str(Path(__file__).parent.parent))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем настройки и базовый класс
from app.core.config import settings
from app.core.database import Base

# Явно импортируем все модели, чтобы Alembic их увидел
from app.models.user import User
from app.models.room import Room
from app.models.timeslot import TimeSlot
from app.models.booking import Booking

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Метаданные для автогенерации
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    # Убираем "+aiosqlite" для использования синхронного драйвера
    url = settings.DATABASE_URL.replace("+aiosqlite", "")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Убираем "+aiosqlite" для использования синхронного драйвера
    url = settings.DATABASE_URL.replace("+aiosqlite", "")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=url,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
