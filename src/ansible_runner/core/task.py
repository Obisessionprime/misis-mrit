from datetime import datetime

from ansible_runner.datastores.postgresql.models.tasks import Task
from ansible_runner.datastores.postgresql.repositories.tasks import TaskPostgresRepository


class TaskController:
    """Class that represents data manager for task instance"""

    def __init__(self, postgres_repository: TaskPostgresRepository):
        """
        Initialization method for task controller
        :param postgres_repository: Class of SessionGetter object
        """
        self._postgres_repository = postgres_repository

    async def read_record(self, task_id):
        """Method that returns task entry by identifier"""
        filters = {'task_id': task_id}

        records = await self._postgres_repository.get_records(filters=filters)

        return records[0] if len(records) else []

    async def read_records(self, filters=None):
        """
        Method that requests data about task from PostgreSQL session
        """
        # Getting record using general PostgreSQL repository
        records = await self._postgres_repository.get_records(filters=filters)

        return records

    async def create_record(self, data: dict) -> bool:
        """
        Method that creates object of models.Task class in database
        :param data: Dict of data for ansible_runner.postgresql.models.Task class
        """
        objects = [data]

        await self._postgres_repository.create_record(objects=[data])

        return True
