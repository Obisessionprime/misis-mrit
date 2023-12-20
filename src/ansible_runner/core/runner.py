import json
import os
import uuid

from ansible_runner.datastores.redis import RedisSessionGetter


class TaskRunner:
    """Class controller that resolves business logic for Task instance"""

    def __init__(self, redis_session_getter: RedisSessionGetter):
        """Initializer method that accepts session managers for Redis and PostgreSQL"""
        self._redis_session = redis_session_getter

    def _download_playbook(self, playbook_url: str, playbook_alias: str = 'test.yml'):
        """"""
        os.system('mkdir /tmp/playbooks')
        os.system(f'curl {playbook_url} -o /tmp/playbooks/{playbook_alias}')

        return f'/tmp/playbooks/{playbook_alias}'

    def _create_inventory(self, inventory_content: str):
        """"""
        with open('/tmp/playbooks/inventory', 'w') as inventory_file:
            inventory_file.write(inventory_content)

        return '/tmp/playbooks/inventory'

    async def start_task(
        self,
        inventory_content: str,
        playbook_url: str,
        extra_vars: str,
        task_initiator: str
    ):
        """Method that runs ansible playbook execution"""
        # Preparing playbook for execution
        playbook_path = self._download_playbook(playbook_url=playbook_url)
        inventory_path = self._create_inventory(inventory_content=inventory_content)

        # Creating task uuid for database navigation
        task_uuid = str(uuid.uuid4())

        pid = os.system(f'ansible-playbook -i {inventory_path} -e {extra_vars} {playbook_path}')

        # Getting REDIS session
        session = self._redis_session.get_async_session()

        # Setting information about running task
        session.set(task_uuid, json.dumps({
            'started_by': task_initiator,
            'pid': pid
        }))

        return task_uuid

    def interrupt_task_execution(self, task_id: str):
        """Method that cancels running task"""
        # Getting REDIS session
        session = self._redis_session.get_async_session()

        task_data = session.get(name=task_id)

        if not task_data:
            response = {'message': f'task {task_id} is not running!'}

        # Convert string returned from cache database to python object
        task_data = json.loads(task_data)

        os.system(f'kill -KILL {task_data["pid"]}')

        return {'message': f'task {task_id} interrupted!'}
