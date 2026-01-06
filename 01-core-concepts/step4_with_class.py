"""
Step 4: Use a class to organize the code.

WHY A CLASS?
- The conversation has "state" (messages, is_done, etc.)
- A class bundles the data AND the functions that work on it
- Makes the code cleaner and reusable

Think of a class like a "thing" that knows stuff and can do stuff.
"""

import anthropic


class SimpleConversation:
    """
    A simple conversation manager.

    It remembers:
    - The API client
    - All messages in the conversation
    - Whether we're done
    """

    def __init__(self):
        """
        __init__ runs when you create a new SimpleConversation.

        Example: conversation = SimpleConversation()
        """
        # Automatically uses ANTHROPIC_API_KEY environment variable
        self.client = anthropic.Anthropic()
        self.messages = []  # Start with empty history
        self.is_done = False

    def send(self, user_message):
        """
        Send a message and get Claude's response.

        This method:
        1. Adds your message to history
        2. Sends entire history to Claude
        3. Adds Claude's response to history
        4. Returns what Claude said
        """
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })

        # Call the API with full history
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=self.messages
        )

        # Get Claude's response
        claude_says = response.content[0].text

        # Add to history
        self.messages.append({
            "role": "assistant",
            "content": claude_says
        })

        return claude_says

    def get_message_count(self):
        """How many messages in the conversation?"""
        return len(self.messages)


# --- Using the class ---

# Create a conversation (this calls __init__)
# Uses ANTHROPIC_API_KEY environment variable automatically
convo = SimpleConversation()

# First message
print("You: I want to build a recipe app")
response = convo.send("I want to build a recipe app. What's one question you have?")
print(f"Claude: {response}")

# Second message
print("\nYou: It should work on phones")
response = convo.send("It should work on phones")
print(f"Claude: {response}")

# Check how many messages
print(f"\n(Total messages: {convo.get_message_count()})")
