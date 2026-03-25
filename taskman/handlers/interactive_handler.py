from rich.console import Console
from rich.table import Table
from rich import box
import questionary
from taskman.core import Task, DeadlineTask, PriorityTask, JsonTaskRepo, TaskFactory
from taskman.commands import AddTaskCommand, CompleteTaskCommand, DeleteTaskCommand
from taskman.decorators import OverdueDecorator, UrgentDecorator
from taskman.events import EventBus, TaskEvent
from taskman.config import get_theme

console = Console()

def handle_interactive(args, repo: JsonTaskRepo, theme, run_command, undo_last):
    while True:
        console.clear()
        
        tasks = repo.get_all()
        decorated_tasks = []
        for t in tasks:
            if isinstance(t, DeadlineTask) and t.is_overdue():
                decorated_tasks.append(OverdueDecorator(t))
            elif isinstance(t, PriorityTask) and t.priority == 5:
                decorated_tasks.append(UrgentDecorator(t))
            else:
                decorated_tasks.append(t)
        
        # === Rich Table ===
        table = Table(title="TaskMan Interactive",
                      box=getattr(box, theme.border_style),
                      header_style=theme.header_color)
        table.add_column("ID", justify="center", width=4)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Title", min_width=20)
        table.add_column("Type", justify="center", width=14)
        table.add_column("Extra", justify="center", width=16)

        for task in decorated_tasks:
            raw_task = getattr(task, "_task", task)
            if isinstance(raw_task, DeadlineTask):
                extra = f"[{theme.overdue_color}]{raw_task.due_date}[/]" if raw_task.is_overdue() else f"[{theme.pending_color}]{raw_task.due_date}[/]"
            elif isinstance(raw_task, PriorityTask):
                extra = f"[{theme.priority_color}]{ '*' * raw_task.priority }[/]"
            else:
                extra = ""
            status = f"[{theme.done_color}]done[/]" if raw_task.done else f"[{theme.pending_color}]todo[/]"
            table.add_row(str(raw_task.id), status, raw_task.title or "", type(raw_task).__name__, extra)

        console.print(table)
        console.print(f"[dim]{sum(1 for t in tasks if t.done)}/{len(tasks)} complete[/]\n")

        # === Build menu mapping ===
        menu_map = {}
        choices = []

        for t in tasks:
            if not t.done:
                key = f"[{t.id}] {t.title}"
                choices.append(key)
                menu_map[key] = t

        if any(t.done for t in tasks):
            choices.append("--- done ---")

        for t in tasks:
            if t.done:
                key = f"[{t.id}] {t.title} (done)"
                choices.append(key)
                menu_map[key] = t

        choices += ["Add new task", "Undo last action", "Quit"]

        # === Ask user via arrow keys ===
        answer = questionary.select("Select a task or action:", choices=choices, qmark="➡").ask()

        if answer in (None, "Quit"):
            break
        elif answer == "Add new task":
            title = questionary.text("Task title:").ask()
            if title:
                p = questionary.text("Priority (1-5, leave empty for none):").ask()
                due = questionary.text("Deadline (YYYY-MM-DD, leave empty for none):").ask()
                task = TaskFactory.create(
                    title=title,
                    due=due if due else None,
                    priority=int(p) if p.isdigit() else None
                )

                run_command(AddTaskCommand(repo, task)) 
                console.print(f"[{theme.done_color}]Added task:[/] {task}")
                EventBus.publish(TaskEvent('created', task.id, task.title))
        elif answer == "Undo last action":
            undo_last()
        else:
            task = menu_map.get(answer)
            if not task:
                continue

            action = questionary.select(
                f"Task: {task.title}\nAction:",
                choices=["Mark done", "Delete", "Cancel"],
                qmark="➡"
            ).ask()

            if action == "Mark done":
                run_command(CompleteTaskCommand(repo, task.id))
            elif action == "Delete":
                run_command(DeleteTaskCommand(repo, task.id))
