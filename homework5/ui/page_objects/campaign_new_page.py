import allure
from selenium.webdriver.common.by import By

from models.campaign import CampaignObjective, CampaignAdvFormat
from ui.page_objects import BasePage


class CampaignNewPageLocators:
    REACH_OBJECTIVE = (By.CSS_SELECTOR, "div[class*=objectives] div[class*=reach]")
    OBJECTIVE_URL_INPUT = (By.CSS_SELECTOR, "input[class*=mainUrl]")
    CAMPAIGN_NAME_INPUT = (By.CSS_SELECTOR, "div.campaign-name input")
    BUDGET_PER_DATE_INPUT = (By.CSS_SELECTOR, "input[data-test=budget-per_day]")
    BUDGET_TOTAL_INPUT = (By.CSS_SELECTOR, "input[data-test=budget-total]")
    TEASER_ADV_FORMAT = (By.CSS_SELECTOR, "[data-id^=patterns_teaser]")
    ADV_TITLE = (By.CSS_SELECTOR, "input[data-name^=title]")
    ADV_TEXT = (By.CSS_SELECTOR, "textarea[data-name^=text]")
    BANNER_IMAGE_INPUT = (By.CSS_SELECTOR, "div[class^=bannerForm] [class^=upload-module] input[type=file]")
    BANNER_SAVE_IMAGE = (By.CSS_SELECTOR, "div[class^=image] input[class*=save]")
    SUBMIT_CREATE_CAMPAIGN = (By.CSS_SELECTOR, "div[class*=save] button[data-class-name=Submit]")


class CampaignNewPage(BasePage):
    path = "/campaign/new"

    locators = CampaignNewPageLocators()

    @allure.step
    def select_campaign_objective(self, objective):
        match objective:
            case CampaignObjective.REACH:
                self.click(self.locators.REACH_OBJECTIVE)
            case _:
                raise NotImplementedError()

    @allure.step
    def set_objective_url(self, url):
        self.send_keys(self.locators.OBJECTIVE_URL_INPUT, url)

    @allure.step
    def set_campaign_name(self, name):
        self.send_keys(self.locators.CAMPAIGN_NAME_INPUT, name)

    @allure.step
    def set_budget_per_date(self, budget):
        self.send_keys(self.locators.BUDGET_PER_DATE_INPUT, budget)

    @allure.step
    def set_budget_total(self, budget):
        self.send_keys(self.locators.BUDGET_TOTAL_INPUT, budget)

    @allure.step
    def select_adv_format(self, format):
        match format:
            case CampaignAdvFormat.TEASER:
                self.click(self.locators.TEASER_ADV_FORMAT)
            case _:
                raise NotImplementedError()

    @allure.step
    def set_adv_title(self, title):
        self.send_keys(self.locators.ADV_TITLE, title)

    @allure.step
    def set_adv_text(self, text):
        self.send_keys(self.locators.ADV_TEXT, text)

    @allure.step
    def upload_adv_image(self, file_path):
        self.upload_file(self.locators.BANNER_IMAGE_INPUT, file_path)
        self.click(self.locators.BANNER_SAVE_IMAGE)

    @allure.step
    def submit_create_campaign(self):
        self.click(self.locators.SUBMIT_CREATE_CAMPAIGN)

        from ui.page_objects import DashboardPage
        return DashboardPage(self.driver)
