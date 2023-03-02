from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore

from core.settings import settings


def redis_connect_storage():
    return RedisStorage.from_url(
        f'redis://{settings.bots.redis_user}:{settings.bots.redis_password}@{settings.bots.redis_host}:'
        f'{settings.bots.redis_port}/{settings.bots.redis_db_name_0}')


def redis_connect_jobstores():
    return {
        'default': RedisJobStore(
            jobs_key='dispatcher_trips_jobs',
            run_times_key='dispatcher_trips_running',
            username=settings.bots.redis_user,
            password=settings.bots.redis_password,
            host=settings.bots.redis_host,
            db=settings.bots.redis_db_name_1,
            port=settings.bots.redis_port
        )
    }
