import argparse
import questionary
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns 

from taskman.models import Task, DeadlineTask, PriorityTask
from taskman.storage import load_tasks, save_tasks


console = Console()
def handle_add(args,tasks):
    if args.due:
        task = DeadlineTask(args.title, args.due)
    elif args.priority:
        task = PriorityTask(args.title, args.priority)
    else:
        task = Task(args.title)
    tasks.append(task)
    save_tasks(tasks)

    console.print(f"[green]Added task:[/] {task}")


def handle_list(args, tasks):

    filtered = {
        'done': [t for t in tasks if t.done],
        'pending': [t for t in tasks if not t.done],
        'all': tasks
    }[args.filter]

    if not filtered:
        console.print("[yellow]No tasks to show[/]")
        return

    table = Table(
        box=box.ROUNDED,
        header_style="bold purple"
    )

    table.add_column("ID", width=4)
    table.add_column("Status", width=8)
    table.add_column("Title", min_width=22)
    table.add_column("Type", width=14)
    table.add_column("Extra", width=16)

    for task in filtered:

        done = "[green]done[/]" if task.done else "[dim]todo[/]"
        extra = ""

        if isinstance(task, DeadlineTask):
            col = "red" if task.is_overdue() else "yellow"
            extra = f"[{col}]{task.due_date}[/]"

        elif isinstance(task, PriorityTask):
            extra = "[magenta]" + "*" * task.priority + "[/]"

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


def handle_done(args, tasks):
    task = next((t for t in tasks if t.id == args.id), None)
    if not  task:
        console.print(f"[red]Task with ID {args.id} not found[/]")
        return
    task.complete()
    save_tasks(tasks)
    console.print(f"[green]Task marked as done:[/] {task}")


def handle_delete(args, tasks):
    before = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == before:
        console.print(f"[red]Task with ID {args.id} not found[/]")
        return
    save_tasks(tasks)
    console.print(f"[green]Deleted task with ID {args.id}[/]")




def handle_interactive(args, tasks):
    while True:
        console.clear()

        # === Rich Table ===
        table = Table(title="TaskMan Interactive", box=box.ROUNDED, header_style="bold cyan")
        table.add_column("ID", justify="center", width=4)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Title", min_width=20)
        table.add_column("Type", justify="center", width=14)
        table.add_column("Extra", justify="center", width=16)

        for task in tasks:
            if isinstance(task, DeadlineTask):
                extra = f"[red]{task.due_date}[/]" if task.is_overdue() else f"[yellow]{task.due_date}[/]"
            elif isinstance(task, PriorityTask):
                extra = "[magenta]" + "*" * task.priority + "[/]"
            else:
                extra = ""
            status = "[green]done[/]" if task.done else "[white]todo[/]"
            table.add_row(str(task.id), status, task.title or "", type(task).__name__, extra)

        console.print(table)
        console.print(f"[dim]{sum(1 for t in tasks if t.done)}/{len(tasks)} complete[/]\n")

        # === Build arrow-key menu with mapping ===
        menu_map = {}  # map menu string → Task
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

        # === Ask user via arrow keys ===
        answer = questionary.select("Select a task or action:", choices=choices, qmark="➡").ask()

        if answer in (None, "Quit"):
            break
        elif answer == "Add new task":
            title = questionary.text("Task title:").ask()
            if title:
                # optional: ask for priority or due date
                p = questionary.text("Priority (1-5, leave empty for none):").ask()
                due = questionary.text("Deadline (YYYY-MM-DD, leave empty for none):").ask()
                if due:
                    task = DeadlineTask(title, due)
                elif p.isdigit():
                    task = PriorityTask(title, int(p))
                else:
                    task = Task(title)
                tasks.append(task)
                save_tasks(tasks)
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
                task.complete()
                save_tasks(tasks)
            elif action == "Delete":
                tasks[:] = [t for t in tasks if t.id != task.id]
                save_tasks(tasks)


def handle_stats(args, tasks):
    total = len(tasks)
    done = sum(1 for t in tasks if t.done)
    overdue = sum (1 for t in tasks if isinstance(t,DeadlineTask) and t.is_overdue() and not t.done)

    pct = int (done / total * 100) if total else 0

    by_type = {
        'Task': sum(1 for t in tasks if type(t).__name__ == "Task"),
        'DeadlineTask': sum(1 for t in tasks if isinstance(t, DeadlineTask)),
        'PriorityTask': sum(1 for t in tasks if isinstance(t, PriorityTask))
    }
    body = (f"[bold]{total}[/] total [green]{done}[/] done [red]{overdue}[/] overdue [purple]{pct}%[/]\n")

    for kind, count in by_type.items():
        body += f"[cyan]{kind}[/]: {count}\n"
    console.print(Panel(body, title="TaskMan Stats", box=box.DOUBLE))




def main():
    
    tasks = load_tasks()
    
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # add command
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("title")
    parser_add.add_argument("--due", help="Deadline YYYY-MM-DD")
    parser_add.add_argument("--priority", type=int, help="Priority level")
    
    # list command
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--filter", choices=["all","done","pending"], default="all")
    
    # done command
    parser_done = subparsers.add_parser("done")
    parser_done.add_argument("id", type=int)
    
    # delete command
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("id", type=int)


    parser_interactive = subparsers.add_parser("interactive")

    parser_stats = subparsers.add_parser("stats")

    args = parser.parse_args()
    
    if args.command == "add":
        handle_add(args, tasks)
    elif args.command == "list":
        handle_list(args, tasks)
    elif args.command == "done":
        handle_done(args, tasks)
    elif args.command == "delete":
        handle_delete(args, tasks)
    elif args.command == "stats":
        handle_stats(args, tasks)
    elif args.command == "interactive":
        handle_interactive(args, tasks)
    else:
        parser.print_help()