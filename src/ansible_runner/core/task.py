from sqlalchemy.future import select
from datetime import datetime

from ansible_runner.datastores import SessionGetter
from ansible_runner.datastores.postgresql.models.tasks import Task
from ansible_runner.datastores.postgresql.repositories.tasks import TaskPostgresRepository


class TaskController:
    """Class that represents data manager for task instance"""

    def __init__(self, postgres_repository: TaskPostgresRepository):
        """
        Initialization method for task controller
        :param postgresql_session_getter: Class of SessionGetter object
        """
        self._postgres_repository = postgres_repository

    async def read_record(self, task_id):
        """Method """
        pass

    async def read_records(self, filters=None):
        """
        Method that requests data about task from PostgreSQL session
        """
        # Getting record using general PostgreSQL repository
        record = await self._postgres_repository.get_records(filters=filters)

        return record

    async def create_record(self, data) -> bool:
        """
        Method that creates object of models.Task class in database
        :param data: Dict of data for ansible_runner.postgresql.models.Task class
        """
        try:
            session = self._session_getter.get_async_session()

            session.add(Task(
                task_id=1,
                task_initiator_username='admin',
                task_runstart=datetime.now()))
            await session.commit()
        except Exception as exception:
            print(f'Exception occurred! Original message was {exception}')
            return False
        else:
            return True
