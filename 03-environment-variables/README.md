# Module 3: Environment Variables

## What You'll Learn

By the end of this module, you'll understand:
- Why hardcoding secrets is dangerous
- What environment variables are
- How to use `.env` files
- How to use `pydantic-settings` for type-safe configuration

---

## Step 1: The Problem

**File:** `step1_hardcoded.py`

```python
# NEVER DO THIS!
API_KEY = "sk-ant-abc123xyz"
```

**Why is this bad?**

| Problem | Consequence |
|---------|-------------|
| Committed to Git | Secret is in history forever, even if deleted |
| Sharing code | Can't share without exposing secret |
| Different environments | Dev vs Prod need different keys |
| Security | Hackers scan GitHub for exposed keys |

---

## Step 2: Environment Variables

**File:** `step2_os_environ.py`

Environment variables are values stored in your shell, not in your code.

```python
import os

# Read an environment variable
api_key = os.environ.get("MY_API_KEY")

# With a default if not set
api_key = os.environ.get("MY_API_KEY", "default")

# Raises KeyError if not set
api_key = os.environ["MY_API_KEY"]
```

### Setting Environment Variables

```bash
# Option 1: Export (lasts for terminal session)
export MY_API_KEY=sk-ant-xxx
python my_script.py

# Option 2: Inline (just for this command)
MY_API_KEY=sk-ant-xxx python my_script.py
```

---

## Step 3: The .env File

**File:** `step3_dotenv.py`

Typing `export` every time is tedious. A `.env` file stores your variables:

### Create a .env file

```
# .env
TASK_CLI_API_KEY=sk-ant-your-key-here
TASK_CLI_MODEL=claude-sonnet-4-5-20250929
```

### Load it in Python

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env into os.environ

api_key = os.environ.get("TASK_CLI_API_KEY")
```

### Important: .gitignore

**Never commit your `.env` file!** Add it to `.gitignore`:

```
# .gitignore
.env
```

### The .env.example Pattern

Create a template file that IS committed:

```
# .env.example (committed to git)
TASK_CLI_API_KEY=your-key-here
TASK_CLI_MODEL=claude-sonnet-4-5-20250929
```

Users copy it and fill in their values:
```bash
cp .env.example .env
# Edit .env with real values
```

---

## Step 4: pydantic-settings

**File:** `step4_pydantic_settings.py`

`os.environ` has limitations:
- Everything is a string
- No validation
- No defaults in one place
- Secrets can leak in logs

`pydantic-settings` solves all of these:

```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # SecretStr hides value when printed
    api_key: SecretStr

    # With default
    model: str = Field(default="claude-sonnet-4-5-20250929")

    # Auto-converts string "1024" to int 1024
    max_tokens: int = Field(default=1024, ge=1, le=10000)

    model_config = SettingsConfigDict(
        env_prefix="TASK_CLI_",  # TASK_CLI_API_KEY, etc.
        env_file=".env",
    )


settings = Settings()
print(settings.api_key)  # SecretStr('**********') - hidden!
print(settings.max_tokens)  # 1024 (int, not string)
```

### Why pydantic-settings?

| Feature | Benefit |
|---------|---------|
| Type conversion | `"1024"` → `1024` automatically |
| Validation | Must be between 1 and 10000 |
| SecretStr | Won't leak in logs/errors |
| Defaults | All in one place |
| Documentation | Field descriptions |

---

## How This Connects to the Real Project

In `contextual-task-cli/config.py`:

```python
class Settings(BaseSettings):
    anthropic_api_key: SecretStr
    model_name: str = Field(default="claude-sonnet-4-5-20250929")
    max_tokens: int = Field(default=4096)
    max_questions: int = Field(default=5, ge=1, le=10)

    model_config = SettingsConfigDict(
        env_prefix="TASK_CLI_",
        env_file=".env",
    )
```

The `.env` file:
```
TASK_CLI_ANTHROPIC_API_KEY=sk-ant-your-real-key
```

---

## Summary

| Step | Tool | Purpose |
|------|------|---------|
| 1 | (none) | Understand the problem |
| 2 | `os.environ` | Basic env var reading |
| 3 | `python-dotenv` | Load from .env file |
| 4 | `pydantic-settings` | Type-safe, validated config |

## Key Vocabulary

| Term | Meaning |
|------|---------|
| Environment variable | Value stored in shell, not code |
| `.env` file | File containing environment variables |
| `.env.example` | Template .env file (safe to commit) |
| `SecretStr` | Pydantic type that hides secrets |
| `env_prefix` | Prefix for variable names |

---

## The Pattern

```
.env.example (committed)     →  Users copy to .env
.env (NOT committed)         →  Contains real secrets
.gitignore                   →  Lists .env to prevent commits
pydantic-settings            →  Loads and validates config
```

---

## Exercises (Optional)

1. Create a `.env` file with your own variables
2. Write a script that reads them with `os.environ`
3. Convert to using `pydantic-settings`
4. Try putting an invalid value (like `max_tokens=abc`) and see the error

---

## What's Next?

In [Module 4: Typer CLI](../04-typer-cli/), you'll learn how to build beautiful command-line interfaces with arguments, flags, and help text!
