from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Task(BaseModel):
    task_id: int
    task_title: str
    task_desc: Optional[str] = ""
    is_finished: bool = False

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

# GET /tasks/{task_id}
@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if task is None:
        return {"status": "error", "error": "Task not found."}
    return {"status": "ok", "task": task}

# POST /tasks
@app.post("/tasks")
def create_task(task: Task):
    if any(t['task_id'] == task.task_id for t in task_db):
        return {"status": "error", "error": "Task ID already exists."}

    task_db.append(task.dict())
    return {"status": "ok", "task": task}

# PATCH /tasks/{task_id}
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    existing_task = next((t for t in task_db if t["task_id"] == task_id), None)
    
    if existing_task is None:
        return {"status": "error", "error": "Task not found."}
    if task.task_title:
        existing_task['task_title'] = task.task_title
    if task.task_desc is not None:
        existing_task['task_desc'] = task.task_desc
    if task.is_finished is not None:
        existing_task['is_finished'] = task.is_finished

    return {"status": "ok", "task": existing_task}

# DELETE /tasks/{task_id}
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global task_db
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    
    if task is None:
        return {"status": "error", "error": "Task not found."}

    task_db = [t for t in task_db if t["task_id"] != task_id]
    return {"status": "ok", "message": "Task deleted successfully."}

