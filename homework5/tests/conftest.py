import pytest
from models.user import User


@pytest.fixture(scope="session")
def user():
    return User("torag86369@3dinews.com", "A_LCbL^xf5b@-AQ")
