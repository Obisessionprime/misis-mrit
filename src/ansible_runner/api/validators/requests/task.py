from typing import Optional

from pydantic import BaseModel


class TaskFiltersValidator(BaseModel):
    """Class that used for HTTP filters usage validation"""
    state: Optional[str] = None


class TaskValidator(BaseModel):
    """Class that represents validation model for task"""
    playbook_url: str
    extra_vars: str
    ssh_pair_id: int
    inventory_content: str
    initiator_username: str
