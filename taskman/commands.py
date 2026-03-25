# Backward compatibility wrapper - imports moved to taskman.commands module
from taskman.commands.base import Command
from taskman.commands.add import AddTaskCommand
from taskman.commands.complete import CompleteTaskCommand
from taskman.commands.delete import DeleteTaskCommand

__all__ = ['Command', 'AddTaskCommand', 'CompleteTaskCommand', 'DeleteTaskCommand']

        self.repo.delete(self.task_id)

    def undo(self):
        if self._backup:
            self.repo.save(self._backup)