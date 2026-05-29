import os
import tomllib
from pathlib import Path
from jackdaw.schemas import BUNDLED_SCHEMAS

class ConfigManager:
    BASE_DIR = Path.home() / ".jackdaw"
    CONFIG_FILE = BASE_DIR / "config.toml"
    PROMPTS_DIR = BASE_DIR / "prompts"

    @classmethod
    def ensure_directories_exist(cls):
        """Creates the dotfile architecture if it doesn't exist."""
        cls.BASE_DIR.mkdir(parents=True, exist_ok=True)
        cls.PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

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
    def get_full_context(cls) -> dict:
        """Returns the fully assembled modular configuration state."""
        cls.ensure_directories_exist()
        user_config = cls.load_user_space()
        
        active_schemas = {}
        secrets = user_config.get("secrets", {})
        
        active_ws_name = user_config.get("jackdaw", {}).get("active_workspace", "default")
        active_platform = user_config.get("workspaces", {}).get(active_ws_name, {}).get("platform")
        
        for spec_name, schema_rules in BUNDLED_SCHEMAS.items():
            if spec_name in secrets or spec_name == active_platform:
                active_schemas[spec_name] = schema_rules

        return {
            "user": user_config,
            "prompts": cls.load_prompts(),
            "schemas": active_schemas
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