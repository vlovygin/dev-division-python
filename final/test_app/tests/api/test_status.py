import pytest

from tests.base import BaseTestApi

pytestmark = pytest.mark.API


class TestStatus(BaseTestApi):

    def test_app_status(self):
        """
        Запросить статус приложения

        Шаги выполнения:
        1. GET http://<APP_HOST>:<APP_PORT>/status

        Ожидаемый результат:
        Status: 200 OK
        Content-Type: application/json
        Body:
        {
            "status": "ok"
        }
        """

        r = self.api_client.get_status()

        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_app_status_by_not_auth_client(self):
        """
        Запросить статуса приложения из под неавторизованного клиента

        Шаги выполнения:
        1. GET http://<APP_HOST>:<APP_PORT>/status

        Ожидаемый результат:
        Status: 200 OK
        Content-Type: application/json
        Body:
        {
            "status": "ok"
        }
        """

        r = self.api_not_auth_client.get_status()

        assert r.status_code == 200
        assert r.json() == {"status": "ok"}
