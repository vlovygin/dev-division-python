from urllib3.exceptions import MaxRetryError

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.config import Config


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome", help="Browser type")
    parser.addoption("--selenoid", action="store_true", help="Remote web driver")
    parser.addoption("--selenoid-vnc", action="store_true", help="Enable selenoid VNC")
    parser.addoption("--selenoid-video", action="store_true", help="Enable selenoid video")


@pytest.fixture(scope="session")
def config(request):
    _config = Config()
    _config["base_url"] = _config["base_url"]
    _config["browser"] = request.config.getoption("--browser")

    if request.config.getoption("--selenoid"):
        _config["selenoid"]["host"] = _config["selenoid"]["host"]
        _config["selenoid"]["port"] = _config["selenoid"]["port"]
        _config["selenoid"]["vnc"] = request.config.getoption("--selenoid-vnc")
        _config["selenoid"]["video"] = request.config.getoption("--selenoid-video")
    else:
        _config["selenoid"] = None

    return _config


@pytest.fixture()
def driver(config, tmp_path, logger):
    """Browser driver initializing"""

    logger.info("Start initializing browser driver")
    driver = None
    selenoid = config["selenoid"]
    download_dir = str(tmp_path)

    match browser := config["browser"]:
        case "chrome":

            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})

            if not selenoid:
                service = ChromeService(ChromeDriverManager(log_level=0).install())
                driver = webdriver.Chrome(service=service, options=options)

            logger.info(f'Browser driver is ChromeDriver {options.to_capabilities()}')

        case "firefox":
            mime_types = "application/csv, text/csv, text/plain, application/octet-stream, doc, xls, pdf, txt"

            options = webdriver.FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.download.dir", download_dir)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)

            if not selenoid:
                service = FirefoxService(GeckoDriverManager(log_level=0).install())
                driver = webdriver.Firefox(service=service, options=options)

            logger.info(f'Browser driver is GeckoDriver {options.to_capabilities()}')

        case _:
            logger.critical(f"Browser driver {browser} not supported")
            raise NotImplementedError

    if selenoid:
        executor = f'{selenoid["host"]}:{selenoid["port"]}'
        options.capabilities["enableVNC"] = selenoid["vnc"]
        options.capabilities["enableVideo"] = selenoid["video"]
        options.capabilities["sessionTimeout"] = selenoid["session_timeout"]

        try:
            driver = webdriver.Remote(f'http://{executor}/wd/hub', options=options)
            logger.info(f'Test executes at Selenoid node {executor}')
        except MaxRetryError as e:
            logger.critical(f'Cant connect to Selenoid node {executor} - {e}')
            raise e

    driver.maximize_window()
    yield driver

    driver.quit()
