import os
from pathlib import Path

# Target file: ~/.jackdaw/config.toml
CONFIG_DIR = Path.home() / ".jackdaw"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG_TEMPLATE = """[jackdaw]
port = 4242

[ai]
api_key = "YOUR_LLM_API_KEY_HERE"
base_url = "https://api.groq.com/openai/v1"
model = "llama-3.3-70b-versatile"

[sources.github]
owner = "withcoral"
repo = "coral"

[prompts]
system_sql = '''You are 'Anne', an expert SQL data analyst. Translate the user's question into a single, valid Coral SQL query.
RULES:
1. Output ONLY the raw SQL query. No explanations.
2. Do NOT wrap the output in markdown (do NOT use ```sql).
3. Always use LIMIT 15 to prevent terminal overflow.
4. NEVER use SELECT *. Always explicitly select 3 to 5 relevant columns.'''

[schema.stripe]
charges = "Columns: id, amount (in cents), customer (ID), created, description. Note: Divide amount by 100.0 for USD."
customers = "Columns: id, name, email, created. Note: Join with stripe.charges ON stripe.charges.customer = stripe.customers.id"

[schema.github]
commits = "Columns: sha, commit__author__name, commit__author__date, commit__message. RULE: MUST include WHERE owner = '{gh_owner}' AND repo = '{gh_repo}'"
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