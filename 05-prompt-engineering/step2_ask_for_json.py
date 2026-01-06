"""
Step 2: Asking for JSON in the Prompt

The simplest fix: Just ask Claude to respond in JSON!

Run with:
    python step2_ask_for_json.py

Note: Requires ANTHROPIC_API_KEY environment variable
"""

import os
import json
from anthropic import Anthropic

client = Anthropic()


def get_task_breakdown(task: str) -> dict:
    """Ask Claude to break down a task and return JSON."""

    # The key is in the prompt - we ask for JSON!
    prompt = f"""Break down this task into steps: {task}

Respond with ONLY valid JSON in this exact format:
{{
    "task": "the original task",
    "steps": [
        {{"number": 1, "title": "Step title", "description": "What to do"}},
        {{"number": 2, "title": "Step title", "description": "What to do"}}
    ]
}}

No other text, just the JSON."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Get the text response
    text = response.content[0].text

    # Parse it as JSON
    try:
        data = json.loads(text)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw response: {text}")
        return {}


def main():
    task = "Build a personal website"

    print(f"Task: {task}")
    print("-" * 50)

    result = get_task_breakdown(task)

    # Now we can work with structured data!
    if result:
        print(f"\nParsed {len(result.get('steps', []))} steps:\n")

        for step in result.get("steps", []):
            print(f"  {step['number']}. {step['title']}")
            print(f"     {step['description']}\n")

        print("-" * 50)
        print("\nNOW WE CAN:")
        print(f"  - Count steps: {len(result['steps'])}")
        print(f"  - Get first step: {result['steps'][0]['title']}")
        print(f"  - Loop through steps programmatically")
        print(f"  - Save to database, convert to other formats, etc.")


if __name__ == "__main__":
    main()


# ============================================================
# KEY INSIGHT:
#
# By asking for JSON in a specific format, Claude will
# (usually) respond with parseable JSON.
#
# This works but has issues:
# 1. Sometimes Claude adds "Here's the JSON:" before it
# 2. Sometimes it uses markdown code blocks
# 3. The prompt is getting long and messy
#
# Next step: Use system prompts to make this cleaner!
# ============================================================
