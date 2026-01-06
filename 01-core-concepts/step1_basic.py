"""
Step 1: The simplest possible version.
Just call the API and print what Claude says.
"""

import anthropic

# Your API key - set ANTHROPIC_API_KEY environment variable
# (We'll learn better ways to handle this in Module 3)
client = anthropic.Anthropic()  # Automatically uses ANTHROPIC_API_KEY env var

# The task we want help with
task = "Build a simple todo app"

# Call Claude
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"Give me a short 3-step plan for: {task}"}
    ]
)

# Print what Claude said
print(response.content[0].text)
