import allure
from selenium.webdriver.common.by import By

from ui.page_elements import Element


class Common():
    _spinner = Element(By.CSS_SELECTOR, ".spinner")

    def __init__(self, driver):
        self.driver = driver

    @allure.step("Wait until spinner is loaded")
    def wait_spinner_miss(self):
        self._spinner.wait_until_not_visible()
