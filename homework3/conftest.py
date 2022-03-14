import pytest

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


def pytest_addoption(parser):
    parser.addoption("--base_url", action="store", default="https://target.my.com", help="SUT URL")


@pytest.fixture()
def base_url(request):
    """SUT URL"""

    return request.config.getoption('--base_url')


@pytest.fixture()
def driver(base_url) -> WebDriver:
    """Return a new instance of the chrome driver with open SUT site page"""

    wd = webdriver.Chrome()
    wd.maximize_window()
    wd.get(base_url)

    yield wd
    wd.quit()
