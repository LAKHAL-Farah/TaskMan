# tests/test_models.py
import pytest
from taskman.core import Task, DeadlineTask, PriorityTask
from datetime import datetime, timedelta

def test_task_creation():
    t = Task("Buy milk")
    assert t.title == "Buy milk"
    assert not t.done
    assert isinstance(t.id, int)

def test_task_complete():
    t = Task("Buy eggs")
    t.complete()
    assert t.done is True

def test_deadline_task_creation():
    due = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    dt = DeadlineTask("Submit report", due)
    assert dt.title == "Submit report"
    assert dt.due_date == due
    assert not dt.done
    # is_overdue should be False because due is tomorrow
    assert dt.is_overdue() is False

def test_priority_task_creation():
    pt = PriorityTask("Pay bills", priority=3)
    assert pt.title == "Pay bills"
    assert pt.priority == 3
    assert not pt.done

def test_task_str():
    t = Task("Test task")
    s = str(t)
    assert "[ ]" in s or "[X]" in s
    assert t.title in s

def test_task_repr():
    t = Task("Test task")
    r = repr(t)
    assert "Task" in r
    assert t.title in r