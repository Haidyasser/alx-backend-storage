#!/usr/bin/env python3
""" Redis basic exercise """
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

def call_history(method: Callable) -> Callable:
    """ Decorator to log inputs and outputs of a method """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        
        # Normalize args as strings and push to the inputs list
        self._redis.rpush(input_key, str(args))
        
        # Call the original method and get the output
        output = method(self, *args, **kwargs)
        
        # Push the output to the outputs list
        self._redis.rpush(output_key, str(output))
        
        return output
    
    return wrapper

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
    @call_history
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
