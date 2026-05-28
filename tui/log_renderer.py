from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout

console = Console()

class LogRenderer:
    @staticmethod
    def render_dashboard(data: list, ai_analysis: dict):
        # Clear the terminal for a clean dashboard view
        console.clear()

        # 1. The Header
        header = Panel(
            "[bold cyan]Jackdaw Operations Dashboard[/bold cyan]\n[dim]AI Chief Strategist: Anne Bonny[/dim]", 
            style="cyan", 
            border_style="cyan"
        )
        console.print(header)

        # 2. Anne's Analysis Panel
        summary = ai_analysis.get("summary", "Log unavailable.")
        insight = ai_analysis.get("insight", "No insights generated.")
        
        ai_text = f"[bold white]Summary:[/bold white] {summary}\n\n[bold gold1]Strategic Insight:[/bold gold1] {insight}"
        ai_panel = Panel(ai_text, title="[bold gold1]⚓ The Captain's Log[/bold gold1]", border_style="gold1")
        console.print(ai_panel)

        # 3. The Data Table (Code-to-Cash)
        table = Table(title="Recent Deployments vs. Revenue (Code-to-Cash)", expand=True, border_style="green")
        table.add_column("Commit", style="dim", width=10)
        table.add_column("Developer", style="cyan")
        table.add_column("Customer", style="magenta")
        table.add_column("Revenue", justify="right", style="green")

        # Handle the case where Coral returns an error dict instead of a list
        if isinstance(data, dict) and "error" in data:
            console.print(f"[bold red]Data Engine Error:[/bold red] {data['error']}")
            return

        for row in data:
            table.add_row(
                row.get("commit_hash", "")[:7],  # Shorten the hash
                row.get("developer", "Unknown"),
                row.get("customer_name", "Unknown"),
                f"${row.get('revenue_usd', 0.0):.2f}"
            )
        
        console.print(table)
        console.print("\n[dim]Press Ctrl+C to exit.[/dim]\n")