some_list = [1, 4, 6, 9, 2, 3, 5]


def reverse_list_1(lst: list) -> list:
    return lst[::-1]


def reverse_list_2(lst: list) -> list:
    lst.reverse()
    return lst


def reverse_list_3(lst: list) -> list:
    return list(reversed(lst))


def reverse_list_4(lst: list) -> list:
    result = []
    for i in lst:
        result.insert(0, i)
    return result


def reverse_list_5(lst: list) -> list:
    result = []
    for i in lst:
        result = [i] + result
    return result


def reverse_list_6(lst: list) -> list:
    for i in range(len(lst)):
        lst.insert(i, lst.pop())
    return lst


def reverse_list_7(lst: list) -> list:
    for i in range(len(lst) // 2):
        lst[i], lst[len(lst) - 1 - i] = lst[len(lst) - 1 - i], lst[i]
    return lst


def reverse_list_8(lst: list) -> list:
    return [lst[i] for i in range(len(lst) - 1, -1, -1)]


def reverse_list_9(lst: list) -> list:
    if not lst:
        return []
    else:
        return reverse_list_9(lst[1:]) + lst[:1]


print(reverse_list_1(some_list[:]))
print(reverse_list_2(some_list[:]))
print(reverse_list_3(some_list[:]))
print(reverse_list_4(some_list[:]))
print(reverse_list_5(some_list[:]))
print(reverse_list_6(some_list[:]))
print(reverse_list_7(some_list[:]))
print(reverse_list_8(some_list[:]))
print(reverse_list_9(some_list[:]))
