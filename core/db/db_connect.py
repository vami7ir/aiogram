import asyncpg

from core.settings import settings


def postgres_connect():
    return asyncpg.create_pool(
        user=settings.bots.db_user,
        password=settings.bots.db_password,
        database=settings.bots.db_name,
        host=settings.bots.db_host,
        port=settings.bots.db_port,
        command_timeout=settings.bots.db_timeout,
    )
