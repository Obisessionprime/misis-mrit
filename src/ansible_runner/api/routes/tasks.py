import uuid
from typing import Dict

from fastapi import APIRouter

from ansible_runner.api.validators.requests.task import TaskValidator
from ansible_runner.config import GLOBAL_CONFIG
from ansible_runner.core.runner import TaskRunner
from ansible_runner.core.task import TaskController
from ansible_runner.datastores.postgresql import PostgreSQLRepository
from ansible_runner.datastores.postgresql.repositories.tasks import TaskPostgresRepository
from ansible_runner.datastores.redis import RedisSessionGetter

tasks_router = APIRouter(
    prefix='/tasks',
    tags=['TASKS']
)


@tasks_router.post('')
async def run_task(data: TaskValidator) -> Dict[str, str]:
    """
    Route function for ansible task running functional. This function creates task object in database and
    starts execution on current jump host
    """
    tasks_controller = TaskController(
        postgres_repository=TaskPostgresRepository(**GLOBAL_CONFIG['tasks_database'])
    )

    # Task runner creation
    task_runner = TaskRunner(redis_session_getter=RedisSessionGetter(**GLOBAL_CONFIG['cache_database']))

    task_uuid = (await task_runner.start_task(
        inventory_content=data.inventory_content,
        playbook_url=data.playbook_url,
        extra_vars=data.extra_vars,
        task_initiator=data.initiator_username
    ))

    data = dict(data)
    data['task_id'] = task_uuid

    # Task registration in database
    await tasks_controller.create_record(data=data)

    return {'task_uuid': task_uuid}


@tasks_router.get('')
async def get_tasks():
    """Method that reads tasks allowing `state` parameter as filter"""
    tasks_controller = TaskController(TaskPostgresRepository(**GLOBAL_CONFIG['tasks_database']))
    return await tasks_controller.read_records()


@tasks_router.delete('/{task_id}')
async def interrupt_task_execution(task_id: str) -> Dict[str, str]:
    """
    Function that reads single task record from database
    :param task_id:     ID of task
    """
    task_runner = TaskRunner(redis_session_getter=RedisSessionGetter(**GLOBAL_CONFIG['cache_database']))
    return task_runner.interrupt_task_execution(task_id=task_id)
