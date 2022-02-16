welcome_string = """
Select operation:
    1. Add (+)
    2. Subtract (-)
    3. Multiply (*)
    4. Divide (/)
"""

while True:
    print(welcome_string)

    operation = input("Enter operation (1/2/3/4): ")

    if operation in ("1", "2", "3", "4"):
        try:
            num_1 = int(input("Enter first number: "))
            num_2 = int(input("Enter second number: "))
        except:
            print("Entered values are not a number. Try again.")
            continue

        try:
            if operation == "1":
                print(f"{num_1} + {num_2} = {num_1 + num_2}")
            elif operation == "2":
                print(f"{num_1} - {num_2} = {num_1 - num_2}")
            elif operation == "3":
                print(f"{num_1} * {num_2} = {num_1 * num_2}")
            elif operation == "4":
                print(f"{num_1} / {num_2} = {num_1 / num_2}")
        except Exception as e:
            print(f"Something went wrong: {e}. Try again.")
        else:
            continue

    else:
        print(f"Unsupported operation: \"{operation}\". Try again.")
