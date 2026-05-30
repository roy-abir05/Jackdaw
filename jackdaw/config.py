import sys
import tomllib
from pathlib import Path
from jackdaw.schemas import BUNDLED_SCHEMAS
from jackdaw.prompts import BUNDLED_PROMPTS

class ConfigManager:
    BASE_DIR = Path.home() / ".jackdaw"
    CONFIG_FILE = BASE_DIR / "config.toml"

    @classmethod
    def ensure_directories_exist(cls):
        """Creates the base dotfile directory safely without enforcing state."""
        cls.BASE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def require_initialization(cls):
        """Enforces the strict initialization rule before running normal commands."""
        if not cls.CONFIG_FILE.exists():
            print("\n[Error] Jackdaw is not initialized.")
            print("Please run `jackdaw init` to configure your AI engine and workspace.\n")
            sys.exit(1)

    @classmethod
    def load_user_space(cls) -> dict:
        """Parses the main config.toml."""
        try:
            with open(cls.CONFIG_FILE, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            print(f"[Error parsing user config: {e}]")
            sys.exit(1)

    @classmethod
    def get_full_context(cls) -> dict:
        """Returns the fully assembled modular configuration state."""
        cls.ensure_directories_exist()
        cls.require_initialization()
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
            "prompts": BUNDLED_PROMPTS,
            "schemas": active_schemas
        }