import logging
import typing
from datetime import datetime
from pathlib import Path

import allure
import pytest
import requests
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from ui.page_objects.base_page import BasePage
from ui.page_objects.main_page import MainPage

T = typing.TypeVar('T', bound=BasePage)


class BaseTestUI:
    """Base class for UI test classes"""
    authorize = True

    @pytest.fixture(scope='session')
    def cookies(self, config, user):
        url = "https://auth-ac.my.com/auth"
        data = {"email": user.login, "password": user.password}
        headers = {"Referer": config["base_url"]}

        response = requests.post(url, data=data, headers=headers, allow_redirects=False)

        if not response.ok:
            pytest.fail(f'Authorization failed with [{response.status_code}]: {response.text}')

        return response.cookies

    @pytest.fixture(autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        """Setup test environment"""

        self.driver: WebDriver = driver
        self.config: dict = config
        self.base_url: str = config["base_url"]
        self.logger: logging.Logger = logger

        if self.authorize:
            self.logger.info("Prepare authenticated page object ")
            MainPage(self.driver, load=True)

            cookies = request.getfixturevalue("auth_cookies")
            for cookie in cookies:
                cookie_dict = {
                    'domain': ".my.com",
                    'name': cookie.name,
                    'value': cookie.value,
                    'secure': cookie.secure
                }
                self.driver.add_cookie(cookie_dict)

        self.logger.info(f"Setup for <{request._pyfuncitem.nodeid}> is done")

    @pytest.fixture(autouse=True)
    def ui_report(self, driver: WebDriver, request: FixtureRequest, tmp_path: Path, logger: logging.Logger):
        """Create additional artefacts for failed tests"""

        failed_tests_cnt = request.session.testsfailed
        yield

        if request.session.testsfailed > failed_tests_cnt:
            self.logger.error(f"Test <{request._pyfuncitem.nodeid}> failed")

            screenshot_path = tmp_path.joinpath("failure.png")
            driver.save_screenshot(str(screenshot_path))
            allure.attach.file(screenshot_path, 'failure.png', attachment_type=allure.attachment_type.PNG)
            logger.info(f"Screenshot saved at {screenshot_path}")

            if request.config.getoption("--browser") not in "firefox":  # get_log doesnt work at firefox
                browser_log = tmp_path.joinpath("browser.log")
                with open(browser_log, 'w+') as log_file:

                    for entry in driver.get_log('browser'):
                        timestamp = datetime.fromtimestamp(entry["timestamp"] / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')
                        log_file.write(f'{entry["level"]: <8} {timestamp} [{entry["source"]}] {entry["message"]}\n')

                    log_file.seek(0)
                    allure.attach(log_file.read(), "browser.log", attachment_type=allure.attachment_type.TEXT)

                logger.info(f"Browser log saved at {browser_log}")

    def get_page(self, page_class: typing.Type[T], load=True) -> T:
        """Page factory"""

        page = page_class(self.driver, load=load)
        self.logger.info(f"Initializing {page_class.__name__} page object")
        return page
