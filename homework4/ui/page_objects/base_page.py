import logging
from abc import ABC, abstractmethod

import allure
from furl import furl
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from config import config
from ui.page_objects.common import Common


class BasePage(ABC):

    @abstractmethod
    def is_page_loaded(self):
        """We need to check that the page has been loaded"""

    @property
    @abstractmethod
    def path(self):
        """Page Url path"""

    def __init__(self, driver, load=False):
        self.driver: WebDriver = driver
        self.base_url: furl = furl(config["base_url"])
        self.logger: logging.Logger = logging.getLogger('test')

        if load:
            self.load()
        self.is_page_loaded()

    @property
    def common(self):
        return Common(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    def load(self):
        """Open the page by url and path"""

        _url = self.base_url.add(path=self.path).url
        with allure.step(f"Open page {_url}"):
            self.driver.get(_url)
            return self
