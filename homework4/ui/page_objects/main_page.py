import allure

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from ui.exceptions import PageNotLoadError
from ui.page_elements import Element
from ui.page_objects.base_page import BasePage
from ui.page_objects.dashbord_page import DashboardPage


class MainPage(BasePage):
    path = "/"

    _entry_btn = Element(By.CSS_SELECTOR, "div[class*=rightSide] > div[class^=responseHead-module-button]")
    _login_input = Element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=email]")
    _password_input = Element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=password]")
    _submit_login_btn = Element(By.CSS_SELECTOR,
                                "div[class^=authForm-module-actions] > div[class*=authForm-module-button]")

    @allure.step("Login by user")
    def login(self, user, password):
        self._entry_btn.click()
        self._login_input.send_keys(user)
        self._password_input.send_keys(password)
        self._submit_login_btn.click()
        return DashboardPage(self.driver)

    @allure.step("Check main page has loaded")
    def is_page_loaded(self):
        try:
            self.common.wait_spinner_miss()
            return True
        except TimeoutException:
            raise PageNotLoadError("Dashboard page has not loaded")
