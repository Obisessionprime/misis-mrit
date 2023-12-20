# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TaskState(Base):
    __tablename__ = 'task_state'
    __table_args__ = {'schema': 'ansible_runner'}

    state_id = Column(Integer, primary_key=True, server_default=text("nextval('ansible_runner.task_state_state_id_seq'::regclass)"))
    state_name = Column(String(256))


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'schema': 'ansible_runner'}

    task_id = Column(UUID, primary_key=True)
    task_initiator_username = Column(String(256), nullable=False)
    task_runstart = Column(DateTime, nullable=False)
    state_id = Column(ForeignKey('ansible_runner.task_state.state_id'))
