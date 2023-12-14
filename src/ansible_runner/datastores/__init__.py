from abc import ABC


class SessionGetter(ABC):
    """Class that returns session object of connection to any database"""

    def __init__(self, **connection_options):
        """Initialization class that gets connection options"""
        self._connection_options = connection_options

    def get_async_session(self):
        """Method that returns asynchronous session connection to database"""
        raise NotImplementedError('Method get_session of SessionGetter subclass should be implemented!')

    async def get_records(self, filters: dict, session=None, **metadata):
        """Method that returns one object from database by presented filters"""
        raise NotImplementedError('Method get_record of SessionGetter subclass should be implemented!')
