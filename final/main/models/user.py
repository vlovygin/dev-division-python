import datetime
from dataclasses import dataclass


@dataclass
class User:
    name: str
    surname: str
    middle_name: int
    username: str
    password: str
    email: str
    access: int
    active: int
    start_active_time: datetime.datetime

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "surname": self.surname,
            "middle_name": self.middle_name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "access": self.access,
            "active": self.active,
            "start_active_time": self.start_active_time
        }
