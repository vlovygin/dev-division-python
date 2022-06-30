import pytest

from tests.base import BaseTestApi

pytestmark = pytest.mark.API


class TestAcceptUser(BaseTestApi):

    @pytest.mark.parametrize("access", [0, None])
    def test_accept_user(self, access):
        """
        Разблокировать пользователя без доступа

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/accept

        Ожидаемый результат:
        Status: 200 OK
        Content-Type: application/json
        Body:
        {
            "detail": "User access granted",
            "status": ""
        }

        Пользователю проставляется access = 1 в БД.
        """

        user = self.create_user(access=access)

        r = self.api_client.accept_user(username=user.username)

        assert r.status_code == 200
        assert r.json() == {"detail": "User access granted", "status": ""}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.access == 1, f"User {user.username} not accepted in DB"

    def test_accept_accessed_user(self):
        """
        Разблокировать пользователя с доступом

        Предусловия:
        1. Создать нового пользователя с доступом

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/accept

        Ожидаемый результат:
        Status: 400 OK
        Content-Type: application/json
        Body:
        {
            "detail": "User is already accessed",
            "status": "failed"
        }
        """

        user = self.create_user(access=1)

        r = self.api_client.block_user(username=user.username)

        assert r.status_code == 400
        assert r.json() == {"detail": "User is already accessed", "status": "failed"}

    def test_access_not_exists_user(self):
        """
        Разблокировать НЕ существующего пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/block

        Ожидаемый результат:
        Status: 404
        Body:
        {
            "detail": "User does not exist",
            "status": "failed"
        }
        """

        user = self.data_manager.user()

        r = self.api_client.accept_user(username=user.username)

        assert r.status_code == 404
        assert r.json() == {"detail": "User does not exist", "status": "failed"}

    def test_accept_user_by_not_auth_client(self):
        """
        Разблокировать пользователя из под неавторизованного клиента

        Предусловия:
        1. Создать нового разблокированного пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/accept

        Ожидаемый результат:
        Status: 401
        Body:
        {
            "detail": "session not present",
            "status": "error",
            "url": <url>
        }
        """

        user = self.create_user(access=0)

        r = self.api_not_auth_client.accept_user(username=user.username)

        assert r.status_code == 401, "API client must be authenticated"
        assert r.json() == {"detail": "session not present", "status": "error", "url": f"{r.request.url}"}
