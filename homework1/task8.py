from contextlib import contextmanager


@contextmanager
def greetings(name):
    print(f"Привет, {name}!")
    yield name.upper()
    print(f"Пока, {name}!")


class Greetings:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Привет, {self.name}!")
        return self.name.upper()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Пока, {self.name}!")


with greetings("Илья") as name:
    for letter in name:
        print(letter * 3)

with Greetings("Илья") as name:
    for letter in name:
        print(letter * 3)
