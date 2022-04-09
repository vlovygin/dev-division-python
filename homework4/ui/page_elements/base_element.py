import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement


class Element:

    def __init__(self, by, value, index=None):
        self.locator: tuple = (by, value)
        self.index: int = index
        self.logger: logging.Logger = logging.getLogger("test")

    def __get__(self, instance, owner):
        self.driver = instance.driver
        return self

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    @property
    def web_element(self) -> WebElement:
        return self._find_web_element()

    def _find_web_element(self):
        self.wait_until_presence()

        if self.index:
            self.logger.info(f"{self.locator}[{self.index}] Find elements")
            return self.driver.find_elements(*self.locator)[self.index]
        else:
            self.logger.info(f"{self.locator} Find element")
            return self.driver.find_element(*self.locator)

    @property
    def text(self):
        return self.web_element.text

    def get_attribute(self, attribute):
        self.logger.info(f"{self.locator} Get attribute {attribute}")
        return self.web_element.get_attribute(attribute)

    def scroll_element_into_view(self):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.web_element)

    def click(self):
        self.logger.info(f"{self.locator} Click on element")
        self.wait_until_clickable()
        self.web_element.click()

    def clear_element(self):
        self.logger.info(f"{self.locator} Clear element")
        self.web_element.clear()

    def send_keys(self, keys):
        self.wait_until_visible()
        self.clear_element()
        self.logger.info(f'{self.locator} Send keys "{keys}"')
        self.web_element.send_keys(keys)

    def upload_file(self, path):
        self.logger.info(f'{self.locator} Upload file "{path}"')
        self.web_element.send_keys(path)

    def wait_until_presence(self, timeout: int = None):
        try:
            self.wait(timeout).until(lambda d: d.find_element(*self.locator))
        except TimeoutException as e:
            err_msg = f"{self.locator} Element not presence"
            self.logger.warning(err_msg)
            raise TimeoutException(err_msg) from e

    def wait_until_visible(self, timeout: int = None):
        try:
            self.wait(timeout).until(EC.visibility_of_element_located(self.locator))
        except TimeoutException as e:
            err_msg = f"{self.locator} Element not visible"
            self.logger.warning(err_msg)
            raise TimeoutException(err_msg) from e

    def wait_until_clickable(self, timeout: int = None):
        try:
            self.wait(timeout).until(EC.element_to_be_clickable(self.locator))
        except TimeoutException as e:
            err_msg = f"{self.locator} Element not clickable"
            self.logger.warning(err_msg)
            raise TimeoutException(err_msg) from e

    def wait_until_not_visible(self, timeout: int = None):
        try:
            self.wait(timeout).until_not(EC.visibility_of_element_located(self.locator))
        except TimeoutException as e:
            err_msg = f"{self.locator} Element is visible"
            self.logger.warning(err_msg)
            raise TimeoutException(err_msg) from e

    def is_visible(self, timeout: int = None):
        self.logger.info(f"{self.locator} Check is element visible")
        try:
            self.wait_until_visible(timeout)
            return True
        except TimeoutException:
            return False


class Elements:

    def __init__(self, by, value):
        self.locator = (by, value)

    def __get__(self, instance, owner):
        self.driver = instance.driver
        return self

    @property
    def web_elements(self):
        return self.driver.find_elements(*self.locator)

    @property
    def elements(self):
        _elements = []
        for index, _ in enumerate(self.web_elements):
            element = Element(self.locator[0], self.locator[1], index)
            element.driver = self.driver
            _elements.append(element)
        return _elements

    def __len__(self):
        return len(self.web_elements)

    def __getitem__(self, i):
        element = Element(self.locator[0], self.locator[1], i)
        element.driver = self.driver
        return element

    def __iter__(self):
        return iter(self.elements)
