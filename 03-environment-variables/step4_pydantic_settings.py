"""
Step 4: Type-Safe Config with pydantic-settings

os.environ returns strings. What if you need a number?

    max_tokens = os.environ.get("MAX_TOKENS")  # "1024" (string!)
    max_tokens = int(os.environ.get("MAX_TOKENS"))  # Better, but verbose

pydantic-settings combines Pydantic validation with environment variables:
- Automatic type conversion (string "1024" → int 1024)
- Validation (is it actually a number?)
- Defaults
- SecretStr for API keys (won't leak in logs)
"""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings loaded from environment variables.

    Field names become environment variable names (with prefix).
    e.g., api_key → TASK_CLI_API_KEY
    """

    # SecretStr hides the value when printed
    api_key: SecretStr = Field(
        description="Your API key"
    )

    # String with a default
    model: str = Field(
        default="claude-sonnet-4-5-20250929",
        description="Model to use"
    )

    # Integer - automatically converted from string!
    max_tokens: int = Field(
        default=1024,
        ge=1,
        le=10000,
        description="Maximum tokens in response"
    )

    # Configure how settings are loaded
    model_config = SettingsConfigDict(
        env_prefix="TASK_CLI_",  # Look for TASK_CLI_API_KEY, etc.
        env_file=".env",          # Load from .env file
        env_file_encoding="utf-8",
    )


print("=== Loading Settings ===\n")

try:
    settings = Settings()

    print("Settings loaded successfully!\n")

    # Notice: SecretStr hides the actual value
    print(f"api_key: {settings.api_key}")
    print(f"  (Hidden! To get actual value: settings.api_key.get_secret_value())")
    print()

    print(f"model: {settings.model}")
    print(f"  Type: {type(settings.model)}")
    print()

    print(f"max_tokens: {settings.max_tokens}")
    print(f"  Type: {type(settings.max_tokens)} (auto-converted from string!)")

except Exception as e:
    print(f"Error loading settings: {e}")
    print("\nMake sure .env file exists with TASK_CLI_API_KEY set")


print("\n" + "="*50)
print("WHY pydantic-settings?")
print("="*50)
print()
print("1. TYPE CONVERSION")
print('   "1024" in .env → int 1024 in Python')
print()
print("2. VALIDATION")
print("   max_tokens must be between 1 and 10000")
print()
print("3. DEFAULTS")
print("   If not in .env, use the default value")
print()
print("4. SecretStr")
print("   API keys won't show in logs or error messages")
print()
print("5. SINGLE SOURCE OF TRUTH")
print("   All config in one class, with documentation")
print("="*50)
