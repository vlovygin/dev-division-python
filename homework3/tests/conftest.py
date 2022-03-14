import pytest
from dataclasses import dataclass


@dataclass
class User:
    """Class for user"""
    login: str
    password: str


@pytest.fixture(scope="session")
def test_user() -> User:
    """Exists test user at https://target.my.com/"""
    return User("lovigin@mail.ru", "5@mkfQTkZG8rGbw")
