import inspect
import sys
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        name = inspect.getmodule(func).__name__.split(".")[3].capitalize()
        # Ignore T201
        print(f"{name} Took {total_time:.4f} seconds", file=sys.stderr)
        return result

    return timeit_wrapper
