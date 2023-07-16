import datetime
import typing
import uuid
from pathlib import Path

import asyncpg
import pydantic

DIR = Path(__file__).parent / "tmp"


class IncidentReport(pydantic.BaseModel):
    id: uuid.UUID
    reported_by: str
    # WKT location
    location: str
    photos: typing.List[str]
    # With UTC zone
    created_at: datetime.datetime
    # Pending - when person needs to review this and approve if needed.
    #   Reports in this state won't appear on the map
    # Active - when person report was approved and should appear on the screen.
    # Inactive - After some time report may become inactive.
    status: str


class IncidentReportRepository(typing.Protocol):
    async def save(self, *, report: IncidentReport):
        raise NotImplementedError()


class AsyncPgIncidentReportRepository(IncidentReportRepository):
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def save(self, *, report: IncidentReport):
        # TODO: Add proper implementation.
        await self._conn.execute(
            """
            select 1;
            """
        )