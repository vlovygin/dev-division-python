import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from ui.exceptions import PageNotLoadError
from ui.page_elements import Element, Elements
from ui.page_objects.base_page import BasePage
from ui.page_objects.campaign_new_page import CampaignNewPage


class DashboardPage(BasePage):
    path = "/dashboard"

    _get_started_instruction = Element(By.CSS_SELECTOR, "div[class^=instruction-module-container]")
    _create_campaign_btn = Element(By.CSS_SELECTOR, "div[class*=createButton] div[data-test=button]")
    _new_campaign_link = Element(By.CSS_SELECTOR, "li[class^='instruction-module-item'] > a[href='/campaign/new']")
    _search_input = Element(By.CSS_SELECTOR, "input[class*=searchInput]")
    _search_result_preview = Elements(By.CSS_SELECTOR, "ul[class*=optionsList] li")
    _campaigns_list = Elements(By.CSS_SELECTOR, "a[class*=campaignNameLink]")
    _success_notification = Element(By.CSS_SELECTOR, "div[class*=notify-module-success]")

    @allure.step("Check that dashboard page has loaded")
    def is_page_loaded(self):
        try:
            self.common.wait_spinner_miss()
            self.wait().until(lambda d: self.path in d.current_url)
            return True
        except TimeoutException:
            raise PageNotLoadError("Dashboard page has not loaded")

    @allure.step("Navigate to new campaign create")
    def navigate_to_new_campaign_create(self):
        if self._create_campaign_btn.is_visible():
            self._create_campaign_btn.click()
        else:
            self._new_campaign_link.click()

        return CampaignNewPage(self.driver)

    @property
    @allure.step("Get success message notification")
    def success_notification_text(self):
        return self._success_notification.get_attribute("innerText")

    @allure.step("Search campaign by name")
    def search_campaign(self, name):
        self._search_input.send_keys(name)
        self._search_result_preview[0].wait_until_visible()
        self._search_result_preview[0].click()
        return self

    @property
    @allure.step("Get campaigns name")
    def campaigns_name_list(self):
        self._campaigns_list[0].wait_until_visible()
        return [campaign.text for campaign in self._campaigns_list]
