"""
Step 5: JSON Conversion - The Magic of Pydantic

This is where Pydantic really shines for AI applications.

Claude responds with text (often JSON). Pydantic can:
1. Parse JSON into validated Python objects
2. Convert Python objects back to JSON

This is EXACTLY how we handle Claude's responses in the real project!
"""

from pydantic import BaseModel, Field
from enum import Enum
import json


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    title: str
    priority: Priority = Priority.MEDIUM
    done: bool = False
    estimated_hours: float | None = None


class TaskPlan(BaseModel):
    plan_name: str
    tasks: list[Task]
    total_hours: float | None = None


print("=== Python Object → JSON ===\n")

# Create a Python object
my_plan = TaskPlan(
    plan_name="Build a Website",
    tasks=[
        Task(title="Design mockups", priority=Priority.HIGH, estimated_hours=4.0),
        Task(title="Write HTML", priority=Priority.MEDIUM, estimated_hours=2.0),
        Task(title="Add CSS styling", priority=Priority.MEDIUM, estimated_hours=3.0),
    ],
    total_hours=9.0
)

# Convert to JSON string
json_string = my_plan.model_dump_json(indent=2)
print("JSON output:")
print(json_string)


print("\n=== JSON → Python Object ===\n")

# Imagine this JSON came from Claude's response
json_from_claude = '''
{
    "plan_name": "Learn Python",
    "tasks": [
        {"title": "Read tutorial", "priority": "low", "estimated_hours": 1.0},
        {"title": "Practice coding", "priority": "high", "estimated_hours": 5.0},
        {"title": "Build a project", "priority": "high", "estimated_hours": 10.0}
    ],
    "total_hours": 16.0
}
'''

# Parse it into a validated Python object
parsed_plan = TaskPlan.model_validate_json(json_from_claude)

print(f"Parsed plan: {parsed_plan.plan_name}")
print(f"Number of tasks: {len(parsed_plan.tasks)}")
for task in parsed_plan.tasks:
    print(f"  - {task.title} ({task.priority.value}): {task.estimated_hours}h")


print("\n=== Validation Still Works! ===\n")

# What if Claude returns bad JSON?
bad_json = '''
{
    "plan_name": "Bad Plan",
    "tasks": [
        {"title": "Valid task", "priority": "high"},
        {"title": "Bad task", "priority": "super-urgent"}
    ]
}
'''

print("Attempting to parse JSON with invalid priority:")
try:
    TaskPlan.model_validate_json(bad_json)
except Exception as e:
    print(f"  CAUGHT! Invalid data in JSON")
    print(f"  'super-urgent' is not a valid Priority")


print("\n=== Converting to Dict ===\n")

# Sometimes you need a dictionary instead of JSON string
my_dict = my_plan.model_dump()
print(f"Type: {type(my_dict)}")
print(f"Dict: {my_dict}")


print("\n=== From Dict to Object ===\n")

# Convert dict to object
some_dict = {
    "plan_name": "From Dict",
    "tasks": [
        {"title": "Task 1", "priority": "low"}
    ]
}

plan_from_dict = TaskPlan.model_validate(some_dict)
print(f"Created: {plan_from_dict.plan_name} with {len(plan_from_dict.tasks)} task(s)")


print("\n" + "="*50)
print("KEY METHODS:")
print("")
print("Python Object → JSON string:")
print("  obj.model_dump_json()      # Returns JSON string")
print("  obj.model_dump_json(indent=2)  # Pretty-printed")
print("")
print("JSON string → Python Object:")
print("  Model.model_validate_json(json_string)")
print("")
print("Python Object → Dict:")
print("  obj.model_dump()           # Returns dictionary")
print("")
print("Dict → Python Object:")
print("  Model.model_validate(dict)")
print("="*50)
print("")
print("THIS IS HOW WE HANDLE CLAUDE'S RESPONSES!")
print("Claude sends JSON → We parse it → We get validated Python objects")
