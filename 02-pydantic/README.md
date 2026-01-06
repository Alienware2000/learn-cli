# Module 2: Pydantic - Data Validation

## What You'll Learn

By the end of this module, you'll understand:
- Why dictionaries alone are problematic
- How to define data "shapes" with Pydantic models
- How validation catches errors early
- How to convert between Python objects and JSON

## Why Pydantic Matters for AI Apps

When Claude responds, it sends text - often JSON. Without Pydantic:
```python
response = '{"title": "Buy milk", "priority": "high"}'
data = json.loads(response)  # Just a dict - no validation!
print(data["titel"])  # Typo? Runtime crash!
```

With Pydantic:
```python
task = Task.model_validate_json(response)  # Validated!
print(task.title)  # Autocomplete works, typos caught
```

---

## Step 1: The Problem

**File:** `step1_without_pydantic.py`

```bash
python step1_without_pydantic.py
```

This shows what goes wrong with plain dictionaries:

| Problem | What Happens |
|---------|--------------|
| Typo in key (`titel`) | Crashes later with confusing KeyError |
| Wrong type (`done="yes"`) | Might work but give wrong behavior |
| Missing field | Crashes when you try to use it |

**Key Insight:** Errors happen far from where the mistake was made, making debugging hard.

---

## Step 2: Your First Pydantic Model

**File:** `step2_basic_model.py`

```python
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    priority: str
    done: bool
```

That's it! Now:

```python
# This works
task = Task(title="Buy milk", priority="high", done=False)
print(task.title)  # Access with dot notation

# This is caught IMMEDIATELY
task = Task(titel="Buy milk", ...)  # Error: unexpected field 'titel'
task = Task(title="Buy milk")       # Error: missing 'priority' and 'done'
```

### How It Works

1. Inherit from `BaseModel`
2. Define fields with type hints (`name: type`)
3. When you create an instance, Pydantic validates everything

---

## Step 3: Validation Rules

**File:** `step3_validation.py`

Use `Field()` to add constraints:

```python
from pydantic import BaseModel, Field
from typing import Optional

class Task(BaseModel):
    # Required, 1-100 characters
    title: str = Field(min_length=1, max_length=100)

    # Optional with default
    priority: str = Field(default="medium")

    # Can be None
    due_date: Optional[str] = Field(default=None)

    # Number between 0 and 100
    hours: float = Field(ge=0, le=100)
```

### Field Options

| Option | Meaning | Example |
|--------|---------|---------|
| `default=value` | Use if not provided | `default="medium"` |
| `min_length` | Minimum string length | `min_length=1` |
| `max_length` | Maximum string length | `max_length=100` |
| `ge` | Greater than or equal | `ge=0` (≥ 0) |
| `le` | Less than or equal | `le=100` (≤ 100) |
| `gt` | Greater than | `gt=0` (> 0) |
| `lt` | Less than | `lt=100` (< 100) |

### Optional Fields

```python
from typing import Optional

due_date: Optional[str] = None  # Can be a string OR None
```

---

## Step 4: Nested Models

**File:** `step4_nested_models.py`

Models can contain other models:

```python
class Task(BaseModel):
    title: str
    priority: str

class TaskList(BaseModel):
    name: str
    tasks: list[Task]  # List of Task objects!
```

Usage:
```python
my_list = TaskList(
    name="Shopping",
    tasks=[
        Task(title="Buy milk", priority="high"),
        Task(title="Buy bread", priority="low"),
    ]
)

for task in my_list.tasks:
    print(task.title)
```

### Enums for Fixed Choices

```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority  # Only LOW, MEDIUM, or HIGH allowed!
```

Why `str, Enum`? So `Priority.HIGH == "high"` is `True` (makes JSON work nicely).

---

## Step 5: JSON Conversion

**File:** `step5_json.py`

This is the magic for AI applications!

### Python → JSON

```python
task = Task(title="Buy milk", priority="high", done=False)

# To JSON string
json_str = task.model_dump_json()
# '{"title":"Buy milk","priority":"high","done":false}'

# Pretty-printed
json_str = task.model_dump_json(indent=2)
```

### JSON → Python

```python
json_from_claude = '{"title": "Buy milk", "priority": "high", "done": false}'

# Parse and validate in one step!
task = Task.model_validate_json(json_from_claude)
print(task.title)  # "Buy milk"
```

### Dict Conversion

```python
# To dict
d = task.model_dump()

# From dict
task = Task.model_validate({"title": "Test", "priority": "low", "done": True})
```

### Quick Reference

| Direction | Method |
|-----------|--------|
| Object → JSON string | `obj.model_dump_json()` |
| JSON string → Object | `Model.model_validate_json(str)` |
| Object → Dict | `obj.model_dump()` |
| Dict → Object | `Model.model_validate(dict)` |

---

## How This Connects to the Real Project

In `contextual-task-cli`, we use Pydantic exactly like this:

```python
# models.py
class Task(BaseModel):
    title: str
    description: str
    priority: Priority
    ...

class TaskPlan(BaseModel):
    title: str
    tasks: list[Task]
    ...

# conversation.py - parsing Claude's response
plan = TaskPlan.model_validate_json(claude_response)
```

Claude sends JSON → Pydantic validates it → We get clean Python objects.

---

## Summary

| Concept | What It Does |
|---------|--------------|
| `BaseModel` | Base class for validated data models |
| Type hints | Define what type each field should be |
| `Field()` | Add constraints and defaults |
| `Optional[T]` | Field can be `None` |
| `str, Enum` | Fixed set of valid string choices |
| Nested models | Models containing other models |
| `model_dump_json()` | Convert to JSON |
| `model_validate_json()` | Parse JSON into validated object |

## Key Vocabulary

| Term | Meaning |
|------|---------|
| **Model** | A class defining the shape of your data |
| **Validation** | Checking that data matches expected rules |
| **Serialization** | Converting objects to JSON/dict |
| **Deserialization** | Converting JSON/dict to objects |

---

## Exercises (Optional)

1. Create a `Book` model with title, author, pages (must be > 0), and an optional isbn
2. Create a `Library` model that contains a list of `Book` objects
3. Write JSON for a library with 3 books, then parse it with Pydantic
4. Try creating a book with -10 pages and see what happens

---

## What's Next?

In [Module 3: Environment Variables](../03-environment-variables/), you'll learn how to properly handle secrets like API keys - never hardcode them again!
