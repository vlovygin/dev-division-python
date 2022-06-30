import pytest

from tests.base import BaseTestUi
from ui.pages.reg_page import RegPage

pytestmark = pytest.mark.UI


class TestReg(BaseTestUi):

    def test_register_user(self):
        """
        Зарегистрировать нового пользователя

        Шаги:
        1. Открыть страницу регистрации
        2. Заполнить все поля
        3. Установить чекбокс согласия
        4. Нажать Register

        Ожидаемый результат:
        1. Открылась главная страница
        2. Пользователь добавлен в БД
        """

        user = self.data_manager.user()

        reg_page = self.get_page(RegPage)
        main_page = reg_page.register_user(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            email=user.email,
            password=user.password,
            confirm_password=user.password
        )

        assert main_page.is_page_loaded(), "Main page not shown after registration"
        db_user = self.db_client.get_user(username=user.username)
        assert db_user, "User not added to DB"

    def test_register_user_with_exists_username(self):
        """
        Зарегистрировать нового пользователя с существующим username

        Шаги:
        1. Открыть страницу регистрации
        2. Заполнить все поля
        3. Установить чекбокс согласия
        4. Нажать Register

        Ожидаемый результат:
        1. На странице отобразилось сообщение "User already exist"
        """

        hint = "User already exist"
        _user = self.create_user()

        user = self.data_manager.user(username=_user.username)

        reg_page = self.get_page(RegPage)
        reg_page.register_user(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            email=user.email,
            password=user.password,
            confirm_password=user.password
        )

        assert reg_page.get_hint_text() == hint, f"{hint} not shown"
        db_user = self.db_client.get_user(username=user.username)
        assert db_user.email != user.email, "User added to DB"

    def test_register_user_with_exists_email(self):
        """
        Зарегистрировать нового пользователя с существующим email

        Шаги:
        1. Открыть страницу регистрации
        2. Заполнить все поля
        3. Установить чекбокс согласия
        4. Нажать Register

        Ожидаемый результат:
        1. На странице отобразилось сообщение "Email already exist"
        """

        hint = "Email already exist"
        _user = self.create_user()

        user = self.data_manager.user(email=_user.email)

        reg_page = self.get_page(RegPage)
        reg_page.register_user(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            email=user.email,
            password=user.password,
            confirm_password=user.password
        )

        assert reg_page.get_hint_text() == hint, f"{hint} not shown"
        db_user = self.db_client.get_user(username=user.username)
        assert not db_user, "User added to DB"

    def test_register_user_with_not_match_password(self):
        """
        Зарегистрировать нового пользователя указав неверный пароль в подтверждении

        Шаги:
        1. Открыть страницу регистрации
        2. Заполнить все поля
        3. Установить чекбокс согласия
        4. Нажать Register

        Ожидаемый результат:
        1. На странице отобразилось сообщение "Passwords must match"
        """

        hint = "Passwords must match"

        user = self.data_manager.user()

        reg_page = self.get_page(RegPage)
        reg_page.register_user(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            email=user.email,
            password=user.password,
            confirm_password=user.password[:-1]
        )

        assert reg_page.get_hint_text() == hint, f"{hint} not shown"
        db_user = self.db_client.get_user(username=user.username)
        assert not db_user, "User added to DB"

    def test_register_user_with_incorrect_email(self):
        """
        Зарегистрировать нового пользователя с некорректным email

        Шаги:
        1. Открыть страницу регистрации
        2. Заполнить все поля
        3. Установить чекбокс согласия
        4. Нажать Register

        Ожидаемый результат:
        1. На странице отобразилось сообщение об ошибке
        """

        hint = "Invalid email address"
        _user = self.create_user()

        user = self.data_manager.user(email=_user.email)

        reg_page = self.get_page(RegPage)
        reg_page.register_user(
            name=user.name,
            surname=user.surname,
            middle_name=user.middle_name,
            username=user.username,
            email="incorrect_email",
            password=user.password,
            confirm_password=user.password
        )

        assert reg_page.get_hint_text() == hint, f"{hint} not shown"

    def test_validate_registration_form_fields(self):
        """
        Провалидировать поля формы регистрации

        Шаги:
        1. Перейти на страницу регистрации
        2. Получить атрибуты полей формы регистрации

        Ожидаемый результат:
        1. Поля формы соответствуют валидации
        """

        reg_page = self.get_page(RegPage)

        assert reg_page.get_name_attribute("required") == "true", "Name not required field"
        assert reg_page.get_name_attribute("minlength") == "1", "Name minlength not 1"
        assert reg_page.get_name_attribute("maxlength") == "45", "Name maxlength not 45"

        assert reg_page.get_surname_attribute("required") == "true", "Surname not required field"
        assert reg_page.get_surname_attribute("minlength") == "1", "Surname minlength not 1"
        assert reg_page.get_surname_attribute("maxlength") == "255", "Surname maxlength not 255"

        assert not reg_page.get_middle_name_attribute("required"), "Middlename required field"
        assert reg_page.get_middle_name_attribute("minlength") == "1", "Middlename minlength not 1"
        assert reg_page.get_middle_name_attribute("maxlength") == "255", "Middlename maxlength not 255"

        assert reg_page.get_username_attribute("required") == "true", "Username not required field"
        assert reg_page.get_username_attribute("minlength") == "6", "Username minlength not 6"
        assert reg_page.get_username_attribute("maxlength") == "16", "Username maxlength not 16"

        assert reg_page.get_email_attribute("required") == "true", "Email not required field"
        assert reg_page.get_email_attribute("minlength") == "6", "Email minlength not 6"
        assert reg_page.get_email_attribute("maxlength") == "64", "Email maxlength not 64"

        assert reg_page.get_password_attribute("required") == "true", "Password not required field"
        assert reg_page.get_password_attribute("minlength") == "1", "Password minlength not 1"
        assert reg_page.get_password_attribute("maxlength") == "255", "Password maxlength not 255"

        assert reg_page.get_confirm_password_attribute("required") == "true", "Repeat password not required field"
        assert reg_page.get_confirm_password_attribute("minlength") == "1", "Repeat password minlength not 1"
        assert reg_page.get_confirm_password_attribute("maxlength") == "255", "Repeat password maxlength not 255"

        assert reg_page.get_accept_checkbox_attribute("required") == "true", "Accept checkbox not required field"

    def test_navigate_to_login_page(self):
        """
        Перейти на страницу авторизации

        Шаги:
        1. Перейти на страницу регистрации
        2. Перейти по ссылке Log in

        Ожидаемый результат:
        1. Открылась страница авторизации
        """

        reg_page = self.get_page(RegPage)
        login_page = reg_page.navigate_to_login()

        assert login_page.is_page_loaded()
