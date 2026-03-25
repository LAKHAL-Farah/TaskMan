# Backward compatibility wrapper - imports moved to taskman.core
from taskman.core.storage import load_tasks, save_tasks, load_tasks_verbose, DATA_FILE, recover_tasks_from_corrupt_file

__all__ = ['load_tasks', 'save_tasks', 'load_tasks_verbose', 'DATA_FILE', 'recover_tasks_from_corrupt_file']


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


    