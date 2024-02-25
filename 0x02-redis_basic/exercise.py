#!/usr/bin/env python3
"""
0x02. Redis basic
"""
import redis
import uuid
from typing import Union, Any, Callable


class Cache:
    """The Cache class"""

    def __init__(self) -> None:
        """The init method for Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A method that generates a random uuid key and
        stores the input data in Redis using the random key
        and returns the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable) -> Any:
        """A method that take a key string argument and an optional
        Callable argument named fn. This callable will be used to
        convert the data back to the desired format."""
        data = self._redis.get(key)
        if data:
            if fn and Callable(fn):
                data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """A method that will automatically parametrize Cache.get
        with the str conversion function."""
        pass

    def get_int(self, key: str) -> int:
        """A method that will automatically parametrize Cache.get
        with the int conversion function."""
        pass
