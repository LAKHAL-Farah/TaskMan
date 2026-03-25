import argparse
import questionary
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns 
from taskman.themes import get_theme
import shutil
from taskman.events import EventBus, TaskEvent
from taskman.observers import LogObserver

from taskman.commands import AddTaskCommand, CompleteTaskCommand, DeleteTaskCommand, Command
from taskman.config import Config, handle_config_set, ConfigError


from taskman.models import Task, DeadlineTask, PriorityTask
from taskman.storage import load_tasks, save_tasks, load_tasks_verbose, DATA_FILE
from taskman.repository import JsonTaskRepo

from taskman.sorters import SORTERS


cfg = Config.load()        
theme = get_theme(cfg)
console = Console()
LOG_PATH = "history.log"
EventBus.subscribe(LogObserver(LOG_PATH))

history: list[Command] = []

def run(cmd: Command):
    cmd.execute()
    history.append(cmd)

def undo_last():
    if history:
        history.pop().undo()
        console.print("[green]Last action undone[/]")
    else:
        console.print("[yellow]Nothing to undo[/]")


def handle_add(args, repo):
    if args.due:
        task = DeadlineTask(args.title, args.due)
    elif args.priority:
        task = PriorityTask(args.title, args.priority)
    else:
        task = Task(args.title)
    run(AddTaskCommand(repo, task))

    console.print(f"[{theme.done_color}]Added task:[/] {task}")
    EventBus.publish(TaskEvent('created', task.id, task.title))


def handle_list(args, repo):
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

    for task in filtered:
        done = f"[{theme.done_color}]done[/]" if task.done else f"[{theme.pending_color}]todo[/]"
        extra = ""

        if isinstance(task, DeadlineTask):
            col = theme.overdue_color if task.is_overdue() else theme.pending_color
            extra = f"[{col}]{task.due_date}[/]"

        elif isinstance(task, PriorityTask):
            extra = f"[{theme.priority_color}]{ '*' * task.priority }[/]"

        table.add_row(
            str(task.id),
            done,
            task.title,
            type(task).__name__,
            extra
        )

    console.print(table)
    done_n = sum(1 for t in filtered if t.done)
    console.print(f"[dim]{done_n}/{len(filtered)} complete[/]")
    

def handle_done(args, repo):
    task= repo.get_by_id(args.id)
    if not  task:
        console.print(f"[red]Task with ID {args.id} not found[/]")
        return
    if task.done:
        console.print(f"[yellow]Task with ID {args.id} is already marked as done[/]")
        return
    run(CompleteTaskCommand(repo, task.id))  

    console.print(f"[{theme.done_color}]Task marked as done:[/] {task}")
    EventBus.publish(TaskEvent('completed', task.id, task.title))


def handle_delete(args, repo):
    try:
        run(DeleteTaskCommand(repo, args.id))
        EventBus.publish(TaskEvent('deleted', args.id, "Task deleted"))
        console.print(f"[{theme.done_color}]Deleted task with ID {args.id}[/]")
    except Exception as e:
        console.print(f"[red]Error deleting task with ID {args.id}: {e}[/]")





def handle_interactive(args, repo):
    while True:
        console.clear()
        tasks = repo.get_all()  # avoid repeated calls

        # === Rich Table ===
        table = Table(title="TaskMan Interactive",
                      box=getattr(box, theme.border_style),
                      header_style=theme.header_color)
        table.add_column("ID", justify="center", width=4)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Title", min_width=20)
        table.add_column("Type", justify="center", width=14)
        table.add_column("Extra", justify="center", width=16)

        for task in tasks:
            if isinstance(task, DeadlineTask):
                extra = f"[{theme.overdue_color}]{task.due_date}[/]" if task.is_overdue() else f"[{theme.pending_color}]{task.due_date}[/]"
            elif isinstance(task, PriorityTask):
                extra = f"[{theme.priority_color}]{ '*' * task.priority }[/]"
            else:
                extra = ""
            status = f"[{theme.done_color}]done[/]" if task.done else f"[{theme.pending_color}]todo[/]"
            table.add_row(str(task.id), status, task.title or "", type(task).__name__, extra)

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

        choices += ["Add new task", "Quit"]
        choices += ["Undo last action"]


        # === Ask user via arrow keys ===
        answer = questionary.select("Select a task or action:", choices=choices, qmark="➡").ask()

        if answer in (None, "Quit"):
            break
        elif answer == "Add new task":
            title = questionary.text("Task title:").ask()
            if title:
                p = questionary.text("Priority (1-5, leave empty for none):").ask()
                due = questionary.text("Deadline (YYYY-MM-DD, leave empty for none):").ask()
                if due:
                    task = DeadlineTask(title, due)
                elif p.isdigit():
                    task = PriorityTask(title, int(p))
                else:
                    task = Task(title)
                run(AddTaskCommand(repo, task)) 
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
                run(CompleteTaskCommand(repo, task.id))
            elif action == "Delete":
                run(DeleteTaskCommand(repo, task.id))





def handle_stats(args, repo):
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



def handle_repair(args, repo=None):
    """Restore the latest backup of tasks.json"""
    backups = sorted(DATA_FILE.parent.glob("*.bak"))

    if not backups:
        console.print("[yellow]No backups found.[/]")
        return

    latest = backups[-1]

    try:
        shutil.copy(latest, DATA_FILE)
        console.print(f"[green]Restored from {latest.name}[/]")
    except Exception as e:
        console.print(f"[red]Failed to restore backup: {e}[/]")

    if repo:
        repo.get_all()  




def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    parser.add_argument("--verbose", action="store_true", help="Show animated progress when loading tasks")

    subparsers = parser.add_subparsers(dest="command")

    # add command
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("title")
    parser_add.add_argument("--due", help="Deadline YYYY-MM-DD")
    parser_add.add_argument("--priority", type=int, help="Priority level")

    # list command
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--filter", choices=["all", "done", "pending"], default="all")
    parser_list.add_argument("--sort", choices=["priority", "due", "title"], help="Sort tasks by specified criteria")
    # done command
    parser_done = subparsers.add_parser("done")
    parser_done.add_argument("id", type=int)

    # delete command
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("id", type=int)

    # interactive command
    parser_interactive = subparsers.add_parser("interactive")

    # stats command
    parser_stats = subparsers.add_parser("stats")

    repair_parser = subparsers.add_parser("repair", help="Restore latest backup")

    parser_undo = subparsers.add_parser("undo", help="Undo last action")


    parser_config = subparsers.add_parser("config", help="Manage config settings")
    parser_config.add_argument("--set", help="Set a config key=value")

    args = parser.parse_args()
    repo = JsonTaskRepo(DATA_FILE)  
    existing_tasks = repo.get_all()
    if existing_tasks:
        Task.count = max(t.id for t in existing_tasks) + 1
    else:
        Task.count = 0


    if args.command == "repair":
        handle_repair(args,None)
        return

    if args.command == "config" and args.set:
        handle_config_set(args, None)
        return

    if args.command == "undo":
        undo_last()
        return



    if args.command == "add":
        handle_add(args, repo)
    elif args.command == "list":
        handle_list(args, repo)
    elif args.command == "done":
        handle_done(args, repo)
    elif args.command == "delete":
        handle_delete(args, repo)
    elif args.command == "stats":
        handle_stats(args, repo)
    elif args.command == "interactive":
        handle_interactive(args, repo)
    else:
        parser.print_help()



