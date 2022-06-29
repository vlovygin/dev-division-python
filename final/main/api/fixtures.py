import pytest

from main.api.client import MyAppApiClient, VkMockClient
from main.utils.data_manager import DataManager


@pytest.fixture(scope="session")
def myapp_api_not_auth_client(app_config):
    """ MyApp API not auth client fixture """

    client = MyAppApiClient(base_url=app_config["base_url"])

    return client


@pytest.fixture(scope="session")
def myapp_api_client(app_config, db_client, data_manager: DataManager):
    """ MyApp API client fixture """

    client = MyAppApiClient(base_url=app_config["base_url"])

    # add api user to DB
    user = data_manager.user(name="api", surname="client")
    client.api_user = user  # add api_user attribute for test purpose
    db_client.add_user(user)

    # log in by created user
    login = client.login(user.username, user.password)
    login.raise_for_status()

    return client


@pytest.fixture(scope="session")
def vk_mock_client(app_config):
    """ VK mock client """
    client = VkMockClient(base_url=app_config["vk_mock"])
    return client
