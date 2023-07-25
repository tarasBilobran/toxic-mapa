import uuid
from datetime import datetime, timezone

import pytest

from repository import AsyncPgIncidentReportRepository, IncidentReport, ReportStatus


@pytest.fixture
def repo(db_conn):
    return AsyncPgIncidentReportRepository(db_conn)


class TestSaveMethod:
    async def test_report_is_stored_into_db(self, db_conn, repo):
        report = IncidentReport(
            id=uuid.uuid4(),
            reported_by="user",
            location="POINT(0, 0)",
            photos=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            status=ReportStatus.PENDING,
            poison_removed=False,
        )

        await repo.save(report=report)

        actual_rows = await db_conn.fetch("SELECT * FROM public.poison_report;")
        assert len(actual_rows) == 1
        assert IncidentReport.parse_obj(actual_rows[0]) == report
