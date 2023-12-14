from typing import Dict

from fastapi import APIRouter

from ansible_runner.api.validators.requests.ssh_keys import SSHCreateRequestModel
from ansible_runner.config import GLOBAL_CONFIG
from ansible_runner.core.ssh_keys import SSHKeysController
from ansible_runner.datastores.postgresql import PostgreSQLRepository

ssh_router = APIRouter(
    prefix='/ssh_keys',
    tags=['SSH']
)


@ssh_router.post('')
async def add_ssh_key(data: SSHCreateRequestModel):
    """Route that adds ssh key to database"""
    result = (await SSHKeysController(PostgreSQLRepository(**GLOBAL_CONFIG['tasks_database'])).create_record(
        data=data,
    ))

    return {'status': 'ok' if result else 'error'}


@ssh_router.get('/{ssh_key_id}')
async def get_ssh_key(ssh_key_id: int):
    """
    Route that returns information about ssh key pair by ID
    :param ssh_key_id:  Identifier of SSH key pair
    """
    controller = SSHKeysController(PostgreSQLRepository(**GLOBAL_CONFIG['tasks_database']))
    result = (await controller.read_record(ssh_pair_id=ssh_key_id))

    return result


@ssh_router.patch('/{ssh_key_id}')
async def update_ssh_key(ssh_key_id: int, data: Dict) -> Dict[str, str]:
    """
    Route that updates information about ssh key pair by id and new data
    :param ssh_key_id:  Identifier of key pair entry
    :param data:    SSHValidator class-validated dictionary
    """
    controller = SSHKeysController(PostgreSQLRepository(**GLOBAL_CONFIG['tasks_database']))
    result = (await controller.update_record(ssh_pair_id=ssh_key_id, data=data))

    return {'status': 'ok' if result else 'error'}


@ssh_router.delete('/{ssh_key_id}')
async def delete_ssh_key(ssh_key_id: int) -> Dict[str, str]:
    """
    Method that deletes ssh pair entry from database
    :param ssh_key_id:  Identifier of key pair entry
    """
    controller = SSHKeysController(PostgreSQLRepository(**GLOBAL_CONFIG['tasks_database']))
    result = (await controller.delete_record(ssh_pair_id=ssh_key_id))
    return {'status': 'ok' if result else 'error'}
