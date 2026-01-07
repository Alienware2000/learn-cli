# Learn to Build AI-Powered CLIs

A hands-on, beginner-friendly curriculum for learning to build command-line tools powered by AI (Claude).

## Project Overview

This is an educational repository with 7 modules teaching how to build AI-powered CLI tools from scratch. Each module has runnable Python step files and a comprehensive README.

**Repository:** https://github.com/Alienware2000/learn-cli

## Curriculum Structure

| Module | Folder | Topic |
|--------|--------|-------|
| 1 | `01-core-concepts/` | API calls, conversation history, classes |
| 2 | `02-pydantic/` | Data validation, models, JSON |
| 3 | `03-environment-variables/` | Secrets management, .env files |
| 4 | `04-typer-cli/` | Building CLI interfaces |
| 5 | `05-prompt-engineering/` | Structured AI responses |
| 6 | `06-full-project/` | How everything connects |
| 7 | `07-your-project/` | Build your own project |

## File Pattern

Each module follows this pattern:
```
XX-module-name/
├── README.md           # Comprehensive walkthrough
├── step1_*.py          # First concept
├── step2_*.py          # Builds on step 1
├── step3_*.py          # And so on...
└── (optional files)    # .env.example, etc.
```

## Running Examples

Most step files require the `ANTHROPIC_API_KEY` environment variable:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python 01-core-concepts/step1_basic.py
```

Module 4 (Typer) examples don't need an API key:
```bash
python 04-typer-cli/step2_basic_typer.py --help
python 04-typer-cli/step5_rich_output.py
```

## Dependencies

```bash
pip install anthropic pydantic pydantic-settings python-dotenv typer rich
```

## Teaching Philosophy

- **Show, don't tell** - Every concept has runnable code
- **Build incrementally** - Start simple, add complexity
- **Explain the "why"** - Not just how, but why it matters
- **Beginner-friendly** - No assumed knowledge beyond basic Python

## Related Project

This curriculum teaches the concepts used in:
- https://github.com/Alienware2000/contextual-task-cli

## Content Guidelines

When adding or modifying content:
- Keep step files focused on ONE concept
- Include docstrings explaining what each file demonstrates
- Add "KEY CONCEPTS" comments at the bottom of step files
- READMEs should be comprehensive but beginner-friendly
- Never hardcode real API keys - use environment variables
