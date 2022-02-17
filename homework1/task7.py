import time
from functools import wraps


def timing(f):
    """Decorator for measure the execution time of functions"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        print(f"Function {f.__name__} took {end_time - start_time} secs")
        return result

    return wrapper


@timing
def func():
    import random
    import time
    time.sleep(random.randint(0, 10))


func()
func()
func()
