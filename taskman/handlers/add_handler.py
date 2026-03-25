from rich.console import Console
from taskman.core import TaskFactory
from taskman.core import JsonTaskRepo
from taskman.commands import AddTaskCommand
from taskman.events import EventBus, TaskEvent
from taskman.config import get_theme

console = Console()

def handle_add(args, repo: JsonTaskRepo, theme, run_command):
    task = TaskFactory.create(
        title=args.title,
        due=args.due,
        priority=args.priority
    )
    run_command(AddTaskCommand(repo, task))

    console.print(f"[{theme.done_color}]Added task:[/] {task}")
    EventBus.publish(TaskEvent('created', task.id, task.title))
