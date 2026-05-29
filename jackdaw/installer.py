import os
from rich.console import Console
from rich.prompt import Prompt
from jackdaw.config import ConfigManager

console = Console()

class JackdawInstaller:
    
    @classmethod
    def setup_core(cls, api_key: str, base_url: str, model: str, gh_owner: str, gh_repo: str):
        """Initializes the base directories and writes the user config."""
        ConfigManager.ensure_directories_exist()
        
        base_config = f"""[jackdaw]
port = 4242
active_workspace = "default"

[ai]
api_key = "{api_key}"
base_url = "{base_url}"
model = "{model}"

[workspaces.default]
platform = "github"
owner = "{gh_owner}"
repo = "{gh_repo}"
"""
        ConfigManager.CONFIG_FILE.write_text(base_config)
        return True
    
    @classmethod
    def manage_specs(cls):
        """Interactive selector to manage API keys for bundled schemas."""
        # The bundled specs your binary currently supports
        SUPPORTED_SPECS = {
            "1": {"name": "github", "desc": "GitHub (Requires Personal Access Token)"},
            "2": {"name": "stripe", "desc": "Stripe (Requires Secret Key)"}
        }
        
        while True:
            console.print("\n[bold cyan]Manage Schema Connections[/bold cyan]")
            for key, spec in SUPPORTED_SPECS.items():
                console.print(f"  [{key}] {spec['name'].capitalize()} - {spec['desc']}")
            console.print("  [q] Quit")
            
            choice = Prompt.ask("\nSelect a connector to add/update, or 'q' to quit", choices=["1", "2", "q"])
            
            if choice == 'q':
                break
                
            selected_spec = SUPPORTED_SPECS[choice]["name"]
            
            action = Prompt.ask(
                f"Do you want to (a)dd/update or (r)emove the {selected_spec.capitalize()} connection?", 
                choices=["a", "r"], 
                default="a"
            ).lower()
            
            if action == 'a':
                api_key = Prompt.ask(f"Enter your {selected_spec.capitalize()} API Key", password=True)
                
                with open(ConfigManager.CONFIG_FILE, "a") as f:
                    f.write(f"\n[secrets.{selected_spec}]\napi_key = \"{api_key}\"\n")
                
                console.print(f"[bold green]✔ Added {selected_spec} credentials to config.[/bold green]")
                

            elif action == 'r':
                console.print(f"[yellow]⚠ To completely remove {selected_spec}, open ~/.jackdaw/config.toml and delete its [secrets.{selected_spec}] block.[/yellow]")

    @classmethod
    def run_cli_wizard(cls):
        """The interactive terminal entry point."""
        console.clear()
        console.print("[bold cyan]⚓ Jackdaw Initialization[/bold cyan]\n")
        
        if not ConfigManager.CONFIG_FILE.exists():
            console.print("[bold gold1]Configure AI Engine[/bold gold1]")
            console.print("[dim]Jackdaw is vendor-neutral. You must explicitly provide your AI routing details.[/dim]\n")
            
            # No defaults provided. The user must type their URL and model.
            base_url = Prompt.ask("Base URL (e.g., https://api.groq.com/openai/v1 or http://localhost:11434/v1)")
            model = Prompt.ask("Model Name (e.g., llama-3.3-70b-versatile or mistral)")
            api_key = Prompt.ask("API Key (hidden, leave blank if using local LLM)", password=True)
            
            # Hard abort if they leave the required fields blank
            if not base_url.strip() or not model.strip():
                console.print("\n[bold red]✖ Setup aborted: Base URL and Model are mandatory.[/bold red]\n")
                return
            
            console.print("\n[bold gold1]Configure Default Workspace[/bold gold1]")
            gh_owner = Prompt.ask("GitHub Owner/Organization (e.g., withcoral)")
            gh_repo = Prompt.ask("GitHub Repository Name (e.g., coral)")

            if not gh_owner.strip() or not gh_repo.strip():
                console.print("\n[bold red]✖ Setup aborted: Workspace details are mandatory.[/bold red]\n")
                return
            
            cls.setup_core(api_key=api_key, base_url=base_url, model=model, gh_owner=gh_owner, gh_repo=gh_repo)
            console.print("\n[green]✔ Core config initialized.[/green]\n")
        else:
            console.print("[dim]Core config already exists. Skipping setup...[/dim]\n")
            
        # Drop right into spec management
        cls.manage_specs()
        console.print("\n[bold cyan]✔ Jackdaw configuration complete.[/bold cyan]\n")