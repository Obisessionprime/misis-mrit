# coding: utf-8
from sqlalchemy import Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SshKey(Base):
    __tablename__ = 'ssh_keys'
    __table_args__ = {'schema': 'ansible_runner'}

    ssh_key_id = Column(Integer, primary_key=True, server_default=text("nextval('ansible_runner.ssh_keys_ssh_key_id_seq'::regclass)"))
    private_key = Column(String)
    public_key = Column(String)
    username = Column(String)
