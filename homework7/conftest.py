import pytest

from db.client import MysqlORMClient
from utils import PROJECT_PATH


def pytest_configure(config):
    mysql_orm_client = MysqlORMClient(user='test_user', password='test_password', db_name='HOMEWORK')

    if not hasattr(config, 'workerinput'):
        mysql_orm_client.recreate_db()

    mysql_orm_client.connect(db_created=True)

    if not hasattr(config, 'workerinput'):
        mysql_orm_client.create_all_tables()

        log_file = PROJECT_PATH.joinpath("access.log")
        mysql_orm_client.parse_log(log_file)
        mysql_orm_client.prepare_db()

    config.mysql_orm_client = mysql_orm_client


@pytest.fixture(scope='session')
def mysql_orm_client(request) -> MysqlORMClient:
    client = request.config.mysql_orm_client
    yield client
    client.connection.close()
