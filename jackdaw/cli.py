import argparse
import sys
from jackdaw.server.services.query_engine import QueryEngine
from jackdaw.server.services.anne import AnneEngine
from tui.log_renderer import LogRenderer
from jackdaw.config import ConfigManager

def main():
    parser = argparse.ArgumentParser(description="Jackdaw: Local SaaS Analytics")
    subparsers = parser.add_subparsers(dest="command")

    # Command: jackdaw init
    init_parser = subparsers.add_parser("init", help="Initialize Jackdaw configuration")
    
    # Command: jackdaw log
    log_parser = subparsers.add_parser("log", help="Display the AI dashboard")

    args = parser.parse_args()

    if args.command == "log":
        print("Gathering intel from Coral and Anne... (this takes a few seconds)")
        try:
            ConfigManager.ensure_config_exists()
            data = QueryEngine.get_code_to_cash_metrics()
            
            if isinstance(data, dict) and "error" in data:
                print(f"Error fetching data: {data['error']}")
                sys.exit(1)
                
            ai_analysis = AnneEngine.generate_captains_log(data)
            LogRenderer.render_dashboard(data, ai_analysis)
            
        except Exception as e:
            print(f"Failed to generate log: {e}")
            
    elif args.command == "init":
        print("Init flow coming next!")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()