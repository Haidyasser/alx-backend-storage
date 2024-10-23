#!/usr/bin/env python3
""" Redis basic exercise """
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator to count the number of calls to a method """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """ Cache class """

    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()  # Clear the database for a fresh start

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis """
        key = f"data:{uuid.uuid4()}"
        self._redis.set(key, data)
        return key

    @count_calls
    def get(self, key: str, fn: Callable = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """ Get data from Redis """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    @count_calls
    def get_str(self, key: str) -> Optional[str]:
        """ Get string from bytes """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    @count_calls
    def get_int(self, key: str) -> Optional[int]:
        """ Get int from bytes """
        return self.get(key, fn=lambda d: int(d))
