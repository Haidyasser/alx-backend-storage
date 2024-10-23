#!/usr/bin/env python3
""" Redis basic exercise """
import redis
import uuid
from typing import Union, Optional
from functools import wraps


class Cache:
    """ Cache class """

    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.call_count = {}

    def count_calls(self, fn: callable) -> callable:
        """ Decorator to count calls to a method """
        @wraps(fn)
        def wrapper(*args, **kwargs):
            name = fn.__name__
            self.call_count[name] = self.call_count.get(name, 0) + 1
            return fn(*args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis """
        key = f"data:{uuid.uuid4()}"
        self._redis.set(key, data)
        return key

    @count_calls
    def get(self, key: str, fn: callable = None
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
