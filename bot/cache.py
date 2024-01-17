import diskcache as dc
from functools import wraps

cache = dc.Cache('./cachedir')

def cache_disk(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Generate a cache key based on the function name and arguments, excluding 'self'
        key = (func.__name__,) + args + tuple(kwargs.items())

        # Check cache
        if key in cache:
            return cache[key]

        # Call the function and cache its result
        result = func(self, *args, **kwargs)
        cache[key] = result
        return result

    return wrapper