"""
Step 3: System Prompts

System prompts set the "personality" and rules for Claude.
They're processed BEFORE the user's message.

Think of it like:
- System prompt = The job description for Claude
- User message = The actual task to do

Run with:
    python step3_system_prompt.py

Note: Requires ANTHROPIC_API_KEY environment variable
"""

import os
import json
from anthropic import Anthropic

client = Anthropic()

# The system prompt defines HOW Claude should behave
SYSTEM_PROMPT = """You are a task planning assistant. Your job is to break down tasks into clear, actionable steps.

IMPORTANT RULES:
1. Always respond with valid JSON only - no other text
2. Use this exact format:
{
    "task": "the original task",
    "estimated_time": "total time estimate",
    "difficulty": "easy|medium|hard",
    "steps": [
        {
            "number": 1,
            "title": "Short step title",
            "description": "Detailed explanation",
            "time": "time for this step"
        }
    ]
}

3. Be specific and actionable
4. Include time estimates
5. Keep step titles short (under 50 characters)
"""


def get_task_breakdown(task: str) -> dict:
    """Ask Claude to break down a task using system prompt."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,  # <-- System prompt goes here!
        messages=[
            # Now the user message can be simple
            {"role": "user", "content": task}
        ]
    )

    text = response.content[0].text

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON if there's extra text
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}


def main():
    task = "Learn to play guitar"

    print(f"Task: {task}")
    print("=" * 50)

    result = get_task_breakdown(task)

    if result:
        print(f"\n📋 Task: {result.get('task', task)}")
        print(f"⏱️  Estimated time: {result.get('estimated_time', 'Unknown')}")
        print(f"📊 Difficulty: {result.get('difficulty', 'Unknown')}")
        print(f"\n📝 Steps ({len(result.get('steps', []))} total):\n")

        for step in result.get("steps", []):
            print(f"  {step['number']}. {step['title']}")
            print(f"     {step['description']}")
            print(f"     ⏰ {step.get('time', 'N/A')}\n")


if __name__ == "__main__":
    main()


# ============================================================
# KEY CONCEPTS:
#
# 1. System Prompt
#    - Sent BEFORE user messages
#    - Sets behavior, rules, output format
#    - Not visible to user (in a chat interface)
#    - Perfect for defining JSON schemas
#
# 2. Why System Prompts?
#    - Separates "how to respond" from "what to respond to"
#    - Cleaner user messages
#    - More consistent behavior
#    - Can define complex output formats once
#
# 3. The API call:
#    client.messages.create(
#        model="...",
#        system=SYSTEM_PROMPT,  # <-- System prompt
#        messages=[...]         # <-- User messages
#    )
# ============================================================
