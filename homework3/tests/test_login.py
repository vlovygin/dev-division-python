import random
import string

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.UI
class TestUserPage:

    @pytest.fixture(autouse=True)
    def login_by_user(self, driver, test_user):
        """Login by exists user"""

        wait = WebDriverWait(driver, 15)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class*=rightSide] > div[class^=responseHead-module-button]"))
        driver.find_element(By.CSS_SELECTOR, "div[class*=rightSide] > div[class^=responseHead-module-button]").click()

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=email]"))
        driver.find_element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=email]").clear()
        driver.find_element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=email]").send_keys(test_user.login)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class*=rightSide] > div[class^=responseHead-module-button]"))
        driver.find_element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=password]").clear()
        driver.find_element(By.CSS_SELECTOR, "div[class*=authForm] > input[name=password]").send_keys(test_user.password)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class^=authForm-module-actions] > div[class*=authForm-module-button]"))
        driver.find_element(By.CSS_SELECTOR, "div[class^=authForm-module-actions] > div[class*=authForm-module-button]").click()

        wait.until_not(lambda d: d.find_element(By.CSS_SELECTOR, ".spinner"))

    def test_login(self, driver):
        """User logged in to private office"""

        wait = WebDriverWait(driver, 15)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class*=right-module-mail] > div[class^=right-module-userNameWrap]"))
        profile_name = driver.find_element(By.CSS_SELECTOR, "div[class*=right-module-mail] > div[class^=right-module-userNameWrap]").text

        assert profile_name, "Profile name must be displayed at private office"
        assert driver.get_cookie('mc'), "'mc' cookie must be set for authenticated user"

    def test_logout(self, driver):
        """User logout from private office"""

        wait = WebDriverWait(driver, 15)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class*=right-module-mail]"))
        driver.find_element(By.CSS_SELECTOR, "div[class*=right-module-mail]").click()

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "ul[class*=visibleRightMenu] a[href='/logout']").location["y"] > 60)
        driver.find_element(By.CSS_SELECTOR, "ul[class*=visibleRightMenu] a[href='/logout']").click()

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "div[class*=rightSide] > div[class^=responseHead-module-button]"))
        entry_btn_text = driver.find_element(By.CSS_SELECTOR, "div[class*=rightSide] > div[class^=responseHead-module-button]").text

        assert entry_btn_text == "Войти", "Entry button must be displayed after logout"
        assert not driver.get_cookie('mc'), "'mc' cookie must be deleted for not authenticated user"

    def test_edit_profile(self, driver):
        """Edit profile Full name"""

        wait = WebDriverWait(driver, 15)
        new_full_name = "".join([random.choice(string.ascii_letters) for _ in range(10)])

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "ul[class^=center-module-buttons] a[href='/profile']"))
        driver.find_element(By.CSS_SELECTOR, "ul[class^=center-module-buttons] a[href='/profile']").click()

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, ".input[data-name=fio] input"))
        driver.find_element(By.CSS_SELECTOR, ".input[data-name=fio] input").clear()
        driver.find_element(By.CSS_SELECTOR, ".input[data-name=fio] input").send_keys(new_full_name)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "button.button_submit"))
        driver.find_element(By.CSS_SELECTOR, "button.button_submit").click()

        driver.refresh()

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, ".input[data-name=fio] input"))
        current_full_name = driver.find_element(By.CSS_SELECTOR, ".input[data-name=fio] input").get_attribute("value")

        assert current_full_name == new_full_name, "User full name not updated"

    @pytest.mark.parametrize("href, path", [
        ("/segments", "/segments/segments_list"),
        ("/billing", "/billing#deposit")
    ])
    def test_menu_sections(self, driver, href, path, base_url):
        """Open sections at header menu"""

        wait = WebDriverWait(driver, 15)

        wait.until(lambda d: d.find_element(By.CSS_SELECTOR, f"ul[class^=center-module-buttons] a[href='{href}']"))
        driver.find_element(By.CSS_SELECTOR, f"ul[class^=center-module-buttons] a[href='{href}']").click()

        wait.until_not(lambda d: d.find_element(By.CSS_SELECTOR, ".spinner"))

        assert driver.current_url == f"{base_url}{path}", f"Expected url is {base_url}{path}, but given {driver.current_url}"
