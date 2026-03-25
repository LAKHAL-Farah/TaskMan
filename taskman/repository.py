from abc import ABC, abstractmethod
from typing import List, Optional
from taskman.models import Task
from taskman.storage import load_tasks, save_tasks, DATA_FILE, load_tasks_verbose
from taskman.exceptions import TaskManError, StorageError, ValidationError



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
        existing = self.get_by_id(task.id)
        if existing:
            tasks = [t if t.id != task.id else task for t in tasks]
        else:
            tasks.append(task)
        save_tasks(tasks)

    def delete(self, id: int) -> None:
        tasks = self.get_all()
        before = len(tasks)
        tasks = [t for t in tasks if t.id != id]
        save_tasks(tasks)
        if before == len(tasks):
            raise TaskNotFoundError(id)