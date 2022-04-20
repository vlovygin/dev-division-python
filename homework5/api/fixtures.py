import pytest

from api.client import ApiClient


@pytest.fixture(scope='session')
def api_client(app_config, user):
    """myTarget API client"""

    client = ApiClient(base_url=app_config["base_url"])
    client.auth(user.login, user.password)

    return client
