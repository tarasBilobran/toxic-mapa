import datetime
import typing
import uuid
from pathlib import Path

import aiofiles
import pydantic

DIR = Path(__file__).parent / "tmp"


class IncidentReport(pydantic.BaseModel):
    id: uuid.UUID
    reported_by: str
    # WKT location
    location: str
    photos: typing.List
    # With UTC zone
    created_at: datetime.datetime


class IncidentReportRepository(typing.Protocol):
    async def save(self, *, report: IncidentReport):
        raise NotImplementedError()


class JSONReportRepository(IncidentReportRepository):
    async def save(self, *, report: IncidentReport):
        async with aiofiles.open(DIR / f"{report.id}.json", "w") as file:
            await file.write(report.model_dump_json(indent=4))

