import allure
from selenium.webdriver.common.by import By
from ui.page_objects import BasePage


class SegmentsListPageLocators:
    SEARCH_INPUT = (By.CSS_SELECTOR, "div[class*=segmentsTable] input[class*=searchInput]")
    SEARCH_PREVIEW_RESULTS = (By.CSS_SELECTOR, "ul[class*=optionsList] li")
    SEARCH_RESULT_HORIZONTAL_SCROLL = (By.CSS_SELECTOR, "div[class*=horizontal] div[class^=custom-scroll]")
    DELETE_SEGMENT_BTN = (By.CSS_SELECTOR, "span[class*=removeCell]")
    CONFIRM_DELETE_BTN = (By.CSS_SELECTOR, "button[class~=button_confirm-remove]")
    SEGMENTS_LIST = (By.CSS_SELECTOR, "div[data-class-name=SegmentsList]")
    SEGMENTS_LINKS = (By.CSS_SELECTOR, "div[class*=name] a[href^='/segments/segments_list/']")


class SegmentsListPage(BasePage):
    path = "/segments/segments_list"

    locators = SegmentsListPageLocators()

    @allure.step
    def search_segment(self, text):
        self.send_keys(self.locators.SEARCH_INPUT, text)
        self.click(self.locators.SEARCH_PREVIEW_RESULTS)

    @allure.step
    def delete_segment(self):
        horizontal_scroll_el = self.find(self.locators.SEARCH_RESULT_HORIZONTAL_SCROLL)

        self.action_chain().drag_and_drop_by_offset(horizontal_scroll_el, 100, 0).perform()
        self.click(self.locators.DELETE_SEGMENT_BTN)
        self.click(self.locators.CONFIRM_DELETE_BTN)
        self.wait_miss(self.locators.CONFIRM_DELETE_BTN)

    @allure.step
    def get_segments_list(self, timeout=None):
        segments = self.finds(self.locators.SEGMENTS_LINKS, timeout=timeout)
        return [segment.text for segment in segments]
