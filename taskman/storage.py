import json
from pathlib import Path
from typing import List
from taskman.models import Task, DeadlineTask, PriorityTask


DATA_FILE = Path.home() / "taskman" / "tasks.json"


def _task_to_dict(task: Task) -> dict:
    d= {
        'type': task.__class__.__name__,
        'id': task.id,
        'title': task.title,
        'done': task.done
    }
    if isinstance(task, DeadlineTask):
        d['due_date'] = task.due_date
    if isinstance(task, PriorityTask):
        d['priority'] = task.priority
    return d

def _dict_to_task(d: dict) -> Task:
    kind = d.pop('type')
    if kind == 'DeadlineTask':
        return DeadlineTask(**d)
    if kind == 'PriorityTask':
        return PriorityTask(**d)

    return Task(**d)

def load_tasks() -> List[Task]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text())
    return [_dict_to_task(d) for d in raw]

def save_tasks(tasks: List[Task]) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    raw = json.dumps([_task_to_dict(t) for t in tasks], indent=2)
    DATA_FILE.write_text(raw)