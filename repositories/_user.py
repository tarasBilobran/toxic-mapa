from __future__ import annotations

import typing
import uuid
import enum

import asyncpg
import pydantic


class UserStatus(str, enum.Enum):
    DEFAULT = 'default'
    ADMIN = 'admin'
    BLOCKED = 'blocked'


class User(pydantic.BaseModel):
    id: uuid.UUID
    telegram_id: int
    phone: typing.Optional[str]
    username: str
    status: UserStatus


class AsyncPgIncidentUserRepository:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def get(self, *, id: uuid.UUID) -> User | None:
        row = await self._conn.fetchrow(
            """
            SELECT *
            FROM public.users
            WHERE id = $1
            """,
            id
        )

        if row is not None:
            return User.parse_obj(row)

    async def get_by_telegram_id(self, *, tg_id: int) -> User | None:
        row = await self._conn.fetchrow(
            """
            SELECT *
            FROM public.users
            where telegram_id = $1;
            """,
            tg_id
        )

        if row is not None:
            return User.parse_obj(row)

    async def save(self, *, user: User) -> None:
        await self._conn.execute(
            """
            INSERT INTO public.users (id, telegram_id, phone, username, status)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (ID)
            DO UPDATE SET username=$4, status=$5;
            """,
            user.id, user.telegram_id, user.phone, user.username, user.status
        )
