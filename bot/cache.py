import diskcache as dc
from functools import wraps
import logging

logger = logging.getLogger(__name__)

cache = dc.Cache("./cachedir")


def get_full_function_name(func):
    if hasattr(func, "__qualname__"):
        return func.__qualname__
    return func.__name__


def cache_disk(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Generate a cache key based on the function name and arguments, excluding 'self'
        key = (func.__name__,) + args + tuple(kwargs.items())

        # Check cache
        if key in cache:
            logger.info(
                f"Function '{get_full_function_name(func)}' hit the cache. Return cached value."
            )
            return cache[key]

        # Call the function and cache its result
        result = func(self, *args, **kwargs)
        cache[key] = result
        return result

    return wrapper
