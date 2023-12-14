from ansible_runner.datastores import SessionGetter
from ansible_runner.datastores.postgresql.models.ssh_keys import SshKey


class SSHKeysController:
    """"""

    def __init__(self, postgresql_session_getter: SessionGetter):
        """
        Initialization method for task controller
        :param postgresql_session_getter: Class of SessionGetter object
        """
        self._session_getter = postgresql_session_getter

    async def get_record_by_id(self, identifier: int, session=None):
        """Method that gets"""
        if not session:
            session = self._session_getter.get_async_session()

        return await session.get(SshKey, identifier)

    async def create_record(self, data):
        """
        Method that creates entry about ssh key in relational database
        :param data:
        """
        try:
            session = self._session_getter.get_async_session()

            session.add(SshKey(
                private_key=data.private_key,
                public_key=data.public_key,
                username=data.username,
            ))
            await session.commit()
        except Exception as exception:
            print(f'Exception occurred! Original message was {exception}')
            return False
        else:
            return True

    async def read_record(self, ssh_pair_id):
        """
        Method that requests data about task from PostgreSQL session
        """
        result = await self.get_record_by_id(identifier=ssh_pair_id)

        return result

    async def update_record(self, ssh_pair_id, data):
        """"""
        session = self._session_getter.get_async_session()

        ssh_pair = await self.get_record_by_id(identifier=ssh_pair_id, session=session)

        data = dict(data)

        for data_key, data_value in data.items():
            if hasattr(ssh_pair, data_key):
                setattr(ssh_pair, data_key, data_value)

        await session.commit()

        return True

    async def delete_record(self, ssh_pair_id: int) -> bool:
        """
        Method that deletes entry about SSH key pair from database
        :param ssh_pair_id:
        """
        session = self._session_getter.get_async_session()

        ssh_pair = await self.get_record_by_id(identifier=ssh_pair_id, session=session)

        await session.delete(ssh_pair)

        await session.commit()

        return True
