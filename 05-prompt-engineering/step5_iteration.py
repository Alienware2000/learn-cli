"""
Step 5: Iterating on Prompts

Prompt engineering is an iterative process:
1. Write a prompt
2. Test it
3. See what's wrong
4. Improve it
5. Repeat!

This file shows common issues and how to fix them.

Run with:
    python step5_iteration.py

Note: Requires ANTHROPIC_API_KEY environment variable
"""

import os
import json
from anthropic import Anthropic

client = Anthropic()


# ============================================================
# VERSION 1: Too vague - Claude might not give JSON
# ============================================================
PROMPT_V1 = """Help break down tasks into steps."""


# ============================================================
# VERSION 2: Asks for JSON but format isn't specified
# ============================================================
PROMPT_V2 = """You are a task planning assistant.
Always respond in JSON format."""


# ============================================================
# VERSION 3: Specifies format but Claude might add extra text
# ============================================================
PROMPT_V3 = """You are a task planning assistant.

Respond in this JSON format:
{
    "steps": [{"title": "...", "description": "..."}]
}
"""


# ============================================================
# VERSION 4: Much better! Clear, specific, with examples
# ============================================================
PROMPT_V4 = """You are a task planning assistant that breaks down tasks into actionable steps.

CRITICAL: Respond with ONLY valid JSON. No markdown, no explanation, no extra text.

Use this exact format:
{
    "task": "the original task description",
    "step_count": 5,
    "steps": [
        {
            "number": 1,
            "title": "Short title under 50 chars",
            "description": "2-3 sentences explaining this step",
            "is_optional": false
        }
    ]
}

Rules:
- Always include 3-7 steps
- Make steps specific and actionable
- First step should be the easiest to start
- Mark optional steps with is_optional: true
"""


def test_prompt(prompt_name: str, system_prompt: str, task: str):
    """Test a prompt and show results."""
    print(f"\n{'='*60}")
    print(f"Testing: {prompt_name}")
    print(f"{'='*60}")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": task}]
    )

    text = response.content[0].text

    # Try to parse as JSON
    try:
        data = json.loads(text)
        print("✅ Valid JSON!")
        print(f"   Steps: {len(data.get('steps', []))}")

        # Check structure
        if 'steps' in data and len(data['steps']) > 0:
            step = data['steps'][0]
            has_number = 'number' in step
            has_title = 'title' in step
            has_desc = 'description' in step
            print(f"   Has number field: {'✅' if has_number else '❌'}")
            print(f"   Has title field: {'✅' if has_title else '❌'}")
            print(f"   Has description field: {'✅' if has_desc else '❌'}")

    except json.JSONDecodeError:
        print("❌ Not valid JSON")
        print(f"   Response preview: {text[:200]}...")


def main():
    task = "Learn to cook Italian food"

    print("\n" + "🔬 PROMPT ITERATION EXPERIMENT ".center(60, "="))
    print("\nWe'll test the same task with different prompt versions")
    print(f"Task: '{task}'")

    # Test each version
    test_prompt("V1 - Too Vague", PROMPT_V1, task)
    test_prompt("V2 - No Format Spec", PROMPT_V2, task)
    test_prompt("V3 - Basic Format", PROMPT_V3, task)
    test_prompt("V4 - Production Ready", PROMPT_V4, task)

    print("\n" + "="*60)
    print("LESSONS LEARNED")
    print("="*60)
    print("""
1. Be EXPLICIT about format
   Bad:  "Respond in JSON"
   Good: "Respond with ONLY valid JSON. No markdown, no extra text."

2. Show the EXACT structure
   Include a complete example of what you want

3. Add CONSTRAINTS
   - "3-7 steps"
   - "under 50 characters"
   - "2-3 sentences"

4. Handle edge cases
   - What if the task is vague?
   - What if it's too complex?
   - Add rules for these situations

5. TEST with different inputs
   - Simple tasks
   - Complex tasks
   - Ambiguous tasks
   - Edge cases
""")


if __name__ == "__main__":
    main()


# ============================================================
# PROMPT ENGINEERING TIPS:
#
# 1. Start Simple, Add Complexity
#    Don't try to write the perfect prompt first.
#    Start basic, test, improve.
#
# 2. Be Specific About Output Format
#    "Return JSON" is vague
#    "Return ONLY this exact JSON structure: {...}" is clear
#
# 3. Use Examples
#    Show Claude exactly what good output looks like
#
# 4. Add Constraints
#    Limits help Claude make decisions:
#    - "maximum 5 steps"
#    - "each description under 100 words"
#    - "difficulty must be: easy, medium, or hard"
#
# 5. Handle Edge Cases
#    What should happen if:
#    - Input is too vague?
#    - Task is impossible?
#    - Multiple interpretations exist?
#
# 6. Test Thoroughly
#    Try many different inputs
#    Look for failure modes
#    Refine based on real results
# ============================================================
