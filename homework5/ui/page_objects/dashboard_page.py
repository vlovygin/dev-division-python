import allure
from selenium.webdriver.common.by import By
from ui.page_objects import BasePage


class DashboardPageLocators:
    SEARCH_INPUT = (By.CSS_SELECTOR, "div[class^=dashboard] input[class*=searchInput]")
    SEARCH_PREVIEW_RESULTS = (By.CSS_SELECTOR, "ul[class*=optionsList] li")
    CAMPAIGNS_LIST = (By.CSS_SELECTOR, "a[class*=campaignNameLink]")


class DashboardPage(BasePage):
    path = "/dashboard"

    locators = DashboardPageLocators()

    @allure.step
    def search_campaign(self, text):
        self.send_keys(self.locators.SEARCH_INPUT, text)
        self.click(self.locators.SEARCH_PREVIEW_RESULTS)

    @allure.step
    def get_campaigns_list(self):
        campaigns = self.finds(self.locators.CAMPAIGNS_LIST)
        return [campaign.text for campaign in campaigns]
