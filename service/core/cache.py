import redis
from decouple import config


# TODO: add validation to dev (local redis) or stg (server redis)

class LoginTokens:
    _instance_token_login = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_token_login is None:
            cls._instance_token_login = super(LoginTokens, cls).__new__(cls)
            cls._instance_token_login._redis = redis.StrictRedis(
                host=config('REDIS_HOST'),
                port=config('REDIS_PORT'),
                db=config('REDIS_TOKENS_DB'),
                password=config('REDIS_PASSWORD')
            )
        return cls._instance_token_login

    def get_connection(self):
        return self._redis
