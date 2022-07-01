import pytest

from tests.base import BaseTestUi
from ui.pages.login_page import LoginPage

pytestmark = pytest.mark.UI


class TestAuth(BaseTestUi):

    def test_success_login(self):
        """
        Авторизоваться под пользователем

        Предусловия:
        1. Создать нового пользователя

        Шаги:
        1. Перейти на страницу логина
        2. Ввести логин
        3. Ввести пароль
        4. Нажать кнопку Login

        Ожидаемый результат:
        1. Открылась главная страница
        2. В БД поле active = 1
        3. В БД поле start_active_time не пустое
        """

        user = self.create_user()

        login_page = self.get_page(LoginPage)
        main_page = login_page.login(username=user.username, password=user.password)

        assert main_page.is_page_loaded(), "MainPage page not opened"
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.active == 1, "active not set in DB for logged in user"
        assert db_user.start_active_time is not None, "start_active_time not set in DB for logged in user"

    def test_login_page_console_error(self):
        """
        Открыть страницу логина

        Ожидаемый результат:
        1. Проверить консоль на наличие ошибок
        """

        login_page = self.get_page(LoginPage)

        assert not login_page.get_console_error(), "Console has SEVERE message error"

    def test_login_block_user(self):
        """
        Авторизоваться под заблокированным пользователем

        Предусловия:
        1. Создать нового пользователя с access = 0

        Шаги:
        1. Перейти на страницу логина
        2. Ввести логин
        3. Ввести пароль
        4. Нажать кнопку Login

        Ожидаемый результат:
        1.  На странице отобразилось сообщение "Ваша учетная запись заблокирована"
        """

        hint = "Ваша учетная запись заблокирована"
        user = self.create_user(access=0)

        login_page = self.get_page(LoginPage)
        login_page.login(username=user.username, password=user.password)

        assert login_page.get_hint_text() == hint, f"{hint} not shown"

    def test_validate_login_form_fields(self):
        """
        Провалидировать поля формы логина

        Шаги:
        1. Перейти на страницу логина
        2. Получить атрибуты полей формы логина

        Ожидаемый результат:
        1. Поля формы соответствуют валидации
        """

        login_page = self.get_page(LoginPage)

        assert login_page.get_username_attribute("required") == "true", "Username not required field"
        assert login_page.get_username_attribute("minlength") == "6", "Username minlength not 6"
        assert login_page.get_username_attribute("maxlength") == "16", "Username maxlength not 16"

        assert login_page.get_password_attribute("required") == "true", "Password not required field"
        assert login_page.get_password_attribute("minlength") == "1", "Password minlength not 1"
        assert login_page.get_password_attribute("maxlength") == "255", "Password maxlength not 255"

    def test_login_with_incorrect_password(self):
        """
        Авторизоваться с указанием некорректного пароля

        Предусловия:
        1. Создать нового пользователя

        Шаги:
        1. Перейти на страницу логина
        2. Ввести логин
        3. Ввести некорректный пароль
        4. Нажать кнопку Login

        Ожидаемый результат:
        1. На странице отобразилось сообщение "Invalid username or password"
        """

        hint = "Invalid username or password"
        user = self.create_user()

        login_page = self.get_page(LoginPage)
        login_page.login(username=user.username, password=user.password[:-1])

        assert login_page.get_hint_text() == hint, f"{hint} not shown"

    @pytest.mark.parametrize("params", [
        ("Spaces in login", " " * 6, "password", "Необходимо указать логин для авторизации"),
        ("Spaces in password", "my_login", " ", "Необходимо указать пароль для авторизации"),
        ("Start space in password", "my_login", "not_exist_password", "Invalid username or password")
    ], ids=lambda x: x[0])
    def test_incorrect_login(self, params):
        """
        Авторизоваться с указанием некорректного логина/пароля

        Шаги:
        1. Перейти на страницу логина
        2. Ввести логин
        3. Ввести пароль
        4. Нажать кнопку Login

        Ожидаемый результат:
        1. На странице отобразилось сообщение об ошибке
        """

        username, password, hint = params[1:]

        login_page = self.get_page(LoginPage)
        login_page.login(username=username, password=password)

        assert login_page.get_hint_text() == hint, f"{hint} not shown"

    def test_navigate_to_reg_page(self):
        """
        Перейти на страницу регистрации

        Шаги:
        1. Перейти на страницу логина
        2. Перейти по ссылке Create an account

        Ожидаемый результат:
        1. Открылась страница регистрации
        """

        login_page = self.get_page(LoginPage)
        reg_page = login_page.navigate_to_reg_page()

        assert reg_page.is_page_loaded(), "Registration page not loaded"
