import json
from pathlib import Path
from typing import List
from taskman.models import Task, DeadlineTask, PriorityTask
from taskman.exceptions import StorageError, ValidationError
import time

from alive_progress import alive_bar


DATA_FILE = Path.home() / "taskman" / "tasks.json"


def _task_to_dict(task: Task) -> dict:
    d = {
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

    if not kind:
        raise ValidationError("Missing task type in stored data")
    if kind == 'DeadlineTask':
        return DeadlineTask(**d)
    if kind == 'PriorityTask':
        return PriorityTask(**d)
    if kind == 'Task':
        return Task(**d)

    raise ValidationError(f"Unknown task type: {kind}")


def load_tasks() -> List[Task]:
    if not DATA_FILE.exists():
        return []

    try:
        raw = json.loads(DATA_FILE.read_text())

        tasks = [_dict_to_task(d) for d in raw]

        if tasks:
            Task.count = max(t.id for t in tasks) + 1
        else:
            Task.count = 0

        return tasks
    except (json.JSONDecodeError, OSError) as e:
        raise StorageError(f"Failed to load tasks from {DATA_FILE}") from e
    except ValidationError as e:
        raise StorageError(f"Data validation error: {e}") from e


def save_tasks(tasks: List[Task]) -> None:
    try:
        DATA_FILE.parent.mkdir(exist_ok=True)
        raw = json.dumps([_task_to_dict(t) for t in tasks], indent=2)
        DATA_FILE.write_text(raw)
    except OSError as e:
        raise StorageError(f"Failed to save tasks to {DATA_FILE}") from e


def load_tasks_verbose(path: Path = DATA_FILE, verbose: bool = False) -> List[Task]:
    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        raise StorageError(f"Failed to load tasks from {path}") from e

    tasks: List[Task] = []
    if verbose:
        with alive_bar(len(raw), title="Loading tasks...") as bar:
            for d in raw:
                tasks.append(_dict_to_task(d))
                bar()
    else:
        tasks = [_dict_to_task(d) for d in raw]

        if tasks:
            Task.count = max(t.id for t in tasks) + 1
        else:
            Task.count = 0
    return tasks