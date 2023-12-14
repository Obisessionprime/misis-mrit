from typing import Optional

from pydantic import BaseModel


class TaskFiltersValidator(BaseModel):
    """"""
    state: Optional[str] = None

class TaskValidator(BaseModel):
    """Class that represents validation model for task"""
    playbook_path: str
    extra_vars: str
    ssh_pair_id: int
    inventory_content: str
