import random

import pytest


@pytest.fixture
def random_int() -> int:
    return random.randint(-1000, 1000)


class TestInt:

    def test_zero_division(self, random_int):
        """
        Check division by zero
        """
        with pytest.raises(ZeroDivisionError):
            random_int / 0

    @pytest.mark.parametrize("val1, val2, result", [
        (0, 0, 0),
        (1, 0, 1),
        (0, 1, 1),
        (10, -15, -5),
        (-5, 10, 5)
    ])
    def test_sum_of_integers(self, val1, val2, result):
        """
        Check sum of two integers
        """
        assert val1 + val2 == result, f"Sum of {val1} and {val2} not equal to{result}"

    def test_integer_from_string(self):
        """
        Check convert string to integer
        """
        assert int("25") == 25, "Numeric string must be converted to integer"

    def test_chained_comparison(self):
        """
        Check chained comparison
        """
        assert -1 < 1 <= 5, "Chained comparison is not work"

    def test_integer_abs(self):
        """
        Check absolute value of the argument
        """
        assert abs(-5) == 5, "Abs method must be return absolute value of the integer argument"
