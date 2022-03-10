import random

import pytest


@pytest.fixture
def random_list_of_integers() -> list:
    return [random.randint(0, 100) for _ in range(10)]


class TestList:

    def test_reverse_list(self, random_list_of_integers):
        """
        Check list reverse
        """
        my_list = random_list_of_integers[:]
        for i in range(len(my_list) // 2):
            my_list[i], my_list[len(my_list) - 1 - i] = my_list[len(my_list) - 1 - i], my_list[i]

        random_list_of_integers.reverse()
        assert random_list_of_integers == my_list, "List must be reversed"

    def test_list_concatenations(self):
        """
        Check concatenations of lists
        """
        assert ["foo", "bar"] + ["DevDivision"] == ["foo", "bar", "DevDivision"], "List must be concatenated"

    @pytest.mark.parametrize("obj", [7, 5.2, "string", None, ("tuple",), ["list"], {"key": "dict"}, {"set"}])
    def test_list_append(self, obj):
        """
        Check append object to the end of the list
        """
        my_list = []
        my_list.append(obj)
        assert obj in my_list, f"Object {obj} not added to the list"

    def test_list_copy(self, random_list_of_integers):
        """
        Check list copy method create new shallow copy object of the list
        """
        my_list = random_list_of_integers
        my_list2 = list.copy(my_list)
        assert my_list is not my_list2, "Shallow copy of list must be a new object"

    def test_list_extend_method(self, random_list_of_integers):
        """
        Check extend list by appending elements from list
        """
        my_list = [1, 2, 3]
        my_list.extend(random_list_of_integers)
        assert my_list == [1, 2, 3] + random_list_of_integers, "List must be extended by new list"
