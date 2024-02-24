#!/usr/bin/env python3
"""
0x02. Redis basic
"""
import redis
import uuid
from typing import Union


class Cache:
    """The Cache class"""

    def __init__(self) -> None:
        """The init method for Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int]) -> str:
        """A method that generates a random uuid key and
        stores the input data in Redis using the random key
        and returns the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
