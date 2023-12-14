from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ansible_runner.datastores import SessionGetter
from ansible_runner.datastores.postgresql.models.ssh_keys import SshKey


class PostgreSQLRepository(SessionGetter):
    """Class that represents repository for PostgreSQL-specified datastorage"""

    def get_async_session(self):
        """Method that returns asyncronous session for PostgreSQL-specified database"""
        async_engine = create_async_engine(
            f'postgresql+asyncpg://'
            f'{self._connection_options["username"]}:'
            f'{self._connection_options["password"]}@'
            f'{self._connection_options["hostname"]}/'
            f'{self._connection_options["database"]}'
        )
        return sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )()

    async def get_records(self, filters: dict, session=None, **metadata):
        """Method that gets"""
        if 'model' not in metadata:
            raise Exception('model is required for PostgreSQL repository!')

        if not session:
            # Open new session if it wasn't presented as input parameter
            session = self.get_async_session()

        records = await session.execute(select(metadata['model']).where(**filters))

        return records

    async def create_record(self, objects: List):
        """
        Method that creates entry about ssh key in relational database
        :param objects:
        """
        try:
            session = self.get_async_session()

            for obj in objects:
                session.add(obj)
            await session.commit()
        except Exception as exception:
            print(f'Exception occurred! Original message was {exception}')
            return False
        else:
            return True

    # async def read_record(self, ssh_pair_id):
    #     """
    #     Method that requests data about task from PostgreSQL session
    #     """
    #     result = await self.get_record_by_id(identifier=ssh_pair_id)
    #
    #     return result

    # async def update_record(self, ssh_pair_id, data):
    #     """"""
    #     session = self._session_getter.get_async_session()
    #
    #     ssh_pair = await self.get_record_by_id(identifier=ssh_pair_id, session=session)
    #
    #     data = dict(data)
    #
    #     for data_key, data_value in data.items():
    #         if hasattr(ssh_pair, data_key):
    #             setattr(ssh_pair, data_key, data_value)
    #
    #     await session.commit()
    #
    #     return True
    #
    # async def delete_record(self, ssh_pair_id: int) -> bool:
    #     """
    #     Method that deletes entry about SSH key pair from database
    #     :param ssh_pair_id:
    #     """
    #     session = self._session_getter.get_async_session()
    #
    #     ssh_pair = await self.get_record_by_id(identifier=ssh_pair_id, session=session)
    #
    #     await session.delete(ssh_pair)
    #
    #     await session.commit()
    #
    #     return True
    #
