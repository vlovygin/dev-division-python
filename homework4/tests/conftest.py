from enum import Enum

import requests
import pytest
from dataclasses import dataclass
from utils.fake import fake


@dataclass
class User:
    """Class for user"""
    login: str
    password: str


@pytest.fixture(scope="session")
def user():
    return User("lovigin@mail.ru", "5@mkfQTkZG8rGbw")


@pytest.fixture(scope='session')
def auth_cookies(config, user):
    url = config["auth_url"]
    data = {"email": user.login, "password": user.password}
    headers = {"Referer": config["base_url"]}

    response = requests.post(url, data=data, headers=headers, allow_redirects=False)

    if not response.ok:
        pytest.fail(f'Authorization failed with [{response.status_code}]: {response.text}')

    return response.cookies


class DataTestType(Enum):
    CORRECT = 0
    INVALID = 1
    EMPTY = 2
    SPACE = 3


@pytest.fixture(params=[
    ("invalid login", DataTestType.INVALID, DataTestType.CORRECT),
    ("incorrect password", DataTestType.CORRECT, DataTestType.INVALID),
    ("space login", DataTestType.SPACE, DataTestType.CORRECT),
    ("space password", DataTestType.CORRECT, DataTestType.SPACE)
    # etc..
], ids=lambda x: x[0])
def negative_user(request, user):
    login, password = request.param[1:]

    match login:
        case DataTestType.CORRECT:
            login = user.login
        case DataTestType.INVALID:
            login = fake.email()
        case DataTestType.EMPTY:
            login = ""
        case DataTestType.SPACE:
            login = " "

    match password:
        case DataTestType.CORRECT:
            password = user.password
        case DataTestType.INVALID:
            password = fake.password()
        case DataTestType.EMPTY:
            password = ""
        case DataTestType.SPACE:
            password = " "

    return User(login, password)
