"""
Step 4: Nested Models - Models Inside Models

Real data is often hierarchical:
- A TaskList contains multiple Tasks
- A User has an Address
- An Order has multiple Items

Pydantic handles this naturally.
"""

from pydantic import BaseModel, Field
from enum import Enum


# First, let's define an Enum for priority
# Enums are a way to define a fixed set of choices
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# A simple Task model
class Task(BaseModel):
    title: str
    priority: Priority = Priority.MEDIUM
    done: bool = False


# A TaskList that CONTAINS multiple Tasks
class TaskList(BaseModel):
    name: str = Field(description="Name of this task list")
    tasks: list[Task] = Field(default_factory=list)  # List of Task objects!

    def count_done(self) -> int:
        """Count how many tasks are done."""
        return sum(1 for task in self.tasks if task.done)

    def count_pending(self) -> int:
        """Count how many tasks are pending."""
        return sum(1 for task in self.tasks if not task.done)


print("=== Creating Nested Models ===\n")

# Create a task list with some tasks
my_list = TaskList(
    name="Weekend Errands",
    tasks=[
        Task(title="Buy groceries", priority=Priority.HIGH),
        Task(title="Call mom", priority=Priority.MEDIUM, done=True),
        Task(title="Clean room", priority=Priority.LOW),
        Task(title="Fix bike", priority=Priority.HIGH, done=True),
    ]
)

print(f"Task List: {my_list.name}")
print(f"Total tasks: {len(my_list.tasks)}")
print(f"Done: {my_list.count_done()}")
print(f"Pending: {my_list.count_pending()}")

print("\nAll tasks:")
for i, task in enumerate(my_list.tasks, 1):
    status = "✓" if task.done else " "
    print(f"  {i}. [{status}] {task.title} ({task.priority.value})")


print("\n=== Why Enums? ===\n")

# With Enum, only valid priorities are allowed
print("Attempt: Invalid priority 'super-high'")
try:
    bad_task = Task(title="Test", priority="super-high")
except Exception as e:
    print(f"  CAUGHT! 'super-high' is not a valid Priority")
    print(f"  Valid choices: {[p.value for p in Priority]}")


print("\n=== Deeper Nesting ===\n")


# You can nest as deep as you need
class Address(BaseModel):
    street: str
    city: str
    country: str = "USA"


class Person(BaseModel):
    name: str
    age: int
    address: Address  # Nested model!


class Team(BaseModel):
    team_name: str
    members: list[Person]  # List of nested models!


# Create a team
dev_team = Team(
    team_name="Backend Team",
    members=[
        Person(
            name="Alice",
            age=30,
            address=Address(street="123 Main St", city="Boston")
        ),
        Person(
            name="Bob",
            age=25,
            address=Address(street="456 Oak Ave", city="Seattle")
        ),
    ]
)

print(f"Team: {dev_team.team_name}")
for member in dev_team.members:
    print(f"  - {member.name}, {member.age}, lives in {member.address.city}")


print("\n" + "="*50)
print("KEY CONCEPTS:")
print("- Models can contain other models (nesting)")
print("- Use list[Model] for lists of models")
print("- Enums (str, Enum) restrict values to valid choices")
print("- default_factory=list creates a new empty list each time")
print("- You can add methods to models (like count_done)")
print("="*50)
