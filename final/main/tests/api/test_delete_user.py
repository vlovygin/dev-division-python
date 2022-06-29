import pytest

from main.tests.base import BaseTestApi

pytestmark = pytest.mark.API


class TestDeleteUser(BaseTestApi):

    def test_delete_user(self):
        """
        Удалить пользователя

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. DELETE http://<APP_HOST>:<APP_PORT>/api/user/<username>

        Ожидаемый результат:
        Status: 204

        Пользователь удаляется из БД
        """

        user = self.create_user()

        r = self.api_client.delete_user(user.username)

        assert r.status_code == 204
        db_user = self.db_client.get_user(username=user.username)
        assert not db_user, f"User {user.username} not deleted from DB"

    def test_delete_not_exists_user(self):
        """
        Удалить НЕ существующего пользователя

        Шаги выполнения:
        1. DELETE http://<APP_HOST>:<APP_PORT>/api/user/<username>

        Ожидаемый результат:
        Status: 404
        Body:
        {
            "detail": "User does not exist!",
            "status": "failed"
        }
        """

        user = self.data_manager.user()

        r = self.api_client.delete_user(user.username)

        assert r.status_code == 404
        assert r.json() == {"detail": "User does not exist!", "status": "failed"}

    def test_delete_user_by_not_auth_client(self):
        """
        Удалить пользователя из под неавторизованного клиента

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. DELETE http://<APP_HOST>:<APP_PORT>/api/user/<username>

        Ожидаемый результат:
        Status: 401
        Body:
        {
            "detail": "session not present",
            "status": "error",
            "url": <url>
        }
        """

        user = self.create_user()

        r = self.api_not_auth_client.delete_user(user.username)

        assert r.status_code == 401, "API client must be authenticated"
        assert r.json() == {"detail": "session not present", "status": "error", "url": f"{r.request.url}"}
