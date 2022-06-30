import logging

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from main.db.models import TestUsers
from main.models.user import User

logger = logging.getLogger("test")


class DbClient:
    """ Database client """

    def __init__(self, *, drivername, username, password, host, port, database, query, echo=False):
        connection_url = URL.create(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            query=query
        )

        self.engine = create_engine(connection_url, echo=echo)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def execute_query(self, query, fetch=True):
        res = self.session.execute(query)
        if fetch:
            return res.fetchall()

    def add_user(self, user: User) -> TestUsers:
        """ Add user in db """

        test_user = TestUsers(**user.to_dict())
        self.session.add(test_user)
        self.session.commit()
        logger.info(f"Created new user {test_user}")

        return test_user

    def get_user(self, username):
        """ Get user from test_users """
        return self.session.query(TestUsers).filter(TestUsers.username == username).one_or_none()
