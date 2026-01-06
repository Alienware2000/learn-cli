"""
Step 4: Template Variables in Prompts

Real applications need dynamic prompts that change based on:
- User preferences
- Application state
- Different use cases

Python f-strings and .format() make this easy!

Run with:
    python step4_templates.py

Note: Requires ANTHROPIC_API_KEY environment variable
"""

import os
import json
from anthropic import Anthropic

client = Anthropic()


# Template with placeholders
SYSTEM_TEMPLATE = """You are a {role} assistant helping with {domain} tasks.

Your communication style should be: {style}

Always respond with valid JSON in this format:
{{
    "task": "the original task",
    "category": "{domain}",
    "steps": [
        {{"number": 1, "title": "...", "description": "..."}}
    ],
    "tips": ["helpful tip 1", "helpful tip 2"]
}}

{extra_instructions}
"""


def create_system_prompt(
    role: str = "helpful",
    domain: str = "general",
    style: str = "friendly and concise",
    extra_instructions: str = ""
) -> str:
    """Create a customized system prompt from template."""
    return SYSTEM_TEMPLATE.format(
        role=role,
        domain=domain,
        style=style,
        extra_instructions=extra_instructions
    )


def get_task_breakdown(task: str, system_prompt: str) -> dict:
    """Get task breakdown with custom system prompt."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": task}
        ]
    )

    text = response.content[0].text

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}


def print_result(result: dict):
    """Pretty print the result."""
    if not result:
        print("No result!")
        return

    print(f"\n📋 Task: {result.get('task', 'Unknown')}")
    print(f"📁 Category: {result.get('category', 'Unknown')}")
    print(f"\n📝 Steps:")

    for step in result.get("steps", []):
        print(f"  {step['number']}. {step['title']}")

    if result.get("tips"):
        print(f"\n💡 Tips:")
        for tip in result["tips"]:
            print(f"  • {tip}")


def main():
    # Example 1: Cooking domain with chef personality
    print("=" * 60)
    print("EXAMPLE 1: Cooking Assistant")
    print("=" * 60)

    cooking_prompt = create_system_prompt(
        role="professional chef",
        domain="cooking",
        style="warm and encouraging, like a cooking show host",
        extra_instructions="Include estimated cooking times. Assume beginner skill level."
    )

    result = get_task_breakdown("Make homemade pasta", cooking_prompt)
    print_result(result)

    # Example 2: Fitness domain with trainer personality
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Fitness Assistant")
    print("=" * 60)

    fitness_prompt = create_system_prompt(
        role="personal trainer",
        domain="fitness",
        style="motivating and energetic",
        extra_instructions="Include safety warnings where relevant. Suggest beginner modifications."
    )

    result = get_task_breakdown("Start a morning workout routine", fitness_prompt)
    print_result(result)

    # Show the actual prompt
    print("\n" + "=" * 60)
    print("BEHIND THE SCENES - The Fitness Prompt:")
    print("=" * 60)
    print(fitness_prompt[:500] + "...")


if __name__ == "__main__":
    main()


# ============================================================
# KEY CONCEPTS:
#
# 1. Template Variables
#    Use {placeholder} in strings, fill with .format()
#
#    template = "Hello {name}!"
#    result = template.format(name="Alice")  # "Hello Alice!"
#
# 2. Escaping Braces
#    In JSON templates, use {{ and }} for literal braces
#    {variable} = placeholder
#    {{literal}} = actual { in output
#
# 3. Why Templates?
#    - One template, many use cases
#    - Easy to customize behavior
#    - User preferences can modify prompts
#    - A/B testing different prompts
#
# 4. Real-World Uses
#    - Different personas (teacher, coach, expert)
#    - Different domains (cooking, fitness, coding)
#    - Different output formats (brief, detailed)
#    - User-selected preferences
# ============================================================
