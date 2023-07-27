from __future__ import annotations

import datetime
import enum
import typing
import uuid

import asyncpg
import pydantic


class ReportStatus(str, enum.Enum):
    # when person needs to review this and approve if needed. Reports in this state won't appear on the map
    PENDING = "pending"
    # when person report was approved and should appear on the screen.
    ACTIVE = "active"


class IncidentReport(pydantic.BaseModel):
    id: uuid.UUID
    reported_by: uuid.UUID
    # WKT location
    location: str
    photos: typing.List[str]
    # With UTC zone
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: ReportStatus
    poison_removed: bool


class AsyncPgIncidentReportRepository:
    def __init__(self, conn: asyncpg.Connection):
        self._conn = conn

    async def count_pending_reports_for_user(self, *, requested_by: uuid.UUID) -> int:
        return await self._conn.fetchval(
            """
            SELECT COUNT(*)
            FROM public.poison_report
            WHERE status = $1 AND requested_by = $2;
            """,
            ReportStatus.PENDING,
            requested_by
        )

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
            )
            ON CONFLICT (id)
            DO UPDATE SET
                status = $5,
                updated_at = $8;
            ;
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

    async def delete_by_id(self, *, id: uuid.UUID) -> None:
        await self._conn.execute(
            """
            DELETE FROM public.poison_report           
            WHERE id = $1;
            """,
            id
        )

    async def delete_by_reported_by(self, *, reported_by: uuid.UUID) -> None:
        await self._conn.execute(
            """
            DELETE FROM public.poison_report           
            WHERE reported_by = $1;
            """,
            reported_by
        )
