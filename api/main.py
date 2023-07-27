from typing import List

import pydantic
from fastapi import FastAPI

from app_context import default_app_context
from repositories import ReportStatus

api = FastAPI()


class HealthResponse(pydantic.BaseModel):
    status: bool


class ReportsResponse(pydantic.BaseModel):
    locations: List[str]


@api.get("/get_status", response_model=HealthResponse)
async def check_health():
    return HealthResponse(status=True)


@api.get("/get_reports_locations", response_model=ReportsResponse)
async def get_reports_locations():
    async with default_app_context() as context:
        async with context.db_pool() as pool:
            async with pool.acquire() as conn:
                rows = await conn.fetch(
                    """
                    SELECT location
                    FROM public.poison_report
                    WHERE status = $1;
                    """,
                    ReportStatus.ACTIVE
                )
    return ReportsResponse(locations=[row["location"] for row in rows])
