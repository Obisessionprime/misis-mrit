import uuid
from typing import Dict

from fastapi import APIRouter, Query

from ansible_runner.api.validators.requests.task import TaskValidator, TaskFiltersValidator
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
    tasks_controller = TaskController(PostgreSQLRepository(**GLOBAL_CONFIG['tasks_database']))

    # Task runner creation
    task_runner = TaskRunner(redis_session_getter=RedisSessionGetter(**GLOBAL_CONFIG['cache_database']))
    await task_runner.start_task(
        # inventory_path=f'/tmp/{task_uuid}',
        # playbook_path=f'/tmp/{task_uuid}/{data.playbook_path}',
        inventory_path='',
        playbook_path='',
        extra_vars=data.extra_vars
    )
    
    # Task registration in database
    result = await tasks_controller.create_record(data=data)

    return {'status': 'ok' if result else 'error'}


@tasks_router.get('')
async def get_tasks(state=Query(default=None,)):
    """Method that reads tasks allowing `state` parameter as filter"""
    tasks_controller = TaskController(TaskPostgresRepository(**GLOBAL_CONFIG['tasks_database']))
    return await tasks_controller.read_records(filters={'state': state} if state else None)


@tasks_router.get('/{task_id}')
async def read_task(task_id: int) -> Dict[str, str]:
    """
    Function that reads single task record from database
    :param task_id:     ID of task
    """
    tasks_controller = TaskController(TaskPostgresRepository(**GLOBAL_CONFIG['tasks_database']))
    records = await tasks_controller.read_records()
    return {}


@tasks_router.delete('/{task_id}')
def read_tasks(task_id: int) -> Dict[str, str]:
    """
    Function that interrupts task execution on jump host
    """
    return {}
