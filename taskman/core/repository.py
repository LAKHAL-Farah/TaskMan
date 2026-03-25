from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Task
from .storage import load_tasks, save_tasks, DATA_FILE, load_tasks_verbose
from taskman.exceptions import TaskManError, StorageError, ValidationError
from taskman.exceptions import TaskNotFoundError


class AbstractTaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]: ...
    @abstractmethod
    def get_by_id(self, id:int) -> Optional[Task]: ...
    @abstractmethod
    def save(self, task: Task) -> None: ...
    @abstractmethod
    def delete(self, id: int) -> None: ...


class JsonTaskRepo(AbstractTaskRepository):
    def __init__(self, path: DATA_FILE):
        self.path = path
    def get_all(self) -> List[Task]:
        return load_tasks_verbose(self.path)

        
    def get_by_id(self, id: int) -> Optional[Task]:
        return next((t for t in self.get_all() if t.id == id), None)

    def save(self, task: Task) -> None:
        tasks = self.get_all()

        if task.id == -1:
            max_id = max([t.id for t in tasks], default=-1)
            task.id = max_id + 1

        existing = next((t for t in tasks if t.id == task.id), None)
        if existing:
            tasks = [t if t.id != task.id else task for t in tasks]
        else:
            tasks.append(task)

        Task.count = max(Task.count, max(t.id for t in tasks) + 1)

        save_tasks(tasks)

    def delete(self, id: int) -> None:
        tasks = self.get_all()
        before = len(tasks)
        tasks = [t for t in tasks if t.id != id]
        save_tasks(tasks)
        if before == len(tasks):
            raise ValueError(f"Task with ID {id} not found")
