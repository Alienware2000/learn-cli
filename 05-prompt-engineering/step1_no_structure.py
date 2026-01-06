"""
Step 1: The Problem - Unstructured Responses

When you ask Claude a question, it responds in natural language.
This is great for humans, but hard for code to parse!

Run with:
    python step1_no_structure.py

Note: Requires ANTHROPIC_API_KEY environment variable
"""

import os
from anthropic import Anthropic

# Create the client
client = Anthropic()


def get_task_breakdown(task: str) -> str:
    """Ask Claude to break down a task."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"Break down this task into steps: {task}"
            }
        ]
    )

    return response.content[0].text


def main():
    task = "Build a personal website"

    print(f"Task: {task}")
    print("-" * 50)

    result = get_task_breakdown(task)
    print(result)

    print("-" * 50)
    print("\nTHE PROBLEM:")
    print("This response is nice to read, but how would your code:")
    print("  - Count the number of steps?")
    print("  - Extract just the step titles?")
    print("  - Save each step to a database?")
    print("  - Display steps in a different format?")
    print("\nYou'd have to write complex parsing logic!")
    print("Every time Claude changes its formatting, your parser breaks.")


if __name__ == "__main__":
    main()


# ============================================================
# THE PROBLEM:
#
# Claude's response might look like:
#
#   "Here's how to build a personal website:
#
#    1. Choose a domain name
#       First, think about what you want...
#
#    2. Select a hosting provider
#       There are many options like..."
#
# But it could also be:
#
#   "To build a personal website, you'll need to:
#    - Pick a domain
#    - Find hosting
#    - Design your site..."
#
# Or even:
#
#   "Building a website involves several key steps.
#    The first thing you should do is..."
#
# Every format is different! Parsing this is a nightmare.
# ============================================================
