#!/usr/bin/env python3
"""
0x02-redis_basic
"""
import requests
import redis


def get_page(url: str) -> str:
    """A method that uses the requests module to obtain the HTML
    content of a particular URL and returns it."""
    redisInstance = redis.Redis()
    callsCount = redisInstance.get(f"count:{url}")
    callsCount = int(callsCount) + 1 if callsCount else 1
    response = requests.get(url)
    redisInstance.set(f"count:{url}", callsCount, ex=10)
    (
        print(f"The url: ({url}) was accessed {callsCount} time.")
        if callsCount == 1
        else print(f"The url: ({url}) was accessed {callsCount} times.")
    )


get_page("http://slowwly.robertomurray.co.uk")
