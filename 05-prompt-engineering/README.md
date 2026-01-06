# Module 5: Prompt Engineering

## What You'll Learn

By the end of this module, you'll understand:
- Why unstructured AI responses are hard to use in code
- How to get Claude to respond in JSON format
- What system prompts are and how to use them
- How to create dynamic prompts with templates
- The iterative process of improving prompts

---

## The Big Picture

So far you've learned:
- **Module 1**: How to call Claude's API
- **Module 2**: How to define data structures with Pydantic
- **Module 3**: How to manage configuration safely
- **Module 4**: How to build beautiful CLIs

But there's a gap: **How do you get Claude to return data your code can actually use?**

If you ask Claude "break down this task," it responds with natural text. That's great for humans, but your code can't easily extract the steps, count them, or save them to a database.

**Prompt engineering** is the skill of crafting prompts that get Claude to respond exactly how you need.

---

## Step 1: The Problem

**File:** `step1_no_structure.py`

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    messages=[
        {"role": "user", "content": f"Break down this task: {task}"}
    ]
)
```

Claude might respond:

```
Here's how to build a personal website:

1. Choose a domain name
   First, think about what you want...

2. Select a hosting provider
   There are many options...
```

Or maybe:

```
To build a website, you'll need to:
- Pick a domain
- Find hosting
- Design your site
```

Or even:

```
Building a website involves several key steps.
The first thing you should do is...
```

**The Problem**: Every response has different formatting. Parsing this reliably is nearly impossible!

---

## Step 2: Asking for JSON

**File:** `step2_ask_for_json.py`

The simplest fix: **Ask Claude to respond in JSON!**

```python
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
```

Now Claude responds with:

```json
{
    "task": "Build a personal website",
    "steps": [
        {"number": 1, "title": "Choose domain name", "description": "Pick a memorable..."},
        {"number": 2, "title": "Select hosting", "description": "Compare providers..."}
    ]
}
```

Your code can now:
```python
data = json.loads(response)
print(f"Found {len(data['steps'])} steps!")
for step in data['steps']:
    print(f"  {step['number']}. {step['title']}")
```

### Run It

```bash
python step2_ask_for_json.py
```

---

## Step 3: System Prompts

**File:** `step3_system_prompt.py`

Putting all the JSON instructions in every message is messy. **System prompts** solve this.

Think of it like:
- **System prompt** = Job description for Claude
- **User message** = The actual task

```python
SYSTEM_PROMPT = """You are a task planning assistant.

IMPORTANT RULES:
1. Always respond with valid JSON only - no other text
2. Use this exact format:
{
    "task": "the original task",
    "estimated_time": "total time estimate",
    "difficulty": "easy|medium|hard",
    "steps": [...]
}
"""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    system=SYSTEM_PROMPT,     # <-- Rules go here
    messages=[
        {"role": "user", "content": "Learn to play guitar"}  # <-- Simple!
    ]
)
```

### Benefits of System Prompts

| Without System Prompt | With System Prompt |
|-----------------------|-------------------|
| Every message needs format instructions | Format defined once |
| Long, repetitive prompts | Clean, simple messages |
| Easy to forget rules | Consistent behavior |
| Hard to maintain | Easy to update |

### Run It

```bash
python step3_system_prompt.py
```

---

## Step 4: Template Variables

**File:** `step4_templates.py`

Real applications need **dynamic prompts** that change based on context.

```python
SYSTEM_TEMPLATE = """You are a {role} assistant helping with {domain} tasks.

Your communication style should be: {style}

Always respond with valid JSON...

{extra_instructions}
"""

def create_system_prompt(role, domain, style, extra_instructions=""):
    return SYSTEM_TEMPLATE.format(
        role=role,
        domain=domain,
        style=style,
        extra_instructions=extra_instructions
    )
```

Now you can create different assistants:

```python
# Cooking assistant
cooking_prompt = create_system_prompt(
    role="professional chef",
    domain="cooking",
    style="warm and encouraging",
    extra_instructions="Include cooking times."
)

# Fitness assistant
fitness_prompt = create_system_prompt(
    role="personal trainer",
    domain="fitness",
    style="motivating and energetic",
    extra_instructions="Include safety warnings."
)
```

### Escaping Braces

When your template contains JSON, you need to escape the braces:

```python
# {variable} = gets replaced
# {{literal}} = stays as { in output

template = """
Use this format:
{{
    "name": "{user_name}",
    "data": {{}}
}}
"""

result = template.format(user_name="Alice")
# Output:
# {
#     "name": "Alice",
#     "data": {}
# }
```

### Run It

```bash
python step4_templates.py
```

---

## Step 5: Iterating on Prompts

**File:** `step5_iteration.py`

Prompt engineering is an **iterative process**:

```
Write prompt → Test → See problems → Improve → Repeat
```

### Evolution of a Prompt

**Version 1 - Too Vague:**
```
Help break down tasks into steps.
```
❌ Claude might not return JSON at all

**Version 2 - No Format:**
```
You are a task planning assistant.
Always respond in JSON format.
```
❌ Claude returns JSON but structure varies

**Version 3 - Basic Format:**
```
Respond in this JSON format:
{
    "steps": [{"title": "...", "description": "..."}]
}
```
⚠️ Better, but Claude might add "Here's the JSON:" before it

**Version 4 - Production Ready:**
```
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
```
✅ Clear, specific, constrained

### Run It

```bash
python step5_iteration.py
```

---

## Prompt Engineering Tips

### 1. Be EXPLICIT About Format

```python
# Bad
"Respond in JSON"

# Good
"Respond with ONLY valid JSON. No markdown code blocks. No explanation before or after."
```

### 2. Show the EXACT Structure

Don't just describe it - show a complete example:

```python
# Bad
"Return a JSON object with task and steps"

# Good
"""Return JSON in exactly this format:
{
    "task": "example task",
    "steps": [
        {"number": 1, "title": "Example", "description": "Details here"}
    ]
}"""
```

### 3. Add Constraints

Constraints help Claude make decisions:

```python
"""
Rules:
- Maximum 5 steps
- Each title under 50 characters
- Difficulty must be: easy, medium, or hard
- Times in format: "X minutes" or "X hours"
"""
```

### 4. Handle Edge Cases

Think about what could go wrong:

```python
"""
If the task is too vague, respond with:
{"error": "Please provide more details about..."}

If the task is impossible, respond with:
{"error": "This task cannot be completed because..."}
"""
```

### 5. Test with Different Inputs

Try:
- Simple tasks: "Make coffee"
- Complex tasks: "Start a business"
- Vague tasks: "Be more productive"
- Edge cases: Empty string, very long text

---

## How This Connects to the Real Project

In `contextual-task-cli/prompts.py`:

```python
SYSTEM_PROMPT = """You are a task planning assistant...

You will have a conversation with the user to understand their task.
Ask 2-3 clarifying questions before creating a plan.

When ready to provide the final plan, respond with JSON:
{
    "type": "plan",
    "plan": {
        "title": "...",
        "tasks": [...]
    }
}

When asking questions, respond with:
{
    "type": "question",
    "question": "..."
}
"""
```

The real project uses:
- System prompts for consistent behavior
- JSON format for parseable responses
- Different response types (`question` vs `plan`)
- Structured output that matches Pydantic models

---

## Summary

| Step | Concept | Key Code |
|------|---------|----------|
| 1 | The problem | Unstructured text is hard to parse |
| 2 | Ask for JSON | Include format in prompt |
| 3 | System prompts | `system=SYSTEM_PROMPT` |
| 4 | Templates | `template.format(var=value)` |
| 5 | Iteration | Test, improve, repeat |

## Quick Reference

```python
# Basic JSON request
prompt = """Do the task. Respond with ONLY JSON:
{"result": "..."}"""

# System prompt
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system="You are a JSON-only assistant...",
    messages=[{"role": "user", "content": "..."}]
)

# Template with variables
template = "You are a {role} assistant"
prompt = template.format(role="cooking")

# Escaping braces for JSON in templates
template = """Return: {{"name": "{name}"}}"""
```

---

## Exercises (Optional)

1. Create a system prompt for a "code reviewer" that returns JSON with issues found
2. Build a template that can switch between "beginner" and "expert" explanation styles
3. Write a prompt that asks for JSON, then try to "break" it with weird inputs
4. Compare responses from the same task with different system prompts

---

## What's Next?

In [Module 6: Putting It All Together](../06-full-project/), you'll see how all these pieces connect in the real `contextual-task-cli` project!
