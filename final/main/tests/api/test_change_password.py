import pytest

from main.tests.base import BaseTestApi
from main.utils.data_manager import fake

pytestmark = pytest.mark.API


class TestChangeUserPassword(BaseTestApi):

    @pytest.mark.parametrize("new_password", [
        ("1 char", fake.bothify("?")),
        ("password", fake.password() + "test"),
        ("255 chars", fake.bothify("?" * 255))
    ], ids=lambda x: x[0])
    def test_change_user_password(self, new_password):
        """
        Сменить пароль пользователя

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. PUT http://<APP_HOST>:<APP_PORT>/api/user/<username>/change-password

        Формат запроса
        Content-Type: application/json
        Body:
        {
            "password": "<new password>"
        }

        Ожидаемый результат:
        Status: 204

        У пользователя изменился пароль в БД
        """

        user = self.create_user()

        r = self.api_client.change_user_password(username=user.username, password=new_password[1])

        assert r.status_code == 204
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.password == new_password[1], f"User {user.username} password not updated in DB"

    def test_change_user_password_to_same_password(self):
        """
        Сменить пароль пользователя с указанием текущего пароля

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. PUT http://<APP_HOST>:<APP_PORT>/api/user/<username>/change-password

        Формат запроса
        Content-Type: application/json
        Body:
        {
            "password": "<new password>"
        }

        Ожидаемый результат:
        Status: 400
        Body:
        {
            "detail": "This password is already in use",
            "status": "failed"
        }
        """

        user = self.create_user()

        r = self.api_client.change_user_password(username=user.username, password=user.password)

        assert r.status_code == 400
        assert r.json() == {"detail": "This password is already in use", "status": "failed"}

    @pytest.mark.parametrize("new_password", [
        ("None", None),
        ("empty", ""),
        ("space", " "),
        ("256 chars", fake.bothify("?" * 256))
    ], ids=lambda x: x[0])
    def test_change_user_invalid_password(self, new_password):
        """
        Сменить пароль пользователя на невалидный

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. PUT http://<APP_HOST>:<APP_PORT>/api/user/<username>/change-password

        Формат запроса
        Content-Type: application/json
        Body:
        {
            "password": "<new password>"
        }

        Ожидаемый результат:
        Status: 400
        Body:
        {
            "detail": "Incorrect password",
            "status": "failed"
        }
        """

        user = self.create_user()

        r = self.api_client.change_user_password(username=user.username, password=new_password[1])

        assert r.status_code == 400
        assert r.json() == {"detail": "Incorrect password", "status": "failed"}

    def test_change_not_exists_user_password(self):
        """
        Сменить пароль НЕ существующего пользователя

        Шаги выполнения:
        1. PUT http://<APP_HOST>:<APP_PORT>/api/user/<username>/change-password

        Формат запроса
        Content-Type: application/json
        Body:
        {
            "password": "<new password>"
        }

        Ожидаемый результат:
        Status: 404
        Body:
        {
            "detail": "User does not exist",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        new_password = "test" + user.password

        r = self.api_client.change_user_password(username=user.username, password=new_password)

        assert r.status_code == 404
        assert r.json() == {"detail": "User does not exist", "status": "failed"}

    def test_change_user_password_by_not_auth_client(self):
        """
        Сменить пароль пользователя из под неавторизованного клиента

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. PUT http://<APP_HOST>:<APP_PORT>/api/user/<username>/change-password

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

        r = self.api_not_auth_client.change_user_password(username=user.username, password="test")

        assert r.status_code == 401, "API client must be authenticated"
        assert r.json() == {"detail": "session not present", "status": "error", "url": f"{r.request.url}"}
