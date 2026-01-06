"""
Step 2: Add user input.
Now the user can type their own task.
"""

import anthropic

# Automatically uses ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()

# NEW: Ask the user what they want to plan
task = input("What do you want to plan? ")

print(f"\nPlanning: {task}\n")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"Give me a short 3-step plan for: {task}"}
    ]
)

print(response.content[0].text)
