import random
import uuid

import faker
from main.models.user import User

fake = faker.Faker('ru_RU')


class DataManager:

    @staticmethod
    def uuid():
        """ Generate a random UUID """

        return uuid.uuid4()

    def randint(self):
        """ Generate a random integer """

        return random.randint(0, 100000)

    def email(self):
        """ Generate a random email """

        return f"{self.uuid()}@{fake.domain_name()}"

    def user(self, name=None, surname=None, middle_name=None, username=None, password=None, email=None, access=None,
             active=None, start_active_time=None):
        user = User(
            name=name or fake.first_name(),
            surname=surname or fake.last_name(),
            middle_name=middle_name or fake.middle_name(),
            username=username or fake.bothify(text="?" * 16),
            password=password or fake.bothify(text="?#" * 5),
            email=email or self.email(),
            access=access,
            active=active,
            start_active_time=start_active_time
        )
        return user
