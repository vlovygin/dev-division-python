import pytest

from main.tests.base import BaseTestApi

pytestmark = pytest.mark.API


class TestBlockUser(BaseTestApi):

    @pytest.mark.parametrize("access", [1, None])
    def test_block_user(self, access):
        """
        Заблокировать пользователя

        Предусловия:
        1. Создать нового НЕ заблокированного пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/block

        Ожидаемый результат:
        Status: 200 OK
        Content-Type: application/json
        Body:
        {
            "detail": "User was blocked",
            "status": ""
        }

        Пользователю проставляется access = 0 в БД.
        """

        user = self.create_user(access=access)

        r = self.api_client.block_user(username=user.username)

        assert r.status_code == 200
        assert r.json() == {"detail": "User was blocked", "status": ""}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.access == 0, f"User {user.username} not blocked in DB"

    def test_block_blocked_user(self):
        """
        Забловировать заблокированного пользователя

        Предусловия:
        1. Создать нового заблокированного пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/block

        Ожидаемый результат:
        Status: 400 OK
        Content-Type: application/json
        Body:
        {
            "detail": "User is already blocked",
            "status": "failed"
        }
        """

        user = self.create_user(access=0)

        r = self.api_client.block_user(username=user.username)

        assert r.status_code == 400
        assert r.json() == {"detail": "User is already blocked", "status": "failed"}

    def test_block_not_exists_user(self):
        """
        Заблокировать НЕ существующего пользователя

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

        r = self.api_client.block_user(username=user.username)

        assert r.status_code == 404
        assert r.json() == {"detail": "User does not exist", "status": "failed"}

    def test_block_user_by_not_auth_client(self):
        """
        Забловировать пользователя из под неавторизованного клиента

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user/<username>/block

        Ожидаемый результат:
        Status: 401
        Body:
        {
            "detail": "session not present",
            "status": "error",
            "url": <url>
        }
        """

        user = self.create_user(access=1)

        r = self.api_not_auth_client.block_user(username=user.username)

        assert r.status_code == 401, "API client must be authenticated"
        assert r.json() == {"detail": "session not present", "status": "error", "url": f"{r.request.url}"}
