# taskman/commands.py
from abc import ABC, abstractmethod
from taskman.models import Task
from taskman.repository import JsonTaskRepo

class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class AddTaskCommand(Command):
    def __init__(self, repo: JsonTaskRepo, task: Task):
        self.repo = repo
        self.task = task

    def execute(self):
        self.repo.save(self.task)

    def undo(self):
        self.repo.delete(self.task.id)

class CompleteTaskCommand(Command):
    def __init__(self, repo: JsonTaskRepo, task_id: int):
        self.repo = repo
        self.task_id = task_id
        self._prev_done = None

    def execute(self):
        t = self.repo.get_by_id(self.task_id)
        self._prev_done = t.done
        t.complete()
        self.repo.save(t)

    def undo(self):
        t = self.repo.get_by_id(self.task_id)
        t.done = self._prev_done
        self.repo.save(t)

class DeleteTaskCommand(Command):
    def __init__(self, repo: JsonTaskRepo, task_id: int):
        self.repo = repo
        self.task_id = task_id
        self._backup = None

    def execute(self):
        self._backup = self.repo.get_by_id(self.task_id)
        self.repo.delete(self.task_id)

    def undo(self):
        if self._backup:
            self.repo.save(self._backup)