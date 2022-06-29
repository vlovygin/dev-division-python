import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from main.ui.pages.base_page import BasePage


class RegPageLocators:
    HEADER_TEXT = (By.CSS_SELECTOR, "h3[class*=card-title]")
    NAME_INPUT = (By.CSS_SELECTOR, "#user_name")
    SURNAME_INPUT = (By.CSS_SELECTOR, "#user_surname")
    MIDDLE_NAME_INPUT = (By.CSS_SELECTOR, "#user_middle_name")
    USERNAME_INPUT = (By.CSS_SELECTOR, "#username")
    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "#confirm")
    ACCEPT_CHECKBOX = (By.CSS_SELECTOR, "#term")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "#submit")
    HINT_TEXT = (By.CSS_SELECTOR, "#flash")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")


class RegPage(BasePage):
    path = "/reg"

    locators = RegPageLocators

    def is_page_loaded(self, timeout=None) -> bool:
        try:
            return self.wait_text(self.locators.HEADER_TEXT) == "Registration"
        except TimeoutException:
            return False

    @allure.step
    def register_user(self, name, surname, middle_name, username, email, password, confirm_password):
        self.send_keys(self.locators.NAME_INPUT, name)
        self.send_keys(self.locators.SURNAME_INPUT, surname)
        self.send_keys(self.locators.MIDDLE_NAME_INPUT, middle_name)
        self.send_keys(self.locators.USERNAME_INPUT, username)
        self.send_keys(self.locators.EMAIL_INPUT, email)
        self.send_keys(self.locators.PASSWORD_INPUT, password)
        self.send_keys(self.locators.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.click(self.locators.ACCEPT_CHECKBOX)
        self.click(self.locators.REGISTER_BUTTON)

        from main.ui.pages.main_page import MainPage
        return MainPage(self.driver)

    @allure.step
    def get_name_attribute(self, attribute):
        return self.find(self.locators.NAME_INPUT).get_attribute(attribute)

    @allure.step
    def get_surname_attribute(self, attribute):
        return self.find(self.locators.SURNAME_INPUT).get_attribute(attribute)

    @allure.step
    def get_middle_name_attribute(self, attribute):
        return self.find(self.locators.MIDDLE_NAME_INPUT).get_attribute(attribute)

    @allure.step
    def get_username_attribute(self, attribute):
        return self.find(self.locators.USERNAME_INPUT).get_attribute(attribute)

    @allure.step
    def get_email_attribute(self, attribute):
        return self.find(self.locators.EMAIL_INPUT).get_attribute(attribute)

    @allure.step
    def get_password_attribute(self, attribute):
        return self.find(self.locators.PASSWORD_INPUT).get_attribute(attribute)

    @allure.step
    def get_confirm_password_attribute(self, attribute):
        return self.find(self.locators.ACCEPT_CHECKBOX).get_attribute(attribute)

    @allure.step
    def get_accept_checkbox_attribute(self, attribute):
        return self.find(self.locators.CONFIRM_PASSWORD_INPUT).get_attribute(attribute)

    @allure.step
    def get_hint_text(self) -> str:
        return self.wait_text(self.locators.HINT_TEXT, 10)

    @allure.step
    def navigate_to_login(self):
        self.click(self.locators.LOGIN_LINK)

        from main.ui.pages.login_page import LoginPage
        return LoginPage(self.driver)
