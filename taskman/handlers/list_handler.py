from rich.console import Console
from rich.table import Table
from rich import box
from taskman.core import DeadlineTask, PriorityTask
from taskman.core import JsonTaskRepo
from taskman.decorators import OverdueDecorator, UrgentDecorator
from taskman.config import get_theme
from taskman.core import SORTERS

console = Console()

def _decorate(task):
    if isinstance(task, DeadlineTask) and task.is_overdue():
        return OverdueDecorator(task)
    if isinstance(task, PriorityTask) and task.priority == 5:
        return UrgentDecorator(task)
    return task


def handle_list(args, repo: JsonTaskRepo, theme):
    tasks = repo.get_all()

    filtered = {
        'done': [t for t in tasks if t.done],
        'pending': [t for t in tasks if not t.done],
        'all': tasks
    }[args.filter]

    if not filtered:
        console.print("[yellow]No tasks to show[/]")
        return

    if hasattr(args, "sort") and args.sort:  
        sorter = SORTERS.get(args.sort)
        if sorter:
            filtered = sorter.sort(filtered)   

    table = Table(
        box=getattr(box, theme.border_style),
        header_style=theme.header_color
    )

    table.add_column("ID", width=4)
    table.add_column("Status", width=8)
    table.add_column("Title", min_width=22)
    table.add_column("Type", width=14)
    table.add_column("Extra", width=16)

    tasks_to_show = [_decorate(t) for t in filtered]

    for task in tasks_to_show:
        done = f"[{theme.done_color}]done[/]" if task.done else f"[{theme.pending_color}]todo[/]"
        extra = ""

        raw_task = getattr(task, "_task", task)

        if isinstance(raw_task, DeadlineTask):
            col = theme.overdue_color if raw_task.is_overdue() else theme.pending_color
            extra = f"[{col}]{raw_task.due_date}[/]"

        elif isinstance(raw_task, PriorityTask):
            extra = f"[{theme.priority_color}]{ '*' * raw_task.priority }[/]"

        table.add_row(
            str(raw_task.id),
            done,
            str(task),
            type(raw_task).__name__,
            extra
        )
    
    console.print(table)
    done_n = sum(1 for t in filtered if t.done)
    console.print(f"[dim]{done_n}/{len(filtered)} complete[/]")
