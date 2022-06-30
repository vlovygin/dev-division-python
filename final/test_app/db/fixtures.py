import pytest

from db.client import DbClient


@pytest.fixture(scope="session")
def db_client(app_config):
    """ MySQL client fixture """

    client = DbClient(**app_config["mysql"])

    yield client
    client.session.close()
    client.engine.dispose()
