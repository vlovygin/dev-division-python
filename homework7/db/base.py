import pytest

from db.client import MysqlORMClient


class MysqlBase:

    # is called from setup fixture on every test. test can override this method for its custom data prepare
    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.mysql: MysqlORMClient = mysql_orm_client
        self.prepare()
