from collections import Counter

my_dict = {'a': 500, 'b': 5874, 'c': 560, 'd': 400, 'e': 5874, 'f': 20}


def dict_max_value_keys(dict_: dict, cnt: int = 2) -> list:
    """
    Return list of a dictionary keys (default: 2) with maximum values
    """
    return sorted(dict_, key=dict_.get, reverse=True)[:cnt]


print(dict_max_value_keys(my_dict))

print([elem for elem, _ in Counter(my_dict).most_common(2)])
