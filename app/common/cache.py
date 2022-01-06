import redis
from django.conf import settings


class RedisCache:
    """
    Simple cache based on redis.
    """

    def __init__(self, host, port, db):
        self._redis = redis.Redis(host=host, port=port, db=db)

    def cache_value(self, key: str, value, expire=None):
        self._redis.set(key, value)

        if expire:
            self._redis.expire(key, expire)

    def get_value(self, key: str):
        data = self._redis.get(key)
        if data:
            return data.decode()


cache = RedisCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
