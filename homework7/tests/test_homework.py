import pytest

from db.base import MysqlBase
from db.models import RequestsCount, MethodsCount, TopRequestsUrl, TopRequestsSize4xx, TopRequestsIp5xx


class TestHomework(MysqlBase):

    @pytest.mark.parametrize("table, expected_row_count", [
        (RequestsCount, 1),
        (MethodsCount, 4),
        (TopRequestsUrl, 10),
        (TopRequestsSize4xx, 5),
        (TopRequestsIp5xx, 5)
    ], ids=[
        "Total requests",
        "Grouping http request methods",
        "Top 10 requests url",
        "Top 5 size requests with client error",
        "Top 5 IP requests with server error"
    ])
    def test_homework_tables_count_rows(self, table, expected_row_count):
        row_count = self.mysql.session.query(table).count()

        assert row_count == expected_row_count, \
            f"Table {table.__name__} contains {row_count} rows, but expected {expected_row_count}"
