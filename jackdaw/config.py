import os
import tomllib
from pathlib import Path

class ConfigManager:
    BASE_DIR = Path.home() / ".jackdaw"
    CONFIG_FILE = BASE_DIR / "config.toml"
    PROMPTS_DIR = BASE_DIR / "prompts"
    SCHEMAS_DIR = BASE_DIR / "schemas"

    @classmethod
    def ensure_directories_exist(cls):
        """Creates the dotfile architecture if it doesn't exist."""
        cls.BASE_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

        # Generate default config if missing
        if not cls.CONFIG_FILE.exists():
            cls._write_default_user_config()
            
        # Generate a default system prompt if missing
        default_prompt = cls.PROMPTS_DIR / "system.txt"
        if not default_prompt.exists():
            default_prompt.write_text(
                "You are 'Anne', an expert SQL data analyst. Output ONLY valid Coral SQL. "
                "Do NOT use markdown wrapping. Always use LIMIT 15 unless specified. NEVER use SELECT *."
            )

    @classmethod
    def load_user_space(cls) -> dict:
        """Parses the main config.toml for API keys and target workspaces."""
        if not cls.CONFIG_FILE.exists():
            return {}
        try:
            with open(cls.CONFIG_FILE, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            print(f"[Error parsing user config: {e}]")
            return {}

    @classmethod
    def load_prompts(cls) -> dict:
        """Scans the prompts directory and loads all .txt files into a dictionary."""
        prompts = {}
        if not cls.PROMPTS_DIR.exists():
            return prompts
            
        for filepath in cls.PROMPTS_DIR.glob("*.txt"):
            try:
                prompts[filepath.stem] = filepath.read_text().strip()
            except Exception:
                pass
        return prompts

    @classmethod
    def load_schemas(cls) -> dict:
        """Scans the schemas directory and loads all .toml source maps."""
        schemas = {}
        if not cls.SCHEMAS_DIR.exists():
            return schemas
            
        for filepath in cls.SCHEMAS_DIR.glob("*.toml"):
            try:
                with open(filepath, "rb") as f:
                    # Keyed by filename (e.g., 'stripe.toml' -> schemas['stripe'])
                    schemas[filepath.stem] = tomllib.load(f)
            except Exception:
                pass
        return schemas

    @classmethod
    def get_full_context(cls) -> dict:
        """Returns the fully assembled modular configuration state."""
        cls.ensure_directories_exist()
        return {
            "user": cls.load_user_space(),
            "prompts": cls.load_prompts(),
            "schemas": cls.load_schemas()
        }

    @classmethod
    def _write_default_user_config(cls):
        """Generates the decoupled target architecture for user space."""
        default_toml = """[jackdaw]
port = 4242

[ai]
api_key = "YOUR_LLM_API_KEY_HERE"
base_url = "https://api.groq.com/openai/v1"
model = "llama-3.3-70b-versatile"

# Workspaces allow decoupling an owner from a single repository.
# You can define multiple workspaces to quickly switch contexts.
[workspaces.default]
platform = "github"
owner = "withcoral"
repo = "coral"
"""
        cls.CONFIG_FILE.write_text(default_toml)