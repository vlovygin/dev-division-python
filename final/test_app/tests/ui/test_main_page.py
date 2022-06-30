import pytest

from tests.base import BaseTestUi
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage

pytestmark = pytest.mark.UI


class TestMainPageNotAuthorized(BaseTestUi):
    authorized = False

    def test_open_main_page_not_authorized(self):
        """
        Открыть главную страницу без авторизации

        Шаги:
        1. Перейти на главную страницу

        Ожидаемый результат:
        1. Выполнился переход на страницу авторизации
        2. На странице отобразилось сообщение "This page is available only to authorized users"
        """

        hint = "This page is available only to authorized users"

        self.get_page(MainPage)

        login_page = self.get_page(LoginPage, load=False)
        assert login_page.get_hint_text() == hint, f"{hint} not shown"


class TestMainPageAuth(BaseTestUi):
    authorized = True

    def test_open_main_page_not_authorized(self):
        """
        Открыть главную страницу после авторизации

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу

        Ожидаемый результат:
        1. Отобразилась главная страница
        """

        main_page = self.get_page(MainPage)

        assert main_page.is_page_loaded(), "Main page not loaded"

    def test_logout(self):
        """
        Выполнить выход из личного кабинета

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать Logout

        Ожидаемый результат:
        1. Отобразилась страница авторизации
        """

        main_page = self.get_page(MainPage)

        login_page = main_page.logout()

        assert login_page.is_page_loaded(), "Login page not loaded after logout"


class TestMainPageNavigation(BaseTestUi):
    authorized = True

    def test_navigate_by_brand(self):
        """
        Перейти по ссылке бренда

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке бренда

        Ожидаемый результат:
        1. Отобразилась главная страница
        """

        main_page = self.get_page(MainPage)
        main_page = main_page.navigate_to_brand()

        assert main_page.is_page_loaded(), "Main page not loaded"

    def test_navigate_to_home(self):
        """
        Перейти по ссылке HOME

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Home

        Ожидаемый результат:
        1. Отобразилась главная страница
        """

        main_page = self.get_page(MainPage)
        main_page = main_page.navigate_to_home()

        assert main_page.is_page_loaded(), "Main page not loaded"

    def test_navigate_to_python(self):
        """
        Перейти по ссылке Python

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Python

        Ожидаемый результат:
        1. Выполнился переход на страницу https://www.python.org/
        """

        url = "https://www.python.org/"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_python()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_python_history(self):
        """
        Перейти по ссылке Python history раздела Python

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Python history в разделе Python

        Ожидаемый результат:
        1. Выполнился переход на страницу https://en.wikipedia.org/wiki/History_of_Python
        """

        url = "https://en.wikipedia.org/wiki/History_of_Python"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_python_python_history()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_python_flask(self):
        """
        Перейти по ссылке About Flask раздела Python

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке About Flask в разделе Python

        Ожидаемый результат:
        1. Выполнился переход на страницу https://flask.palletsprojects.com/en/1.1.x/#
        """

        url = "https://flask.palletsprojects.com/en/1.1.x/#"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_linux_about_flask()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_download_centos_7(self):
        """
        Перейти по ссылке Download Centos7 раздела Linux

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Download Centos7 в разделе Linux

        Ожидаемый результат:
        1. Выполнился переход на страницу https://getfedora.org/ru/workstation/download/ FEDORA?
        """

        url = "https://getfedora.org/ru/workstation/download/"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_linux_download_centos_7()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_news(self):
        """
        Перейти по ссылке News раздела Network

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке News в разделе Network

        Ожидаемый результат:
        1. Выполнился переход на страницу https://www.wireshark.org/news/
        """

        url = "https://www.wireshark.org/news/"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_network_news()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_download(self):
        """
        Перейти по ссылке Download раздела Network

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Download в разделе Network

        Ожидаемый результат:
        1. Выполнился переход на страницу https://www.wireshark.org/#download
        """

        url = "https://www.wireshark.org/#download"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_network_download()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_examples(self):
        """
        Перейти по ссылке Examples раздела Network

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Examples в разделе Network

        Ожидаемый результат:
        1. Выполнился переход на страницу https://hackertarget.com/tcpdump-examples/
        """

        url = "https://hackertarget.com/tcpdump-examples/"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_network_examples()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_what_is_api(self):
        """
        Перейти по ссылке What is an API?

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке What is an API?

        Ожидаемый результат:
        1. Выполнился переход на страницу https://en.wikipedia.org/wiki/API
        """
        url = "https://en.wikipedia.org/wiki/API"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_what_is_api()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_internet_future(self):
        """
        Перейти по ссылке Future of internet

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке Future of internet

        Ожидаемый результат:
        1. Выполнился переход на страницу
        https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/
        """

        url = "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_future_internet()

        assert page.current_url == url, f"Page {url} not loaded"

    def test_navigate_to_smtp(self):
        """
        Перейти по ссылке Lets talk about SMTP?

        Предусловие:
        1. Выполнить авторизацию под пользователем

        Шаги:
        1. Перейти на главную страницу
        2. Нажать по ссылке  Lets talk about SMTP?

        Ожидаемый результат:
        1. Выполнился переход на страницу https://ru.wikipedia.org/wiki/SMTP
        """

        url = "https://ru.wikipedia.org/wiki/SMTP"

        main_page = self.get_page(MainPage)
        page = main_page.navigate_to_smtp()

        assert page.current_url == url, f"Page {url} not loaded"


class TestMainPageInfo(BaseTestUi):

    def test_user_info(self):
        """
        Проверить информацию о пользователе

        Предусловие:
        1. Создать нового пользователя
        2. Авторизоваться

        Шаги:
        1. Перейти на главную страницу

        Ожидаемый результат:
        1. В разделе Logged as отображается username
        2. В разделе User отображается информация о name, surname и middle_name
        """

        user = self.create_user()

        login_page = self.get_page(LoginPage)
        main_page = login_page.login(user.username, user.password)

        assert main_page.get_logged_as_info() == user.username, "username not shown"
        assert main_page.get_user_info() == " ".join([user.name, user.surname, user.middle_name]), "User info not shown"

    def test_user_vk_info(self):
        """
        Проверить информацию о VK id пользователя

        Предусловие:
        1. Создать нового пользователя
        2. Авторизоваться
        3. Сделать мок VK id для пользователя

        Шаги:
        1. Перейти на главную страницу

        Ожидаемый результат:
        1. В разделе Logged as отображается username
        2. В разделе User отображается информация о name, surname и middle_name
        """

        vk_id = str(self.data_manager.randint())

        user = self.create_user()
        self.vk_mock_client.add_user(username=user.username, vk_id=vk_id)

        login_page = self.get_page(LoginPage)
        main_page = login_page.login(user.username, user.password)

        assert main_page.get_vk_id() == vk_id, f"VK ID not is {vk_id}"


class TestMainPageFactInfo(BaseTestUi):
    authorized = True

    def test_python_fact(self):
        """
        Отображается случайный мотивационный факт о python

        Шаги:
        1. Перейти на главную страницу

        Ожидаемый результат:
        1. В нижней части страницы отображается случайный мотивационный факт о python
        """

        main_page = self.get_page(MainPage)

        assert main_page.get_fact_text(), "Fact about python not shown"
