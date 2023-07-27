from __future__ import annotations

import contextlib
import typing
from pathlib import Path

import asyncpg

from config import Envs
from repositories import AsyncPgIncidentReportRepository, AsyncPgIncidentUserRepository

_APP_CONTEXT: "AppContext" | None = None


def get_app_context() -> AppContext:
    if _APP_CONTEXT is None:
        raise RuntimeError

    return _APP_CONTEXT


@contextlib.asynccontextmanager
async def default_app_context():
    context = AppContext()
    global _APP_CONTEXT
    _APP_CONTEXT = context
    try:
        yield context
    finally:
        _APP_CONTEXT = None


class AppContext:
    def get_config(self) -> Envs:
        env_file = Path(__file__).parent / ".env"
        return Envs(_env_file=env_file)
    @contextlib.asynccontextmanager
    async def db_pool(self):
        db_config = self.get_config().db
        async with asyncpg.create_pool(
                host=db_config.host,
                port=db_config.port,
                user=db_config.user,
                password=db_config.password,
                database=db_config.db,
        ) as pool:
            yield pool

    @contextlib.asynccontextmanager
    async def report_repository(self):
        async with self.db_pool() as pool:
            async with pool.acquire() as conn:
                yield AsyncPgIncidentReportRepository(conn=conn)

    @contextlib.asynccontextmanager
    async def user_repository(self) -> typing.AsyncGenerator[AsyncPgIncidentUserRepository, None]:
        async with self.db_pool() as pool:
            async with pool.acquire() as conn:
                yield AsyncPgIncidentUserRepository(conn=conn)
