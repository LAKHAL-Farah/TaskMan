from rich.console import Console
from rich.panel import Panel
from rich import box
from taskman.core import Task, DeadlineTask, PriorityTask, JsonTaskRepo
from taskman.config import get_theme

console = Console()

def handle_stats(args, repo: JsonTaskRepo, theme):
    tasks = repo.get_all()
    total = len(tasks)
    done = sum(1 for t in tasks if t.done)
    overdue = sum(1 for t in tasks if isinstance(t, DeadlineTask) and t.is_overdue() and not t.done)

    pct = int(done / total * 100) if total else 0

    by_type = {
        'Task': sum(isinstance(t, Task) and not isinstance(t, (DeadlineTask, PriorityTask)) for t in tasks),
        'DeadlineTask': sum(isinstance(t, DeadlineTask) for t in tasks),
        'PriorityTask': sum(isinstance(t, PriorityTask) for t in tasks)
    }

    body = (
        f"[bold]{total}[/] total "
        f"[{theme.done_color}]{done}[/] done "
        f"[{theme.overdue_color}]{overdue}[/] overdue "
        f"[{theme.header_color}]{pct}%[/]\n"
    )

    for kind, count in by_type.items():
        body += f"[cyan]{kind:<12}[/]: {count}\n"

    console.print(Panel(body, title="TaskMan Stats", box=box.DOUBLE))
