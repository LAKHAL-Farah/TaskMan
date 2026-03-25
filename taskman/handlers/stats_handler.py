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

    # Build stats string, handling empty theme colors
    done_str = f"[{theme.done_color}]{done}[/]" if theme.done_color else str(done)
    overdue_str = f"[{theme.overdue_color}]{overdue}[/]" if theme.overdue_color else str(overdue)
    pct_str = f"[{theme.header_color}]{pct}%[/]" if theme.header_color else f"{pct}%"
    
    body = (
        f"[bold]{total}[/] total "
        f"{done_str} done "
        f"{overdue_str} overdue "
        f"{pct_str}\n"
    )

    for kind, count in by_type.items():
        body += f"[cyan]{kind:<12}[/]: {count}\n"

    console.print(Panel(body, title="TaskMan Stats", box=box.DOUBLE))
