import json
import os
import uuid

from ansible_runner.datastores.redis import RedisSessionGetter


class TaskRunner:
    """"""

    def __init__(self, redis_session_getter: RedisSessionGetter):
        """"""
        self._session_getter = redis_session_getter

    async def start_task(
        self,
        inventory_path,
        playbook_path,
        extra_vars
    ):
        """Method that runs ansible playbook"""
        task_initiator = 'admin'
        task_uuid = str(uuid.uuid4())
        pid = os.system(f'ansible-playbook -i {inventory_path} -e {extra_vars} {playbook_path}')
        session = self._session_getter.get_async_session()
        await session.set(task_uuid, json.dumps({
            'started_by': task_initiator,
            'pid': pid
        }))

        return task_uuid

    def cancel_task(self):
        """Method that cancels running task"""
        pass
