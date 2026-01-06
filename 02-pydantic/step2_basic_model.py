"""
Step 2: Your First Pydantic Model

A Pydantic model is like a dictionary, but:
- It validates data automatically
- It catches errors immediately
- Your editor can autocomplete fields
"""

from pydantic import BaseModel


# Define a "shape" for our task data
class Task(BaseModel):
    title: str        # Must be a string
    priority: str     # Must be a string
    done: bool        # Must be True or False


# Now let's create some tasks...

print("=== Creating Valid Tasks ===\n")

# This works perfectly:
task1 = Task(
    title="Buy groceries",
    priority="high",
    done=False
)
print(f"Task 1: {task1}")
print(f"  Title: {task1.title}")      # Access with dot notation!
print(f"  Priority: {task1.priority}")
print(f"  Done: {task1.done}")


print("\n=== Trying Invalid Tasks ===\n")

# What happens with a typo?
print("Attempt 1: Typo in field name ('titel' instead of 'title')")
try:
    bad_task = Task(
        titel="Fix bug",  # Typo!
        priority="high",
        done=False
    )
except Exception as e:
    print(f"  CAUGHT! {type(e).__name__}")
    print(f"  Pydantic immediately tells us 'titel' is not a valid field")

# What happens with wrong type?
print("\nAttempt 2: Wrong type (number instead of string for priority)")
try:
    bad_task = Task(
        title="Write report",
        priority=1,  # Number, not string!
        done=False
    )
    # Actually, Pydantic is smart - it converts 1 to "1"!
    print(f"  Interesting: Pydantic converted 1 to '{bad_task.priority}'")
except Exception as e:
    print(f"  CAUGHT! {e}")

# What about a truly wrong type?
print("\nAttempt 3: Wrong type (string 'yes' for done, which needs True/False)")
try:
    bad_task = Task(
        title="Go to gym",
        priority="low",
        done="yes"  # Should be True or False!
    )
except Exception as e:
    print(f"  CAUGHT! {type(e).__name__}")
    print(f"  Pydantic says: 'yes' is not a valid boolean")

# What about missing fields?
print("\nAttempt 4: Missing required field")
try:
    bad_task = Task(
        title="Incomplete task"
        # Missing priority and done!
    )
except Exception as e:
    print(f"  CAUGHT! {type(e).__name__}")
    print(f"  Pydantic lists exactly which fields are missing")


print("\n" + "="*50)
print("WHAT WE LEARNED:")
print("- Define a class that inherits from BaseModel")
print("- Add fields with type hints (name: type)")
print("- Pydantic validates data when you create an instance")
print("- Errors are caught immediately, with clear messages")
print("- Access fields with dot notation (task.title)")
print("="*50)
