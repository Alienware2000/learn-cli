# Learn to Build AI-Powered CLIs

A hands-on, beginner-friendly curriculum for learning to build command-line tools powered by AI (Claude).

## Who Is This For?

You should know:
- Basic Python (functions, dictionaries, imports)
- How to run Python scripts

You'll learn:
- How to integrate AI into your applications
- How to build professional CLI tools
- Industry-standard patterns and libraries

## The Curriculum

| Module | Topic | What You'll Learn |
|--------|-------|-------------------|
| [01](./01-core-concepts/) | **Core Concepts** | API calls, conversation history, classes |
| [02](./02-pydantic/) | **Pydantic** | Data validation, models, JSON conversion |
| [03](./03-environment-variables/) | **Environment Variables** | Secrets management, .env files |
| [04](./04-typer-cli/) | **Typer CLI** | Building beautiful command-line interfaces |
| [05](./05-prompt-engineering/) | **Prompt Engineering** | Getting structured responses from AI |
| [06](./06-full-project/) | **Full Project** | Putting all the pieces together |
| [07](./07-your-project/) | **Your Project** | Build something yourself! |

## How to Use This

Each module folder contains:
- **Step-by-step Python files** - Runnable examples that build on each other
- **README.md** - A complete walkthrough explaining every concept

### Recommended Approach

1. Read the module's README first
2. Run each step file and observe what happens
3. Modify the code and experiment
4. Move to the next module when comfortable

## Setup

### 1. Clone this repository
```bash
git clone https://github.com/Alienware2000/learn-cli.git
cd learn-cli
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install anthropic pydantic pydantic-settings python-dotenv typer rich
```

### 4. Get an Anthropic API key
1. Go to https://console.anthropic.com/
2. Create an account and add credits ($5 is plenty)
3. Generate an API key

## The Final Project

By the end of this curriculum, you'll understand how [contextual-task-cli](https://github.com/Alienware2000/contextual-task-cli) works - an AI-powered task planning tool. More importantly, you'll be able to build your own AI-powered CLI tools.

## Teaching Philosophy

- **Show, don't tell** - Every concept has runnable code
- **Build incrementally** - Start simple, add complexity one step at a time
- **Explain the "why"** - Not just how to do something, but why it matters
- **Beginner-friendly** - No assumed knowledge beyond basic Python

## Questions or Feedback?

Open an issue! This curriculum was built to help others learn.

---

*Built with guidance from Claude Code*
