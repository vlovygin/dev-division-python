import typing
from logging import Logger

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from api.client import MyAppApiClient, VkMockClient
from db.client import DbClient
from models.user import User
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from utils.data_manager import DataManager

T = typing.TypeVar('T', bound=BasePage)


class BaseTest:
    """ Base testsuite for tests """

    @pytest.fixture(autouse=True)
    def setup_base(self, myapp_api_client, myapp_api_not_auth_client, vk_mock_client, db_client, logger, data_manager):
        self.api_client: MyAppApiClient = myapp_api_client
        self.api_not_auth_client: MyAppApiClient = myapp_api_not_auth_client
        self.vk_mock_client: VkMockClient = vk_mock_client
        self.db_client: DbClient = db_client
        self.data_manager: DataManager = data_manager
        self.logger: Logger = logger

    def create_user(self, **kwargs) -> User:
        user = self.data_manager.user(**kwargs)
        self.db_client.add_user(user)

        return user


class BaseTestApi(BaseTest):
    """ Base testsuite for API tests """


class BaseTestUi(BaseTest):
    """ Base testsuite for UI tests """
    authorized = False

    @pytest.fixture(autouse=True)
    def setup_ui(self, driver):
        self.driver: WebDriver = driver

        if self.authorized:
            self.logger.info("Prepare authenticated page object")
            LoginPage(self.driver, load=True)

            cookies = self.api_client.session.cookies
            for cookie in cookies:
                cookie_dict = {
                    "name": cookie.name,
                    "value": cookie.value,
                    "secure": cookie.secure
                }
                self.driver.add_cookie(cookie_dict)

    def get_page(self, page_class: typing.Type[T], load=True) -> T:
        """Page factory"""

        page = page_class(self.driver, load=load)
        self.logger.info(f"Initializing {page_class.__name__} page object")
        return page
