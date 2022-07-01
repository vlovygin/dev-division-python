import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage


class MainPageLocators:
    LOGIN_CONTROLS = (By.CSS_SELECTOR, "#login-controls")

    BRAND_LINK = (By.CSS_SELECTOR, "a[class*=uk-navbar-brand]")

    PYTHON_LINK = (By.XPATH, "//a[text()='Python']")
    PYTHON_HISTORY_LINK = (By.XPATH, "//a[text()='Python history']")
    ABOUT_FLASK_LINK = (By.XPATH, "//a[text()='About Flask']")

    LINUX_LINK = (By.XPATH, "//a[text()='Linux']")
    DOWNLOAD_CENTOS_LINK = (By.XPATH, "//a[text()='Download Centos7']")

    NETWORK_LINK = (By.XPATH, "//a[text()='Network']")
    NEWS_LINK = (By.XPATH, "//a[text()='News']")
    DOWNLOAD_LINK = (By.XPATH, "//a[text()='Download']")
    EXAMPLES_LINK = (By.XPATH, "//a[text()='Examples ']")

    WHAT_IS_API_LINK = (By.XPATH, "//div[text()='What is an API?']/..//a")
    FUTURE_INTERNET_LINK = (By.XPATH, "//div[text()='Future of internet']/..//a")
    SMTP_LINK = (By.XPATH, "//div[text()='Lets talk about SMTP?']/..//a")

    LOGGED_AS_TEXT = (By.CSS_SELECTOR, "#login-name li:nth-child(1)")
    USER_INFO_TEXT = (By.CSS_SELECTOR, "#login-name li:nth-child(2)")
    VK_ID = (By.CSS_SELECTOR, "#login-name li:nth-child(3)")

    FACT_TEXT = (By.CSS_SELECTOR, "footer p:nth-child(1)")

    LOGOUT = (By.CSS_SELECTOR, "#logout a[href='/logout']")


class MainPage(BasePage):
    path = "/welcome"

    locators = MainPageLocators

    def is_page_loaded(self, timeout=None) -> bool:
        try:
            self.find(self.locators.LOGIN_CONTROLS)
            return True
        except TimeoutException:
            return False

    @allure.step
    def logout(self):
        self.click(self.locators.LOGOUT)

        from ui.pages.login_page import LoginPage
        return LoginPage(self.driver)

    @allure.step
    def navigate_to_brand(self):
        ele = self.find(self.locators.BRAND_LINK)
        self.click(self.locators.BRAND_LINK)
        self.wait_stale(ele)

        return MainPage(self.driver)

    @allure.step
    def navigate_to_home(self):
        ele = self.find(self.locators.BRAND_LINK)
        self.click(self.locators.BRAND_LINK)
        self.wait_stale(ele)

        return MainPage(self.driver)

    @allure.step
    def navigate_to_python(self):
        self.click(self.locators.PYTHON_LINK)

        return BasePage(self.driver)

    def move_and_click(self, move_to_element, click_to_element):
        self.action_chain().move_to_element(move_to_element).click(click_to_element).perform()

    @allure.step
    def navigate_to_python_python_history(self):
        self.move_and_click(move_to_element=self.find(self.locators.PYTHON_LINK),
                            click_to_element=self.find(self.locators.PYTHON_HISTORY_LINK))

        return BasePage(self.driver)

    @allure.step
    def navigate_to_linux_about_flask(self):
        self.move_and_click(move_to_element=self.find(self.locators.PYTHON_LINK),
                            click_to_element=self.find(self.locators.ABOUT_FLASK_LINK))
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_linux_download_centos_7(self):
        self.move_and_click(move_to_element=self.find(self.locators.LINUX_LINK),
                            click_to_element=self.find(self.locators.DOWNLOAD_CENTOS_LINK))
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_network_news(self):
        self.move_and_click(move_to_element=self.find(self.locators.NETWORK_LINK),
                            click_to_element=self.find(self.locators.NEWS_LINK))
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_network_download(self):
        self.move_and_click(move_to_element=self.find(self.locators.NETWORK_LINK),
                            click_to_element=self.find(self.locators.DOWNLOAD_LINK))
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_network_examples(self):
        self.move_and_click(move_to_element=self.find(self.locators.NETWORK_LINK),
                            click_to_element=self.find(self.locators.EXAMPLES_LINK))
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_what_is_api(self):
        self.click(self.locators.WHAT_IS_API_LINK)
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_future_internet(self):
        self.click(self.locators.FUTURE_INTERNET_LINK)
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def navigate_to_smtp(self):
        self.click(self.locators.SMTP_LINK)
        self.switch_to_new_window()

        return BasePage(self.driver)

    @allure.step
    def get_logged_as_info(self):
        text = self.find(self.locators.LOGGED_AS_TEXT).text
        return text.removeprefix("Logged as ")

    @allure.step
    def get_logged_as_info(self):
        text = self.find(self.locators.LOGGED_AS_TEXT).text
        return text.removeprefix("Logged as ")

    @allure.step
    def get_user_info(self):
        text = self.find(self.locators.USER_INFO_TEXT).text
        return text.removeprefix("User: ")

    @allure.step
    def get_fact_text(self):
        return self.find(self.locators.FACT_TEXT).text

    @allure.step
    def get_vk_id(self):
        text = self.find(self.locators.VK_ID).text
        return text.removeprefix("VK ID: ")

    @allure.step
    def is_vk_id_info_visible(self):
        try:
            self.find(self.locators.VK_ID, timeout=2)
            return True
        except TimeoutException:
            return False
