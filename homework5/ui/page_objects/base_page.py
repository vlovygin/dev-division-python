import logging
from urllib.parse import urljoin

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import app_config


class BasePage:
    path = None

    def __init__(self, driver, load=False):
        self.driver: WebDriver = driver
        self.base_url: str = app_config["base_url"]
        self.logger: logging.Logger = logging.getLogger('test')

        if load:
            self.load()

    @property
    def current_url(self):
        return self.driver.current_url

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 30
        return WebDriverWait(self.driver, timeout=timeout)

    def action_chain(self):
        return ActionChains(self.driver)

    def load(self):
        url = urljoin(self.base_url, self.path)
        with allure.step(f"Open page {url}"):
            self.driver.get(url)
            return self

    def is_page_loaded(self, timeout=None):
        try:
            self.wait(timeout).until(lambda d: self.path in d.current_url)
            return True
        except TimeoutException:
            return False

    def find(self, locator: tuple, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def finds(self, locator: tuple, timeout=None):
        try:
            self.find(locator, timeout)
        finally:
            return self.driver.find_elements(*locator)

    def click(self, locator: tuple, timeout=None):
        self.wait(timeout).until(EC.element_to_be_clickable(locator))
        self.find(locator).click()

    def send_keys(self, locator: tuple, text: str):
        self.wait().until(EC.visibility_of_element_located(locator))
        self.find(locator).clear()
        self.find(locator).send_keys(text)

    def upload_file(self, locator: tuple, path: str):
        self.find(locator).send_keys(path)

    def wait_miss(self, locator: tuple, timeout=None):
        self.wait(timeout).until_not(EC.presence_of_element_located(locator))

    def wait_stale(self, element: WebElement, timeout=None):
        self.wait(timeout).until(EC.staleness_of(element))
