from datetime import datetime

import pytest

from h.services.bulk_api.lms_stats import CountsByAssignment, CountsByUser
from h.views.api.bulk.stats import (
    AssignmentStatsSchema,
    get_counts_by_assignment,
    get_counts_by_user,
)


class TestSchema:
    def test_it_is_a_valid_schema(self, schema):
        # Extremely basic self checking that this is a valid JSON schema
        assert not schema.validator.check_schema(schema.schema)

    @pytest.fixture
    def schema(self):
        return AssignmentStatsSchema()


@pytest.mark.usefixtures("bulk_stats_service", "with_auth_client")
class TestBulkGroup:
    def test_assignment(self, pyramid_request, assignment_request, bulk_stats_service):
        bulk_stats_service.get_counts_by_user.return_value = [
            CountsByUser(
                display_name=f"display_name{i}",
                userid=i,
                annotations=i,
                replies=i,
                last_activity=datetime.now(),
            )
            for i in range(3)
        ]

        response = get_counts_by_user(pyramid_request)

        bulk_stats_service.get_counts_by_user.assert_called_once_with(
            groups=assignment_request["filter"]["groups"],
            assignment_id=assignment_request["filter"]["assignment_id"],
        )
        return_data = [
            {
                "display_name": row.display_name,
                "userid": row.userid,
                "annotations": row.annotations,
                "replies": row.replies,
                "last_activity": row.last_activity.isoformat(),
            }
            for row in bulk_stats_service.get_counts_by_user.return_value
        ]
        assert response.json == return_data
        assert response.status_code == 200
        assert response.content_type == "application/x-ndjson"

    def test_course(self, pyramid_request, course_request, bulk_stats_service):
        bulk_stats_service.get_counts_by_assignment.return_value = [
            CountsByAssignment(
                assignment_id=f"assignmnt_id_{i}",
                annotations=i,
                replies=i,
                last_activity=datetime.now(),
            )
            for i in range(3)
        ]

        response = get_counts_by_assignment(pyramid_request)

        bulk_stats_service.get_counts_by_assignment.assert_called_once_with(
            groups=course_request["filter"]["groups"]
        )
        return_data = [
            {
                "assignment_id": row.assignment_id,
                "annotations": row.annotations,
                "replies": row.replies,
                "last_activity": row.last_activity.isoformat(),
            }
            for row in bulk_stats_service.get_counts_by_assignment.return_value
        ]
        assert response.json == return_data
        assert response.status_code == 200
        assert response.content_type == "application/x-ndjson"

    @pytest.fixture
    def assignment_request(self, pyramid_request):
        pyramid_request.json = {
            "filter": {
                "groups": ["3a022b6c146dfd9df4ea8662178eac"],
                "assignment_id": "ASSIGNMENT_ID",
            },
        }

        return pyramid_request.json

    @pytest.fixture
    def course_request(self, pyramid_request):
        pyramid_request.json = {
            "filter": {"groups": ["3a022b6c146dfd9df4ea8662178eac"]},
        }

        return pyramid_request.json
