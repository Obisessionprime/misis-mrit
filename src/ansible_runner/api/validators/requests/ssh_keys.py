from pydantic import BaseModel, Field


class SSHCreateRequestModel(BaseModel):
    """Class that represents validation model for SSH pair"""
    public_key: str = Field(pattern=r'ssh-rsa AAAA[0-9A-Za-z+/]+[=]{0,3} ([^@]+@[^@]+)')
    private_key: str
    username: str
