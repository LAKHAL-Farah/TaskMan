from .base import Command
from taskman.core import JsonTaskRepo

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
