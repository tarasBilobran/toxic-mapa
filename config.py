from pathlib import Path
from dotenv import load_dotenv

import pydantic

load_dotenv()


class DBConfig(pydantic.BaseSettings):
    host: str
    port: int = 5432
    user: str
    password: str
    db: str


class Envs(pydantic.BaseSettings):
    tg_api_key: str
    db: DBConfig
    # TODO Add your id for admin panel. Use https://t.me/getmyid_bot.
    admins: list[int] = pydantic.Field(default_factory=lambda : [781766999, 339833320])

# TODO (TB): Example of docker-compose usage with .env files
#   https://stackoverflow.com/questions/29377853/how-can-i-use-environment-variables-in-docker-compose
