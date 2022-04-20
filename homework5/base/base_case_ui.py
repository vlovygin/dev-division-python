import typing

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from base.base import BaseCase
from ui.page_objects import BasePage, MainPage

T = typing.TypeVar('T', bound=BasePage)


class BaseCaseUi(BaseCase):
    """Base class for UI tests"""

    authorize = True

    @pytest.fixture(autouse=True)
    def setup_ui(self, driver, app_config, logger, api_client, tmp_path):
        """Setup test environment"""

        self.driver: WebDriver = driver

        if self.authorize:
            self.logger.info("Prepare authenticated page object")
            MainPage(self.driver, load=True)

            cookies = api_client.session.cookies
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
