# TaskMan CLI
> A command-line task manager built with Python OOP, argparse, and JSON persistence.
## Features
- Add plain tasks, tasks with deadlines, or priority tasks
- List tasks with filters: all / done / pending
- Mark tasks complete, delete tasks
- Colour-coded terminal output (colorama)
- Tasks persist between sessions (JSON file in ~/.taskman/)
## Usage
```bash
python main.py add 'Buy milk'
python main.py add 'Submit report' --due 2026-04-01
python main.py add 'Fix bug' --priority 5
python main.py list
python main.py list --filter pending
python main.py done 0
python main.py delete 1
```
## Architecture
| File | Responsibility |
|------|----------------|
| models.py | Task, DeadlineTask, PriorityTask classes |
| storage.py | JSON load/save (only file touching disk) |
| cli.py | argparse + command handlers |
| main.py | Entry point |