"""
Step 3: Validation - Making Rules for Your Data

Pydantic can enforce rules beyond just types:
- Minimum/maximum values
- String patterns
- Required vs optional fields
- Default values
"""

from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    # Required field - must provide it
    title: str = Field(
        min_length=1,           # Can't be empty
        max_length=100,         # Can't be too long
        description="The task title"
    )

    # Field with limited choices
    priority: str = Field(
        default="medium",        # If not provided, use this
        description="Task priority: low, medium, or high"
    )

    # Optional field - can be None
    due_date: Optional[str] = Field(
        default=None,
        description="When the task is due (optional)"
    )

    # Boolean with a default
    done: bool = Field(
        default=False,
        description="Whether the task is complete"
    )

    # Number with constraints
    estimated_hours: float = Field(
        default=1.0,
        ge=0,                    # Greater than or equal to 0
        le=100,                  # Less than or equal to 100
        description="Estimated hours to complete"
    )


print("=== Creating Tasks with Defaults ===\n")

# Only provide required field - others get defaults
minimal_task = Task(title="Quick task")
print("Minimal task (only title provided):")
print(f"  title: {minimal_task.title}")
print(f"  priority: {minimal_task.priority} (default)")
print(f"  due_date: {minimal_task.due_date} (default)")
print(f"  done: {minimal_task.done} (default)")
print(f"  estimated_hours: {minimal_task.estimated_hours} (default)")


print("\n=== Providing All Fields ===\n")

full_task = Task(
    title="Big project",
    priority="high",
    due_date="2024-12-31",
    done=False,
    estimated_hours=40.0
)
print(f"Full task: {full_task}")


print("\n=== Testing Validation Rules ===\n")

# Empty title (violates min_length=1)
print("Attempt 1: Empty title")
try:
    Task(title="")
except Exception as e:
    print(f"  CAUGHT! Title must have at least 1 character")

# Title too long (violates max_length=100)
print("\nAttempt 2: Title too long (150 characters)")
try:
    Task(title="x" * 150)
except Exception as e:
    print(f"  CAUGHT! Title must be 100 characters or less")

# Negative hours (violates ge=0)
print("\nAttempt 3: Negative estimated hours")
try:
    Task(title="Test", estimated_hours=-5)
except Exception as e:
    print(f"  CAUGHT! Hours must be >= 0")

# Too many hours (violates le=100)
print("\nAttempt 4: Too many estimated hours (500)")
try:
    Task(title="Test", estimated_hours=500)
except Exception as e:
    print(f"  CAUGHT! Hours must be <= 100")


print("\n" + "="*50)
print("FIELD OPTIONS:")
print("- default=value → Use this if not provided")
print("- min_length/max_length → For strings")
print("- ge (>=), le (<=), gt (>), lt (<) → For numbers")
print("- Optional[type] → Field can be None")
print("- description → Documents what the field is for")
print("="*50)
