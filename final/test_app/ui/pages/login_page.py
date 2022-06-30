import allure
from selenium.common import TimeoutException

from selenium.webdriver.common.by import By

from ui.pages.base_page import BasePage


class LoginPageLocators:
    HEADER_TEXT = (By.CSS_SELECTOR, "h3[class*=card-title]")
    USERNAME_INPUT = (By.CSS_SELECTOR, "#username")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    SUBMIT_LOGIN_BTN = (By.CSS_SELECTOR, "#submit")
    HINT_TEXT = (By.CSS_SELECTOR, "#flash")
    REG_LINK = (By.CSS_SELECTOR, "a[href='/reg']")


class LoginPage(BasePage):
    path = "/login"

    locators = LoginPageLocators

    def is_page_loaded(self, timeout=None) -> bool:
        try:
            return self.wait_text(self.locators.HEADER_TEXT) == "Welcome to the TEST SERVER"
        except TimeoutException:
            return False

    @allure.step
    def login(self, username, password):
        self.send_keys(self.locators.USERNAME_INPUT, username)
        self.send_keys(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.SUBMIT_LOGIN_BTN)

        from ui.pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step
    def get_hint_text(self) -> str:
        return self.wait_text(self.locators.HINT_TEXT, 10)

    @allure.step
    def get_username_attribute(self, attribute):
        return self.find(self.locators.USERNAME_INPUT).get_attribute(attribute)

    @allure.step
    def get_password_attribute(self, attribute):
        return self.find(self.locators.PASSWORD_INPUT).get_attribute(attribute)

    @allure.step
    def navigate_to_reg_page(self):
        self.click(self.locators.REG_LINK)

        from ui.pages.reg_page import RegPage
        return RegPage(self.driver)
