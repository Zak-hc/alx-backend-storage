#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store input data in Redis and return the randomly generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
