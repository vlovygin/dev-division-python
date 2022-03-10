import random

import pytest


@pytest.fixture
def random_set_of_integers() -> set:
    return {random.randint(0, 100) for _ in range(10)}


class TestSet:

    @pytest.mark.parametrize("val", [7, 5.2, "str", None, ("tuple")])
    def test_add_value_to_set(self, val):
        """
        Check adding hashable types to set
        """
        my_set = set()
        my_set.add(val)
        assert val in my_set, f"Value {val} not added to the set"

    def test_set_contains_unique_values(self):
        """
        Check the set contains only unique values
        """
        my_set = {1, 1, 2, 3, 3, 2, 1, 5, 0}
        assert my_set == {0, 1, 2, 3, 5}, "Set must be contains only unique values"

    def test_set_clear_method(self, random_set_of_integers):
        """
        Check remove all elements from set
        """
        random_set_of_integers.clear()
        assert len(random_set_of_integers) == 0, "Set must be empty"

    def test_not_subset(self):
        """
        Check items in the specified set not exists in the original set
        """
        my_set = {1, 5, 2}
        assert not {1, 3}.issubset(my_set), "The set is not subset of superset"

    def test_set_from_string(self):
        """
        Check that string converted to set with unique values
        """
        my_set = set("DevDivision")
        assert my_set == {"D", "e", "v", "i", "s", "o", "n"}, "Set must consist of the unique letters of the string"
