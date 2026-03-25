import json
from pathlib import Path
from typing import List
from taskman.models import Task, DeadlineTask, PriorityTask
from taskman.exceptions import StorageError, ValidationError
import time
import shutil
from datetime import datetime
import re


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




def recover_tasks_from_corrupt_file(path: Path) -> List[Task]:
    import re, shutil
    ts = datetime.now().strftime('%Y%m%dT%H%M%S')
    bak = path.with_suffix(f'.{ts}.bak')
    shutil.copy(path, bak)
    print(f"Corrupt tasks.json backed up to {bak.name}. Attempting recovery...")

    raw = []
    try:
        text = path.read_text(encoding='utf-8')
        matches = re.findall(r'\{[^}]*\}', text, flags=re.DOTALL)
        for m in matches:
            try:
                d = json.loads(m)
                raw.append(d)
            except json.JSONDecodeError:
                continue
    except Exception as e:
        Task.count = 0
        path.unlink(missing_ok=True)
        print(f"Failed to read corrupt file for recovery: {e}")
        return []

    tasks: List[Task] = []
    for d in raw:
        try:
            tasks.append(_dict_to_task(d))
        except ValidationError:
            continue

    if tasks:
        Task.count = max(t.id for t in tasks) + 1
    else:
        Task.count = 0

    try:
        path.write_text(json.dumps([_task_to_dict(t) for t in tasks], indent=2), encoding='utf-8')
    except Exception:
        pass  

    return tasks

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

    except ValidationError as e:
        raise StorageError(f"Data validation error: {e}") from e

    except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
        return recover_tasks_from_corrupt_file(DATA_FILE)
    

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
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValidationError):
        return recover_tasks_from_corrupt_file(path)

    tasks: List[Task] = []
    if verbose:
        from alive_progress import alive_bar
        with alive_bar(len(raw), title="Loading tasks...") as bar:
            for d in raw:
                try:
                    tasks.append(_dict_to_task(d))
                except ValidationError:
                    continue  
                bar()
    else:
        for d in raw:
            try:
                tasks.append(_dict_to_task(d))
            except ValidationError:
                continue

    if tasks:
        Task.count = max(t.id for t in tasks) + 1
    else:
        Task.count = 0

    return tasks


    