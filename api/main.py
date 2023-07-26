from typing import List

from fastapi import FastAPI
from fastapi_utils.api_model import APIModel

from repository import IncidentReport, ReportStatus

api = FastAPI()


class HealthResponse(APIModel):
    status: bool


class ReportsResponse(APIModel):
    locations: List[str]


@api.get("get_status/", response_model=HealthResponse)
async def check_health():
    return HealthResponse(status=True)


@api.get("get_reports_locations/", response_model=ReportsResponse)
async def get_reports_locations(session: SomeSession):
    # TODO Update Session to real
    locations = session.query(IncidentReport).filter(IncidentReport.status == ReportStatus.ACTIVE).all()
    return ReportsResponse(locations=locations)
