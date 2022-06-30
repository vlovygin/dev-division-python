from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestUsers(Base):
    __tablename__ = "test_users"
    __table_args__ = {"mysql_charset": "utf8"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    middle_name = Column(String(255))
    username = Column(String(16))
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(SmallInteger)
    active = Column(SmallInteger)
    start_active_time = Column(DateTime)

    UniqueConstraint("email", name="email")
    UniqueConstraint("username", name="ix_test_users_username")

    def __repr__(self):
        return f"<TestUsers: " \
               f"id={self.id}, " \
               f"name={self.name}, " \
               f"surname={self.surname}, " \
               f"middle_name={self.middle_name}, " \
               f"username={self.username}, " \
               f"password={self.password}, " \
               f"email={self.email}, " \
               f"access={self.access}, " \
               f"active={self.active}, " \
               f"start_active_time={self.start_active_time}>"
