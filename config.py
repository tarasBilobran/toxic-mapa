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


env_file = Path(__file__).parent / ".env"
config = Envs(_env_file=env_file)

# TODO (TB): Example of docker-compose usage with .env files
#   https://stackoverflow.com/questions/29377853/how-can-i-use-environment-variables-in-docker-compose
