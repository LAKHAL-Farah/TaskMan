from rich.console import Console
from taskman.core import JsonTaskRepo
from taskman.commands import CompleteTaskCommand
from taskman.events import EventBus, TaskEvent
from taskman.config import get_theme

console = Console()

def handle_done(args, repo: JsonTaskRepo, theme, run_command):
    task = repo.get_by_id(args.id)
    if not task:
        console.print(f"[red]Task with ID {args.id} not found[/]")
        return
    if task.done:
        console.print(f"[yellow]Task with ID {args.id} is already marked as done[/]")
        return
    run_command(CompleteTaskCommand(repo, task.id))  

    console.print(f"[{theme.done_color}]Task marked as done:[/] {task}")
    EventBus.publish(TaskEvent('completed', task.id, task.title))
