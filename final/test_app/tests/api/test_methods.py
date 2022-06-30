import pytest

from tests.base import BaseTestApi

pytestmark = pytest.mark.API


class TestMethods(BaseTestApi):

    def test_not_allowed_method(self):
        """
        Выполнить запрос с неподдерживаемым HTTP методом

        Шаги выполнения:
        1. GET http://<APP_HOST>:<APP_PORT>/api/user

        Ожидаемый результат:
        Status: 405 OK
        Body:
        {
            "detail": "method not allowed",
            "status": "failed"
        }
        """

        base_url = self.api_client.base_url
        r = self.api_client._request("GET", f"{base_url}/api/user")

        assert r.status_code == 405
        assert r.json() == {"detail": "method not allowed", "status": "failed"}
