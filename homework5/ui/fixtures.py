from datetime import datetime
from urllib3.exceptions import MaxRetryError

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class Browsers:
    CHROME = "chrome"
    FIREFOX = "firefox"


@pytest.fixture()
def driver(app_config, tmp_path, logger, request):
    """Browser driver"""

    logger.info("Start initializing browser driver")
    driver = None
    selenoid = app_config["selenoid"]
    download_dir = str(tmp_path)

    match browser := app_config["browser"]:
        case Browsers.CHROME:

            options = webdriver.ChromeOptions()
            options.add_experimental_option("prefs", {"download.default_directory": download_dir})

            if not selenoid:
                service = ChromeService(ChromeDriverManager(log_level=0).install())
                driver = webdriver.Chrome(service=service, options=options)

            logger.info(f'Browser driver is ChromeDriver {options.to_capabilities()}')

        case Browsers.FIREFOX:
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
            logger.info(f"Test executes at Selenoid node {executor}")
        except MaxRetryError as e:
            logger.critical(f"Cant connect to Selenoid node {executor} - {e}")
            raise e

    driver.maximize_window()

    failed_tests_cnt = request.session.testsfailed
    yield driver

    if request.session.testsfailed > failed_tests_cnt:
        allure.attach(driver.get_screenshot_as_png(), 'failure.png', attachment_type=allure.attachment_type.PNG)

        if request.config.getoption("--browser") not in Browsers.FIREFOX:  # get_log doesnt work at firefox
            browser_log = tmp_path.joinpath("browser.log")
            with open(browser_log, 'w+') as log_file:

                for entry in driver.get_log('browser'):
                    timestamp = datetime.fromtimestamp(entry["timestamp"] / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')
                    log_file.write(f'{entry["level"]: <8} {timestamp} [{entry["source"]}] {entry["message"]}\n')

                log_file.seek(0)
                allure.attach(log_file.read(), "browser.log", attachment_type=allure.attachment_type.TEXT)

    driver.quit()
