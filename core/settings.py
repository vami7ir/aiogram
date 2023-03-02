from environs import Env
from dataclasses import dataclass


@dataclass()
class Bots:
    bot_token: str
    admin_id: str
    redis_user: str
    redis_password: str
    redis_host: str
    redis_port: str
    redis_db_name_0: str
    redis_db_name_1: str
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    db_timeout: str


@dataclass()
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str("API_BOT_TOKEN"),
            admin_id=env.str("ADMIN_ID"),
            redis_user=env.str("REDIS_USER"),
            redis_password=env.str("REDIS_PASSWORD"),
            redis_host=env.str("REDIS_HOST"),
            redis_port=env.str("REDIS_PORT"),
            redis_db_name_0=env.str("REDIS_DB_NAME_0"),
            redis_db_name_1=env.str("REDIS_DB_NAME_1"),
            db_user=env.str("BD_USER"),
            db_password=env.str("DB_PASSWORD"),
            db_name=env.str("DB_NAME"),
            db_host=env.str("DB_HOST"),
            db_port=env.str("DB_PORT"),
            db_timeout=env.str("DB_TIMEOUT"),
        )
    )


settings = get_settings('config')
