import redis
from ansible_runner.datastores import SessionGetter


class RedisSessionGetter(SessionGetter):
    """"""

    def get_async_session(self):
        """Method that returns active redis session"""
        session = redis.Redis(
            host=self._connection_options["hostname"],
        )
        return session
