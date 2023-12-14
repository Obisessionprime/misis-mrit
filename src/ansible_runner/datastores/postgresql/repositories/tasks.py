from datetime import datetime
from typing import List

from ansible_runner.datastores.postgresql.models.tasks import Task

from ansible_runner.datastores.postgresql import PostgreSQLRepository


class TaskPostgresRepository(PostgreSQLRepository):
    """Class that represents repository for PostgreSQL instance of models.Task"""

    async def get_records(self, filters: dict = None, session=None, **metadata):
        """Method that returns models.Task object by specified filters"""
        sqlalchemy_filters = {}

        if filters:
            for filter_key, filter_value in filters.items():
                sqlalchemy_filters[getattr(Task, filter_key)] = filter_value

        return (await super().get_records(filters=sqlalchemy_filters, model=Task))[0]

    async def create_record(self, objects: List):
        """Method that creates objects of models.Task in postgresql relational database"""
        sqlalchemy_objects = []
        for obj in objects:
            sqlalchemy_objects.append(
                Task(
                    task_initiator_username=obj['task_initator_name'],
                    task_runstart=datetime.now(),
                )
            )

        return super().create_record(objects=sqlalchemy_objects)
