from pydantic import BaseModel, Field


class SSHResponseModel(BaseModel):
    """Class that represents validation model for SSH pair"""
    ssh_key_id: int
    public_key: str = Field(pattern=r'ssh-rsa AAAA[0-9A-Za-z+/]+[=]{0,3} ([^@]+@[^@]+)')
    private_key: str
    username: str
