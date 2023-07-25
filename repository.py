from __future__ import annotations

import datetime
import enum
import typing
import uuid
from pathlib import Path

import asyncpg
import pydantic

DIR = Path(__file__).parent / "tmp"


class ReportStatus(str, enum.Enum):
    # when person needs to review this and approve if needed. Reports in this state won't appear on the map
    PENDING = "pending"
    # when person report was approved and should appear on the screen.
    ACTIVE = "active"
    # After some time report may become inactive.
    INACTIVE = "inactive"


class IncidentReport(pydantic.BaseModel):
    id: uuid.UUID
    reported_by: str
    # WKT location
    location: str
    photos: typing.List[str]
    # With UTC zone
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: ReportStatus
    poison_removed: bool


class IncidentReportRepository(typing.Protocol):
    async def get_pending_reports_count(self) -> int:
        raise NotImplementedError

    async def get_pending_report(self) -> IncidentReport | None:
        raise NotImplementedError

    async def save(self, *, report: IncidentReport):
        raise NotImplementedError


class AsyncPgIncidentReportRepository(IncidentReportRepository):
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def get_pending_reports_count(self) -> int:
        return await self._conn.fetchval(
            """
            SELECT COUNT(*)
            FROM public.poison_report
            WHERE status = $1;
            """,
            ReportStatus.PENDING
        )

    async def get_pending_report(self) -> IncidentReport | None:
        row = await self._conn.fetchrow(
            """
            SELECT *
            FROM public.poison_report
            WHERE status = $1
            ORDER BY updated_at
            LIMIT 1;
            """,
            ReportStatus.PENDING
        )
        if row is not None:
            return IncidentReport.parse_obj(row)

    async def save(self, *, report: IncidentReport):
        await self._conn.execute(
            """
            INSERT INTO public.poison_report (id, reported_by, location, photos, status, poison_removed, created_at, updated_at)
            VALUES (
                $1,
                $2, 
                $3,
                $4::TEXT[],
                $5,
                $6,
                $7,
                $8
            );
            """,
            report.id,
            report.reported_by,
            report.location,
            report.photos,
            report.status,
            report.poison_removed,
            report.created_at,
            report.updated_at
        )