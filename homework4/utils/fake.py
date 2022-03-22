import uuid
from faker import Faker
from datetime import datetime

fake = Faker('ru_RU')


def random_uuid():
    return str(uuid.uuid4())


def current_date(fmt="%Y-%m-%d"):
    return datetime.today().strftime(fmt)
