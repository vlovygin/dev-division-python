import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from ui.exceptions import PageNotLoadError
from ui.page_elements import Element, Elements
from ui.page_objects.base_page import BasePage
from ui.page_objects.segment_new_page import SegmentNewPage


class SegmentsListPage(BasePage):
    path = "/segments/segments_list"

    _profile_name = Element(By.CSS_SELECTOR, "div[class*=right-module-mail] > div[class^=right-module-userNameWrap]")
    _create_segment_btn = Element(By.CSS_SELECTOR, "button[cid^=view]")
    _new_segment_link = Element(By.CSS_SELECTOR,
                                "li[class^='instruction-module-item'] > a[href='/segments/segments_list/new/']")
    _search_input = Element(By.CSS_SELECTOR, "input[class*=searchInput]")
    _search_result_preview = Elements(By.CSS_SELECTOR, "ul[class*=optionsList] li")
    _segments_list = Elements(By.CSS_SELECTOR, "div[class*=name] a[href^='/segments/segments_list/']")
    _delete_segment_btn = Elements(By.CSS_SELECTOR, "span[class*=removeCell]")
    _confirm_delete_btn = Element(By.CSS_SELECTOR, "button[class~=button_confirm-remove]")

    @allure.step("Check that segments list page has loaded")
    def is_page_loaded(self):
        try:
            self.common.wait_spinner_miss()
            self.wait().until(lambda d: self.path in d.current_url)
            return True
        except TimeoutException:
            raise PageNotLoadError("Segments list page has not loaded")

    @allure.step("Navigate to new campaign create")
    def navigate_to_create_segment(self):
        if self._create_segment_btn.is_visible():
            self._create_segment_btn.click()
        else:
            self._new_segment_link.click()

        return SegmentNewPage(self.driver)

    @allure.step("Search segment by name")
    def search_segment(self, name):
        self._search_input.send_keys(name)
        self._search_result_preview[0].wait_until_visible()
        self._search_result_preview[0].click()
        return self

    @property
    @allure.step("Get segments name")
    def segments_name_list(self):
        return [segment.text for segment in self._segments_list]

    @allure.step("Delete segment in list")
    def delete_segment(self, position: int = 0):
        self._delete_segment_btn[position].click()
        self._confirm_delete_btn.click()
        self._confirm_delete_btn.wait_until_not_visible()
        return
