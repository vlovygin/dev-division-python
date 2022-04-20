import allure
from ui.page_objects import BasePage
from selenium.webdriver.common.by import By


class MainPageLocators:
    ENTRY_BTN = (By.CSS_SELECTOR, "div[class*=rightSide] div[class*=button]")
    LOGIN_INPUT = (By.CSS_SELECTOR, "div[class*=authForm] > input[name=email]")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "div[class*=authForm] > input[name=password]")
    SUBMIT_LOGIN_BTN = (By.CSS_SELECTOR, "div[class^=authForm] > div[class*=button]")
    SUBMIT_LOGIN_BTN_DISABLED = (By.CSS_SELECTOR, "div[class^=authForm] > div[class*=button][class*=disabled]")



class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step
    def login(self, login, password):
        self.click(self.locators.ENTRY_BTN)
        self.send_keys(self.locators.LOGIN_INPUT, login)
        self.send_keys(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.SUBMIT_LOGIN_BTN)

        from ui.page_objects import DashboardPage
        return DashboardPage(self.driver)

    @allure.step
    def is_submit_login_button_disabled(self):
        return self.find(self.locators.SUBMIT_LOGIN_BTN_DISABLED)
