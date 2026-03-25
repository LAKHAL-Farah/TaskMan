from .base import Command
from taskman.core import JsonTaskRepo

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
