import logging
from pathlib import Path

import allure
import pytest
from _pytest.fixtures import Config as PytestConfig, FixtureRequest

from config import app_config as app_cfg
from utils import PROJECT_PATH

pytest_plugins = [
    "ui.fixtures",
    "api.fixtures"
]


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome", help="Browser type")
    parser.addoption("--selenoid", action="store_true", help="Remote web driver")
    parser.addoption("--selenoid-vnc", action="store_true", help="Enable selenoid VNC")
    parser.addoption("--selenoid-video", action="store_true", help="Enable selenoid video")


@pytest.fixture(scope="session")
def app_config(request: FixtureRequest):
    """Test application config"""

    _config = app_cfg
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


def pytest_configure(config: PytestConfig):
    if not hasattr(config, 'workerinput'):  # not xdist worker

        # Set temporary base dir for test artifacts (used in tmp_path fixture)
        if not config.option.basetemp:  # not set --basetemp pytest option
            config.option.basetemp = PROJECT_PATH.joinpath(".temp")


@pytest.fixture(scope="session")
def root_path() -> Path:
    """Project root path"""

    return PROJECT_PATH


@pytest.fixture
def logger(tmp_path: Path):
    """Logger for test. Saved at temp file"""

    log_formatter = logging.Formatter(
        fmt="%(levelname)-8s %(asctime)s.%(msecs)03d [%(filename)s:%(lineno)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    log_file = tmp_path.joinpath("test.log")
    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)

    log = logging.getLogger('test')
    log.handlers.clear()
    log.setLevel(log_level)
    log.addHandler(file_handler)
    log.propagate = False

    yield log

    for handler in log.handlers:
        handler.close()

    allure.attach.file(log_file, 'test.log', attachment_type=allure.attachment_type.TEXT)
