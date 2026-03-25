from .base import Command
from taskman.core import Task
from taskman.core import JsonTaskRepo

class AddTaskCommand(Command):
    def __init__(self, repo: JsonTaskRepo, task: Task):
        self.repo = repo
        self.task = task

    def execute(self):
        self.repo.save(self.task)

    def undo(self):
        self.repo.delete(self.task.id)
