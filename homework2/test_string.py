import random
import string

import pytest


@pytest.fixture()
def random_string() -> str:
    return "".join(random.choice(string.printable) for _ in range(10))


class TestString:

    @pytest.mark.parametrize("s, pad_width, expected_result", [
        ("foo", 4, "0foo"),
        ("foo", 5, "00foo"),

        ("foo", 3, "foo"),
        ("foo", 1, "foo"),
        ("foo", 0, "foo"),
        ("foo", -1, "foo"),

        ("-foo", 5, "-0foo"),
        ("+foo", 5, "+0foo"),
        ("*foo", 5, "0*foo"),

        ("", 3, "000"),
        ("-", 3, "-00"),
        ("+", 3, "+00")
    ])
    def test_string_zfill(self, s, pad_width, expected_result):
        """
        Check adding zeros (0) at the beginning of the string, until it reaches the specified length.
        """
        result = s.zfill(pad_width)
        assert result == expected_result, f'Expected result of "{s}".zfill({pad_width}) is "{expected_result}", but given: "{result}")'

    def test_string_upper_method(self):
        """
        Check string contains all characters in upper case.
        """
        assert "FoO baR".upper() == "FOO BAR", "String must be converts to uppercase"

    def test_string_split_method(self):
        """
        Check split a string into a list
        """
        assert "Foo Bar".split() == ["Foo", "Bar"], "String must be split into a list"

    def test_string_immutables(self, random_string):
        """
        Check immutables of string
        """
        with pytest.raises(TypeError, match="'str' object does not support item assignment"):
            random_string[0] = "a"

    def test_string_concatenations(self):
        """
        Check concatenations of strings
        """
        assert "foo" + "bar" == "foobar", "String must be concatenated"
