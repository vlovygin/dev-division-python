nums = [849, 200, 809, 164, 926, 84, 892, 666, 880, 869, 775, 707, 874, 195, 120, 275,
        328, 228, 43, 445, 421, 246, 666, 324, 107, 455, 632, 666, 468, 603, 500]

printable: bool = True
even: bool = False

for num in nums:
    if num == 666:
        printable = not printable
        if printable:
            even = not even

    elif printable and even is (num % 2 == 0):
        print(num)
