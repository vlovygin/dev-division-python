import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from ui.exceptions import PageNotLoadError
from ui.page_elements import Element
from ui.page_objects.base_page import BasePage


class CampaignNewPage(BasePage):
    path = "/campaign/new"

    _new_campaign_form = Element(By.CSS_SELECTOR, "div[data-class-name=Campaign]")
    _reach_objective = Element(By.CSS_SELECTOR, "div[class*=objectives] div[class*=reach]")
    _objective_url = Element(By.CSS_SELECTOR, "input[class*=mainUrl]")
    _campaign_name = Element(By.CSS_SELECTOR, "div.campaign-name input")
    _adv_format_teaser = Element(By.CSS_SELECTOR, "[data-id^=patterns_teaser]")
    _adv_title = Element(By.CSS_SELECTOR, "input[data-name^=title]")
    _adv_text = Element(By.CSS_SELECTOR, "textarea[data-name^=text]")
    _upload_input = Element(By.CSS_SELECTOR, "[class^=roles-module-buttonWrap] input[type=file]")
    _load_pending = Element(By.CSS_SELECTOR, "div[class*=button-module-pending]")
    _save_image = Element(By.CSS_SELECTOR, "div[class^=image] input[class*=save]")
    _budget_per_date = Element(By.CSS_SELECTOR, "input[data-test=budget-per_day]")
    _budget_total = Element(By.CSS_SELECTOR, "input[data-test=budget-total]")
    _submit_create_campaign = Element(By.CSS_SELECTOR, "div[class*=save] button[data-class-name=Submit]")

    @allure.step("Check that campaign new page has loaded")
    def is_page_loaded(self):
        try:
            self.common.wait_spinner_miss()
            self._new_campaign_form.wait_until_visible()
            return True
        except TimeoutException:
            raise PageNotLoadError("Campaign new page has not loaded")

    @allure.step("Create reach campaign")
    def create_reach_campaign(self, name, image_path):
        self._reach_objective.click()
        self._objective_url.send_keys("https://www.python.org/")
        self._campaign_name.send_keys(name)
        self._budget_per_date.send_keys("1000")
        self._budget_total.send_keys("10000")
        self._adv_format_teaser.click()
        self._adv_title.send_keys("Advert title")
        self._adv_text.send_keys("Advert text")
        self._upload_input.upload_file(image_path)
        self._save_image.click()
        self._load_pending.wait_until_not_visible()
        self._submit_create_campaign.click()

        from ui.page_objects.dashbord_page import DashboardPage
        return DashboardPage(self.driver)
