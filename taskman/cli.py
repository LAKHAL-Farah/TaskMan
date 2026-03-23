import argparse

from colorama import init, Fore, Style
from taskman.models import Task, DeadlineTask, PriorityTask
from taskman.storage import load_tasks, save_tasks

def handle_add(args,tasks):
    if args.due:
        task = DeadlineTask(args.title, args.due)
    elif args.priority:
        task = PriorityTask(args.title, args.priority)
    else:
        task = Task(args.title)
    tasks.append(task)
    save_tasks(tasks)
    print(Fore.GREEN + f"Added task: {task}" + Style.RESET_ALL)

def handle_list(args, tasks):
    filtered = {
        'done': [ t for t in tasks if t.done],
        'pending': [ t for t in tasks if not t.done],
        'all': tasks
    }[args.filter]
    if not filtered:
        print(Fore.YELLOW + "No tasks to show." + Style.RESET_ALL)
        return
    for task in filtered:
        color = Fore.GREEN if task.done else Fore.WHITE
        print(color + str(task) + Style.RESET_ALL)


def handle_done(args, tasks):
    task = next((t for t in tasks if t.id == args.id), None)
    if not  task:
        print(Fore.RED + f"Task with ID {args.id} not found." + Style.RESET_ALL)
        return
    task.complete()
    save_tasks(tasks)
    print(Fore.GREEN + f"Task marked as done: {task}" + Style.RESET_ALL)

def handle_delete(args, tasks):
    before = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == before:
        print(Fore.RED + f"Task with ID {args.id} not found." + Style.RESET_ALL)
        return
    save_tasks(tasks)
    print(Fore.GREEN + f"Deleted task with ID {args.id}." + Style.RESET_ALL)
        



def main():
    init(autoreset=True)  # colorama
    
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
    
    args = parser.parse_args()
    
    if args.command == "add":
        handle_add(args, tasks)
    elif args.command == "list":
        handle_list(args, tasks)
    elif args.command == "done":
        handle_done(args, tasks)
    elif args.command == "delete":
        handle_delete(args, tasks)
    else:
        parser.print_help()