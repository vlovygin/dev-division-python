import pytest


@pytest.fixture(params=[["list"], {"set"}, {"key": "dict"}])
def unhashable_obj(request):
    return request.param


class TestDictionary:

    def test_dict_update_exists_key(self):
        """
        Check updating exists key
        """
        my_dict = {"Dev": "Division"}
        my_dict.update({"Dev": "Multiplication"})
        assert my_dict["Dev"] == "Multiplication", "Dictionary values must be updated"

    def test_dict_get_default_value(self):
        """
        Check that return default get value, if key is not exists
        """
        my_dict = {"Dev": "Division"}
        assert my_dict.get("Test", "default") == "default", "Must be return default value"

    def test_dict_clear_method(self):
        """
        Check remove all elements from dict
        """
        my_dict = {"Dev": "Division"}
        my_dict.clear()
        assert len(my_dict) == 0, "Dict must be empty"

    def test_dict_keys_is_hashable_type(self, unhashable_obj):
        """
        Check not adding unhashable key to dict
        """
        with pytest.raises(TypeError, match="unhashable type"):
            my_dict = {unhashable_obj: "test"}

    def test_dict_unhashable_type(self):
        """
        Check that dictionary is unhashable type
        """
        my_dict = {"foo": "bar"}
        assert my_dict.__hash__ is None, "Dictionary is a unhashable type"
