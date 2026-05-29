import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from jackdaw.server.services.query_engine import QueryEngine
from jackdaw.server.services.anne import AnneEngine
from tui.log_renderer import LogRenderer
from jackdaw.config import ConfigManager
from jackdaw.installer import JackdawInstaller

console = Console()

def render_dynamic_table(data: list, query: str):
    """Renders an arbitrary list of dictionaries as a Rich table."""
    if not data:
        console.print("[yellow]No data returned for that query.[/yellow]")
        return
        
    if isinstance(data, dict) and "error" in data:
        console.print(f"[bold red]Execution Error:[/bold red] {data.get('details', data.get('error'))}")
        return

    # Create table and use the keys of the first dictionary as column headers
    table = Table(title="Jackdaw Intelligence", border_style="cyan")
    headers = list(data[0].keys())
    
    for header in headers:
        table.add_column(header.capitalize(), style="green")
        
    for row in data:
        table.add_row(*[str(row.get(h, "")) for h in headers])
        
    console.print(Panel(f"[dim]{query}[/dim]", title="[cyan]Anne's Generated SQL[/cyan]", border_style="cyan"))
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Jackdaw: Local SaaS Analytics")
    subparsers = parser.add_subparsers(dest="command")

    # Command: jackdaw init
    subparsers.add_parser("init", help="Initialize Jackdaw configuration")
    
    # Command: jackdaw log
    subparsers.add_parser("log", help="Display the AI dashboard")
    
    # Command: jackdaw ask "your question"
    ask_parser = subparsers.add_parser("ask", help="Ask Anne to query your data dynamically")
    ask_parser.add_argument("question", type=str, help="Your natural language question")

    args = parser.parse_args()

    if args.command == "log":
        print("Gathering intel from Coral and Anne... (this takes a few seconds)")
        try:
            data = QueryEngine.get_code_to_cash_metrics()
            
            if isinstance(data, dict) and "error" in data:
                print(f"Error fetching data: {data['error']}")
                sys.exit(1)
                
            ai_analysis = AnneEngine.generate_captains_log(data)
            LogRenderer.render_dashboard(data, ai_analysis)
        except Exception as e:
            print(f"Failed to generate log: {e}")

    elif args.command == "ask":
        console.print("[dim]Analyzing schema and consulting Anne...[/dim]")
        ConfigManager.ensure_directories_exist()
        
        schema = QueryEngine.get_active_schema()
        
        generated_sql = AnneEngine.write_sql(args.question, schema)
        
        if generated_sql.startswith("-- Error"):
            console.print(f"[bold red]{generated_sql}[/bold red]")
            sys.exit(1)
            
        console.print("[dim]Executing query...[/dim]\n")
        results = QueryEngine.execute_raw_sql(generated_sql)
        
        render_dynamic_table(results, generated_sql)

    elif args.command == "init":
        try:
            JackdawInstaller.run_cli_wizard()
        except KeyboardInterrupt:
            print("\nInitialization aborted.")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()