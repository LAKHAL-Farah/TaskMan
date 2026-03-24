import json
from pathlib import Path
from typing import List
from taskman.models import Task, DeadlineTask, PriorityTask
import time

from alive_progress import alive_bar


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


def load_tasks_verbose(path: Path = DATA_FILE, verbose: bool = False) -> List[Task]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text())

    if not verbose:
        return [_dict_to_task(d) for d in raw]

    tasks : List[Task] = []
    with alive_bar(len(raw), title="Loading tasks...") as bar:
        for d in raw:
            tasks.append(_dict_to_task(d))
            #time.sleep(0.1)  
            # Simulate delay (just for demo purposes)
            bar()

    return tasks
