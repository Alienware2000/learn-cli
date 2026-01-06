"""
Step 3: Have a conversation.
Claude asks questions, we answer, back and forth.

KEY INSIGHT: Claude doesn't remember previous messages automatically.
We have to send the ENTIRE conversation history each time.
"""

import anthropic

# Automatically uses ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()

# This list stores all messages in the conversation
# We'll keep adding to it
messages = []

# Get the initial task
task = input("What do you want to plan? ")

# Add user's first message to history
messages.append({
    "role": "user",
    "content": f"I want to plan: {task}. Ask me ONE clarifying question."
})

# Have a 3-round conversation
for round in range(3):
    print(f"\n--- Round {round + 1} ---")

    # Send entire conversation history to Claude
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=messages  # <-- ALL messages, not just the last one!
    )

    # Get Claude's response
    claude_says = response.content[0].text
    print(f"\nClaude: {claude_says}")

    # Add Claude's response to history
    messages.append({
        "role": "assistant",
        "content": claude_says
    })

    # Get user's answer
    if round < 2:  # Don't ask on the last round
        user_says = input("\nYou: ")

        # Add user's answer to history
        messages.append({
            "role": "user",
            "content": user_says
        })

print("\n--- Conversation complete! ---")
print(f"Total messages exchanged: {len(messages)}")
