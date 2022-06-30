import pytest

from tests.base import BaseTestApi
from utils.data_manager import fake

pytestmark = pytest.mark.API


class TestAddUser(BaseTestApi):

    def test_add_user(self):
        """
        Добавить нового пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        Флаг access по умолчанию выставляется в 1
        """

        user = self.data_manager.user()

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.access == 1, f"User {user.username} not added to DB"

    @pytest.mark.parametrize("name", [
        ("1 char", fake.bothify("?")),
        ("name", fake.name()),
        ("45 chars", fake.bothify("?" * 45))
    ], ids=lambda x: x[0])
    def test_add_user_valid_name(self, name):
        """
        Добавить пользователя с валидным name

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        """

        user = self.data_manager.user()
        user.name = name[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.name == user.name, f"User {user.username} name is different in DB"

    @pytest.mark.parametrize("name", [
        ("None", None),
        ("empty", ""),
        ("space", " "),
        ("46 chars", fake.bothify("?" * 46))
    ], ids=lambda x: x[0])
    def test_add_user_invalid_name(self, name):
        """
        Добавить пользователя с невалидным name

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "Invalid name",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        user.name = name[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "Invalid name", "status": "failed"}

    @pytest.mark.parametrize("surname", [
        ("1 char", fake.bothify("?")),
        ("surname", fake.last_name()),
        ("255 chars", fake.bothify("?" * 255))
    ], ids=lambda x: x[0])
    def test_add_user_valid_surname(self, surname):
        """
        Добавить пользователя с валидным surname

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        """

        user = self.data_manager.user()
        user.surname = surname[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.surname == user.surname, f"User {user.username} surname is different in DB"

    @pytest.mark.parametrize("surname", [
        ("None", None),
        ("empty", ""),
        ("space", " "),
        ("256 chars", fake.bothify("?" * 256))
    ], ids=lambda x: x[0])
    def test_add_user_invalid_surname(self, surname):
        """
        Добавить пользователя с невалидным surname

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "Incorrect surname",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        user.surname = surname[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "Incorrect surname", "status": "failed"}

    @pytest.mark.parametrize("middle_name", [
        ("None", None),
        ("1 char", fake.bothify("?")),
        ("middle_name", fake.middle_name()),
        ("255 chars", fake.bothify("?" * 255))
    ], ids=lambda x: x[0])
    def test_add_user_valid_middle_name(self, middle_name):
        """
        Добавить пользователя с валидным middle_name

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        """

        user = self.data_manager.user()
        user.middle_name = middle_name[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.middle_name == user.middle_name, f"User {user.username} middle_name is different in DB"

    @pytest.mark.parametrize("middle_name", [
        ("empty", ""),
        ("space", " "),
        ("256 chars", fake.bothify("?" * 256))
    ], ids=lambda x: x[0])
    def test_add_user_invalid_middle_name(self, middle_name):
        """
        Добавить пользователя с невалидным middle_name

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "Incorrect middle_name",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        user.middle_name = middle_name[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "Incorrect middle_name", "status": "failed"}

    @pytest.mark.parametrize("username", [
        ("6 char", fake.bothify("?")),
        ("username", fake.bothify("?#" * 5)),
        ("16 chars", fake.bothify("?" * 16))
    ], ids=lambda x: x[0])
    def test_add_user_valid_username(self, username):
        """
        Добавить пользователя с валидным username

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        """

        user = self.data_manager.user()
        user.username = username[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        assert self.db_client.get_user(username=user.username), f"User {user.username} not added at DB"

    def test_add_already_exists_username(self):
        """
        Добавить пользователя с уже существующим username

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body с указанием username из предусловия:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "User already exists",
            "status": "failed"
        }
        """

        _user = self.create_user()

        user = self.data_manager.user()
        user.username = _user.username

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "User already exists", "status": "failed"}

    @pytest.mark.parametrize("username", [
        ("None", None),
        ("empty", ""),
        ("space", " "),
        ("5 chars", fake.bothify("?" * 5)),
        ("17 chars", fake.bothify("?" * 17))
    ], ids=lambda x: x[0])
    def test_add_user_invalid_username(self, username):
        """
        Добавить пользователя с невалидным username

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "Incorrect username",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        user.username = username[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "Incorrect username", "status": "failed"}

    @pytest.mark.parametrize("email", [
        ("email", f"{fake.uuid4()}{fake.email()}"),
        ("6 char email", f"{fake.uuid4()}@q.q"[-6:]),
        ("64 chars email", "{fake.uuid4() * 2}{fake.email()}"[-64:])
    ], ids=lambda x: x[0])
    def test_add_user_valid_email(self, email):
        """
        Добавить пользователя с валидным email

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        """

        user = self.data_manager.user()
        user.email = email[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.email == user.email, f"User {user.username} email is different in DB"

    def test_add_already_exists_email(self):
        """
        Добавить пользователя с уже существующем email

        Предусловия:
        1. Создать нового пользователя

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body с указанием email из предусловия:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "User already email",
            "status": "failed"
        }
        """

        _user = self.create_user()

        user = self.data_manager.user()
        user.email = _user.email

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "User already exists", "status": "email"}

    @pytest.mark.parametrize("email", [
        ("None", None),
        ("empty", ""),
        ("space", " "),
        ("65 chars email", f"{fake.uuid4() * 2}{fake.email()}"[-65:]),
        ("invalid email 1", "test_qa"),
        ("invalid email 2", "test_qa@"),
        ("invalid email 3", "@test_qa.ru")  # etc..
    ], ids=lambda x: x[0])
    def test_add_user_invalid_email(self, email):
        """
        Добавить пользователя с невалидным email

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "Incorrect email",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        user.email = email[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "Incorrect email", "status": "failed"}

    @pytest.mark.parametrize("password", [
        ("1 char", fake.bothify("?")),
        ("password", fake.password()),
        ("255 chars", fake.bothify("?" * 255))
    ], ids=lambda x: x[0])
    def test_add_user_password(self, password):
        """
        Добавить пользователя с валидным password

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 201
        Content-Type: application/json
        Body:
        {
            "detail": "User was added",
            "status": "success"
        }

        Пользователь добавляется в БД
        """

        user = self.data_manager.user()
        user.password = password[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 201
        assert r.json() == {"detail": "User was added", "status": "success"}
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.password == user.password, f"User {user.username} password is different in DB"

    @pytest.mark.parametrize("password", [
        ("None", None),
        ("empty", ""),
        ("space", " "),
        ("256 chars", fake.bothify("?" * 256))
    ], ids=lambda x: x[0])
    def test_add_user_invalid_password(self, password):
        """
        Добавить пользователя с невалидным password

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 400
        Content-Type: application/json
        Body:
        {
            "detail": "Invalid password",
            "status": "failed"
        }
        """

        user = self.data_manager.user()
        user.password = password[1]

        r = self.api_client.add_user(user)

        assert r.status_code == 400
        assert r.json() == {"detail": "Invalid password", "status": "failed"}

    def test_add_user_by_not_auth_client(self):
        """
        Добавить пользователя из под неавторизованного клиента

        Шаги выполнения:
        1. POST http://<APP_HOST>:<APP_PORT>/api/user
        Формат запроса
        Content-Type: application/json
        Body:
        {
            "name": "<name>",
            "surname": "<surname>",
            "middle_name": "<middle_name>",
            "username": "<username>",
            "password": "<password>",
            "email": "<email>"
        }

        Ожидаемый результат:
        Status: 401
        Body:
        {
            "detail": "session not present",
            "status": "error",
            "url": <url>
        }
        """

        user = self.data_manager.user()

        r = self.api_not_auth_client.add_user(user)

        assert r.status_code == 401, "API client must be authenticated"
        assert r.json() == {"detail": "session not present", "status": "error", "url": f"{r.request.url}"}
