#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable
import functools


class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    def set(self, key, value):
        """Définir une paire clé-valeur dans le cache."""
        self._redis.set(key, value)

    def get(self, key, fn: Callable = None):
        """Obtenir la valeur associée à une clé depuis le cache."""
        value = self._redis.get(key)
        if value is not None and fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Obtenir la valeur associée à une clé depuis le cache obdlha l strg."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Obtenir la valeur associée à une clé depuis le cache obdlha lint."""
        return self.get(key, int)
    
    def delete(self, key):
        """Supprimer une paire clé-valeur du cache."""
        self._redis.delete(key)

    def clear(self):
        """Effacer l'intégralité du cache."""
        self._redis.flushdb()
    
    @functools.wraps(set)
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store input data in Redis and return the stored value."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self_instance = args[0]  # 'self' is the instance of the Cache class
        method_name = func.__qualname__  # Qualified name of the method
        count_key = f"{method_name}_calls"  # Key for counting method calls
        self_instance._redis.incr(count_key)  # Increment count for method calls
        return func(*args, **kwargs)
    return wrapper

# Decorate the 'store' method of Cache class with 'count_calls'
Cache.store = count_calls(Cache.store)
