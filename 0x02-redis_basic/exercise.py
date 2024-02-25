#!/usr/bin/env python3
"""
0x02. Redis basic
"""
import redis
import uuid
from typing import Union, Any, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """A decorator that takes a single method Callable
    argument and returns a Callable."""
    key = method.__qualname__

    @wraps(method)
    def incrCount(self, *args, **kwargs):
        """A method that increments the count for the key
        every time it's called."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return incrCount


def call_history(method: Callable) -> Callable:
    """A decorator to store the history of inputs and outputs
    for a particular function."""
    input = method.__qualname__ + ":inputs"
    output = method.__qualname__ + ":outputs"

    @wraps(method)
    def addInputOutput(self, *args):
        """A method that appends the input and output arguments."""
        self._redis.rpush(input, str(args))
        temporary = method(self, *args)
        self._redis.rpush(output, temporary)
        return temporary

    return addInputOutput


def replay(method):
    """A function that displays the history of the calls for a
    particular function."""
    instance = redis.Redis()
    methodName = method.__qualname__
    input = instance.lrange(methodName + ":inputs", 0, -1)
    output = instance.lrange(methodName + ":outputs", 0, -1)
    print(f"{methodName} was called {len(input)} times:")
    for key, val in zip(input, output):
        print(f"{methodName}(*{key.decode('utf-8')}) -> {val.decode('utf-8')}")


class Cache:
    """The Cache class"""

    def __init__(self) -> None:
        """The init method for Cache"""
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.count = 0

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """A method that generates a random uuid key and
        stores the input data in Redis using the random key
        and returns the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        """A method that take a key string argument and an optional
        Callable argument named fn. This callable will be used to
        convert the data back to the desired format."""
        data = self._redis.get(key)
        if fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """A method that will automatically parametrize Cache.get
        with the str conversion function."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """A method that will automatically parametrize Cache.get
        with the int conversion function."""
        return self.get(key, int)
