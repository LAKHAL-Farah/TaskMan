import re 
from datetime import datetime
from .exceptions import ValidationError

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def validate_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise ValidationError("Title cannot be empty.")
    if len(title) > 200:
        raise ValidationError("Title cannot exceed 200 characters.")
    return title

def validate_due_date(due_date: str) -> str:
    if not DATE_RE.match(due_date):
        raise ValidationError("Due date must be in YYYY-MM-DD format.")
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Due date is not a valid calendar date.")
    return due_date

def validate_priority(p:int) -> int:
    if not  1<= p <= 5:
        raise ValidationError("Priority must be an integer between 1 and 5.")
    return p