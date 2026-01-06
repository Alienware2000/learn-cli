# Module 1: Core Concepts

## What You'll Learn

By the end of this module, you'll understand:
- How to make API calls to Claude
- Why conversations need to track message history
- Why we use classes (and when you don't need them)

## Prerequisites

- Basic Python (functions, dictionaries, lists)
- An Anthropic API key ([get one here](https://console.anthropic.com/))

---

## Step 1: The Simplest API Call

**File:** `step1_basic.py`

This is the absolute minimum code to talk to Claude:

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key-here")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Give me a 3-step plan for: Build a todo app"}
    ]
)

print(response.content[0].text)
```

### Breaking It Down

| Line | What It Does |
|------|--------------|
| `import anthropic` | Load the Anthropic library |
| `client = anthropic.Anthropic(...)` | Create a "client" - like opening a phone line to Claude |
| `client.messages.create(...)` | Send a message and wait for a response |
| `response.content[0].text` | Get the text of Claude's reply |

### The `messages` Parameter

This is a list of messages in the conversation:
```python
messages=[
    {"role": "user", "content": "Your message here"}
]
```

- `role` is either `"user"` (you) or `"assistant"` (Claude)
- `content` is what was said

### Try It

```bash
python step1_basic.py
```

You should see Claude's 3-step plan printed out.

---

## Step 2: Adding User Input

**File:** `step2_interactive.py`

Now we let the user type their own task:

```python
task = input("What do you want to plan? ")
```

That's it! The `input()` function:
1. Prints the prompt
2. Waits for the user to type something and press Enter
3. Returns what they typed as a string

### Try It

```bash
python step2_interactive.py
```

Type a task when prompted and see Claude's response.

---

## Step 3: Having a Conversation

**File:** `step3_conversation.py`

Here's the key insight of this entire module:

> **Claude has no memory.** Every API call is a fresh start.

So how do we have a back-and-forth conversation? **We send the entire history every time.**

### The Problem

```python
# First call
messages = [{"role": "user", "content": "I want to build an app"}]
# Claude responds: "What kind of app?"

# Second call - Claude has NO IDEA what we talked about before!
messages = [{"role": "user", "content": "A mobile one"}]
# Claude: "What do you mean? What are we discussing?"
```

### The Solution

```python
# We keep a running list of ALL messages
messages = []

# First message
messages.append({"role": "user", "content": "I want to build an app"})
response = call_claude(messages)
messages.append({"role": "assistant", "content": response})

# Second message - we send THE WHOLE HISTORY
messages.append({"role": "user", "content": "A mobile one"})
response = call_claude(messages)  # Claude now sees all 3 messages!
```

### Visualizing the Conversation

```
Round 1:
  Send: [user: "I want to build an app"]
  Get:  "What kind of app?"

Round 2:
  Send: [user: "I want to build an app",
         assistant: "What kind of app?",
         user: "A mobile one"]
  Get:  "Great! iOS or Android?"

Round 3:
  Send: [user: "I want to build an app",
         assistant: "What kind of app?",
         user: "A mobile one",
         assistant: "Great! iOS or Android?",
         user: "iOS"]
  Get:  "Here's how to start..."
```

The list keeps growing, and Claude sees everything each time.

### Try It

```bash
python step3_conversation.py
```

Have a 3-round conversation with Claude.

---

## Step 4: Why Use a Class?

**File:** `step4_with_class.py`

By Step 3, our code has a problem: we're managing `messages` manually everywhere. What if we also need to track:
- How many messages we've sent
- Whether the conversation is "done"
- The original question

A **class** bundles data and functions together.

### Without a Class (Messy)

```python
messages = []
is_done = False
question_count = 0

def send_message(messages, user_input, is_done, question_count):
    # ... lots of code ...
    return messages, response, is_done, question_count + 1

# Every function needs all these parameters!
messages, response, is_done, question_count = send_message(
    messages, "Hello", is_done, question_count
)
```

### With a Class (Clean)

```python
class Conversation:
    def __init__(self):
        self.messages = []
        self.is_done = False
        self.question_count = 0

    def send(self, user_input):
        # Can access self.messages, self.is_done, etc.
        # Don't need to pass them around!
        ...
        return response

# Usage is simple
convo = Conversation()
response = convo.send("Hello")
response = convo.send("Tell me more")
```

### Understanding Classes

Think of a class as a **blueprint for creating "things"**.

```python
class Dog:
    def __init__(self, name):
        self.name = name  # This dog's name

    def bark(self):
        print(f"{self.name} says woof!")

# Create two dogs from the blueprint
fido = Dog("Fido")
rex = Dog("Rex")

fido.bark()  # "Fido says woof!"
rex.bark()   # "Rex says woof!"
```

- `__init__` runs when you create a new instance (`Dog("Fido")`)
- `self` refers to "this particular dog" (or conversation, or whatever)
- Methods (functions inside the class) can access `self.whatever`

### Try It

```bash
python step4_with_class.py
```

Notice how clean the usage is - just `convo.send(message)`.

---

## Summary

| Step | Concept | Key Takeaway |
|------|---------|--------------|
| 1 | Basic API call | Just a few lines to talk to Claude |
| 2 | User input | `input()` makes it interactive |
| 3 | Conversation history | Send ALL messages each time (Claude has no memory) |
| 4 | Classes | Bundle data + functions for cleaner code |

## Key Vocabulary

| Term | Meaning |
|------|---------|
| **Client** | The object that connects to an API |
| **Messages** | The list of back-and-forth in a conversation |
| **Role** | Who said something: "user" or "assistant" |
| **Class** | A blueprint for creating objects with data and methods |
| **Instance** | One specific object created from a class |
| **self** | "This particular instance" inside a class |

## What's Next?

In [Module 2: Pydantic](../02-pydantic/), you'll learn how to validate and structure data - making sure the information flowing through your app is always in the right shape.

---

## Exercises (Optional)

1. **Modify step1** to ask Claude for a joke instead of a plan
2. **Modify step3** to allow 5 rounds instead of 3
3. **Add a method to step4's class** that returns the total number of messages
4. **Create your own class** called `Counter` with methods `increment()` and `get_count()`
