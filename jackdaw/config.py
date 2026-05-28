import os
from pathlib import Path

# Target file: ~/.jackdaw/config.toml
CONFIG_DIR = Path.home() / ".jackdaw"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG_TEMPLATE = """[jackdaw]
port = 4242

[ai]
# For Groq: use "https://api.groq.com/openai/v1" and a free gsk_... key
# For Local: use "http://localhost:11434/v1" for Ollama (no key needed)
api_key = "YOUR_LLM_API_KEY_HERE"
base_url = "https://api.groq.com/openai/v1"
model = "llama3-8b-8192"

[sources.github]
owner = "withcoral"
repo = "coral"
"""

class ConfigManager:
    @staticmethod
    def ensure_config_exists():
        """Creates the ~/.jackdaw/config.toml file if it doesn't exist."""
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        if not CONFIG_FILE.exists():
            with open(CONFIG_FILE, "w") as f:
                f.write(DEFAULT_CONFIG_TEMPLATE)
            print(f"Initialized default configuration at {CONFIG_FILE}")

    @staticmethod
    def load_config() -> dict:
        """Reads the TOML configuration file cleanly."""
        ConfigManager.ensure_config_exists()
        
        # We use standard parsing; using tomllib (Python 3.11+) or a simple manual fallback
        import tomllib
        with open(CONFIG_FILE, "rb") as f:
            return tomllib.load(f)