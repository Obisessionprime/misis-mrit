import aioredis
from ansible_runner.datastores import SessionGetter


class RedisSessionGetter(SessionGetter):
    """"""

    def get_async_session(self):
        """"""
        session = aioredis.from_url(f'redis://{self._connection_options["hostname"]}')
        return session
