"""
Step 1: The Problem - Life Without Pydantic

When you're just using dictionaries, things get messy fast.
Run this file to see what can go wrong.
"""

# Let's say we're building a task tracker.
# We represent tasks as dictionaries:

task1 = {
    "title": "Buy groceries",
    "priority": "high",
    "done": False
}

task2 = {
    "title": "Call mom",
    "priority": "medium",
    "done": False
}

# This works fine... until someone makes a typo:

task3 = {
    "titel": "Fix bug",      # Oops! "titel" instead of "title"
    "priority": "high",
    "done": False
}

# Or uses the wrong type:

task4 = {
    "title": "Write report",
    "priority": 1,            # Number instead of string!
    "done": "no"              # String instead of boolean!
}

# Or forgets a field:

task5 = {
    "title": "Go to gym"
    # Missing priority and done!
}


# Now let's try to use these tasks...

def print_task(task):
    """Print a task nicely."""
    status = "DONE" if task["done"] else "TODO"
    print(f"[{status}] {task['title']} (Priority: {task['priority']})")


print("=== Printing Tasks ===\n")

# These work:
print("Task 1:")
print_task(task1)

print("\nTask 2:")
print_task(task2)

# This crashes with a confusing error:
print("\nTask 3 (with typo):")
try:
    print_task(task3)
except KeyError as e:
    print(f"  ERROR: KeyError - {e}")
    print("  The key 'title' doesn't exist because someone typed 'titel'")

# This might work but gives weird output:
print("\nTask 4 (wrong types):")
try:
    print_task(task4)
    print("  ^ This ran, but the output is wrong! 'done' should be True/False")
except Exception as e:
    print(f"  ERROR: {e}")

# This crashes:
print("\nTask 5 (missing fields):")
try:
    print_task(task5)
except KeyError as e:
    print(f"  ERROR: KeyError - {e}")
    print("  Missing required fields!")


print("\n" + "="*50)
print("THE PROBLEM:")
print("- Typos in keys aren't caught until runtime")
print("- Wrong types aren't caught at all")
print("- Missing fields crash later, not when created")
print("- No autocomplete in your editor")
print("="*50)
print("\nPydantic solves all of these. See step2!")
