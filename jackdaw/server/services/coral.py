import subprocess
import json
from typing import List, Dict, Any

def run_query(sql: str) -> List[Dict[str, Any]]:
    """
    Executes a Coral SQL query via the CLI and returns the parsed JSON.
    """
    try:
        # Using 'coral sql' as per the official documentation
        result = subprocess.run(
            ["coral", "sql", sql, "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the standard output into a Python dictionary/list
        data = json.loads(result.stdout)
        return data

    except subprocess.CalledProcessError as e:
        print(f"Coral Query Failed. Error: {e.stderr}")
        return {"error": "Failed to execute Coral query", "details": e.stderr}
    except json.JSONDecodeError:
        print("Failed to parse Coral output as JSON. Check if the CLI requires a different JSON flag.")
        return {"error": "Invalid JSON from Coral output", "raw_output": result.stdout}