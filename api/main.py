from typing import List

import pydantic
from fastapi import FastAPI


api = FastAPI()


class HealthResponse(pydantic.BaseModel):
    status: bool


class ReportsResponse(pydantic.BaseModel):
    locations: List[str]


@api.get("get_status/", response_model=HealthResponse)
async def check_health():
    return HealthResponse(status=True)


@api.get("get_reports_locations/", response_model=ReportsResponse)
async def get_reports_locations():
    # TODO: Fetch data from DB.
    return ReportsResponse(locations=[])
