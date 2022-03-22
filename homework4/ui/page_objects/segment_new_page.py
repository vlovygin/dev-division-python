import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from ui.exceptions import PageNotLoadError
from ui.page_elements import Element
from ui.page_objects.base_page import BasePage


class SegmentNewPage(BasePage):
    path = "/segments/segments_list/new"

    _segment_source_checkbox = Element(By.CSS_SELECTOR, "input[class^=adding-segments-source]")
    _add_segment_button = Element(By.CSS_SELECTOR, "div[class^=adding-segments-modal] button[data-class-name=Submit]")
    _new_segment_name = Element(By.CSS_SELECTOR, "div[class*=input_create-segment-form] input")
    _create_segment_btn = Element(By.CSS_SELECTOR, "div[class^=create-segment-form] button[data-class-name=Submit]")

    @allure.step("Check that segments list page has loaded")
    def is_page_loaded(self):
        try:
            self.common.wait_spinner_miss()
            self.wait().until(lambda d: self.path in d.current_url)
            return True
        except TimeoutException:
            raise PageNotLoadError("Segments list page has not loaded")

    @allure.step("Create a new segment")
    def create_new_segment(self, name):
        self._segment_source_checkbox.click()
        self._add_segment_button.click()
        self._new_segment_name.send_keys(name)
        self._create_segment_btn.click()

        from ui.page_objects.segments_list_page import SegmentsListPage
        return SegmentsListPage(self.driver)
