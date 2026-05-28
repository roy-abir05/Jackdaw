import os
from pathlib import Path
from jackdaw.server.services.coral import run_query
from jackdaw.config import ConfigManager

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
QUERIES_DIR = BASE_DIR / "queries"

class QueryEngine:
    @staticmethod
    def _load_sql_file(filename: str, **kwargs) -> str:
        """Reads a .sql file, strips comments, and injects dynamic variables."""
        filepath = QUERIES_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Query file not found: {filepath}")
        
        with open(filepath, "r") as file:
            lines = file.readlines()
            clean_lines = [line.strip() for line in lines if not line.strip().startswith("--")]
            clean_sql = " ".join(clean_lines)
            return clean_sql.format(**kwargs)

    @staticmethod
    def get_daily_snapshot():
        """Executes the daily snapshot query using active config properties."""
        config = ConfigManager.load_config()
        gh_config = config.get("sources", {}).get("github", {})
        
        sql = QueryEngine._load_sql_file(
            "daily_snapshot.sql", 
            github_owner=gh_config.get("owner", "withcoral"), 
            github_repo=gh_config.get("repo", "coral")
        )
        return run_query(sql)