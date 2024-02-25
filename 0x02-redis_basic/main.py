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

cache2 = Cache()

cache2.store(b"first")
print(cache2.get(cache2.store.__qualname__))

cache2.store(b"second")
cache2.store(b"third")
print(cache2.get(cache2.store.__qualname__))

# TASK 3

cache3 = Cache()

s1 = cache3.store("first")
print(s1)
s2 = cache3.store("secont")
print(s2)
s3 = cache3.store("third")
print(s3)

inputs = cache3._redis.lrange("{}:inputs".format(cache3.store.__qualname__), 0, -1)
outputs = cache3._redis.lrange("{}:outputs".format(cache3.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))


# TASK 4
print("------------------------------")

replay = __import__('exercise').replay

cache4 = Cache()

cache4.store("foo")
cache4.store("bar")
cache4.store(42)
replay(cache4.store)
