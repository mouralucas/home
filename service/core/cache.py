import redis
from decouple import config


# TODO: add validation to dev (local redis) or stg (server redis)

class LoginTokens:
    _instance_login_token = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_login_token is None:
            cls._instance = super(LoginTokens, cls).__new__(cls)
            cls._instance_login_token._redis = redis.StrictRedis(
                host=config('REDIS_HOST'),
                port=config('REDIS_PORT'),
                db=config('REDIS_TOKENS_DB'),
                password=config('REDIS_PASSWORD')
            )
        return cls._instance_login_token

    def get_connection(self):
        return self._redis


class CompanyProducts:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CompanyProducts, cls).__new__(cls)
            cls._instance._redis = redis.StrictRedis(
                host=config('REDIS_HOST'),
                port=config('REDIS_PORT'),
                db=config('REDIS_COMPANY_PRODUCTS_DB'),
                password=config('REDIS_PASSWORD')
            )
        return cls._instance

    def get_connection(self):
        return self._redis
