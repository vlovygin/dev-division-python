import logging

import allure
import pytest
from _pytest.fixtures import Config

pytest_plugins = [
    "ui.fixtures"
]


def pytest_configure(config: Config):
    if not hasattr(config, 'workerinput'):  # not xdist worker

        # Set temporary base dir for test artifacts (used in tmp_path fixture)
        if not config.option.basetemp:  # not set --basetemp pytest option
            config.option.basetemp = config.rootpath.joinpath(".temp")


@pytest.fixture
def logger(tmp_path, config):
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

    allure.attach.file(log_file, 'debug.log', attachment_type=allure.attachment_type.TEXT)
