from rich.console import Console
from taskman.core import JsonTaskRepo
from taskman.commands import DeleteTaskCommand
from taskman.events import EventBus, TaskEvent
from taskman.config import get_theme

console = Console()

def handle_delete(args, repo: JsonTaskRepo, theme, run_command):
    try:
        run_command(DeleteTaskCommand(repo, args.id))
        EventBus.publish(TaskEvent('deleted', args.id, "Task deleted"))
        console.print(f"[{theme.done_color}]Deleted task with ID {args.id}[/]")
    except Exception as e:
        console.print(f"[red]Error deleting task with ID {args.id}: {e}[/]")
