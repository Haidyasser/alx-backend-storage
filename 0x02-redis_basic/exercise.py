#!/usr/bin/env python3
""" Redis basic exercise """
import redis
import uuid
from typing import Union, Optional


class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis """
        key = f"data:{uuid.uuid4()}"
        self._redis.set(key, data)
        return key 

    def get(self, key: str, fn: callable = None) -> Optional[Union[str, bytes, int, float]]:
        """ get data from Redis """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """ get string from bytes """
        return self.get(key, fn=lambda d: d.decode('utf-8'))
    
    def get_int(self, key: str) -> Optional[int]:
        """ get int from bytes """
        return self.get(key, fn=lambda d: int(d))
