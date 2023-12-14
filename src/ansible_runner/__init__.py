import os
from fastapi import FastAPI

from ansible_runner.api.routes.tasks import tasks_router
from ansible_runner.api.routes.ssh_keys import ssh_router

app = FastAPI(docs_url='/documentation')

app.include_router(
    router=tasks_router,
    prefix=f'/api/{os.environ.get("ANSIBLE_RUNNER_API_PREFIX", "")}'.rstrip('/'),
)

app.include_router(
    router=ssh_router,
    prefix=f'/api/{os.environ.get("ANSIBLE_RUNNER_API_PREFIX", "")}'.rstrip('/'),
)
