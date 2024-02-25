#!/usr/bin/env python3
"""
Main file
"""
import redis

# TASK 0

Cache = __import__('exercise').Cache

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

# TASK 1

cache1 = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

local = redis.Redis()
for value, fn in TEST_CASES.items():
    key = cache1.store(value)
    assert cache1.get(key, fn=fn) == value


# TASK 2

Cache = __import__('exercise').Cache

cache2 = Cache()

cache2.store(b"first")
print(cache2.get(cache2.store.__qualname__))

cache2.store(b"second")
cache2.store(b"third")
print(cache2.get(cache2.store.__qualname__))
