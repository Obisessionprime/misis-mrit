from ansible_runner import app

from ansible_runner.core.runner import TaskRunner


@app.post("/tasks")
def run_task(username):

    # Task runner creation
    task_runner = TaskRunner()
    
    # Task registration in database
    task_runner.register_taks()

    return {
        "Hello": "World"
    }


@app.get('/tasks/{id}')
def read_task(id: int):
    return {}


@app.get('/tasks/{id}')
def read_task(id: int):
    return {}


@app.get("/items/{item_id}")
def start(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
