import sys
import os
import json

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.agents.orchestrator import handle_request

def test_cli():
    print("🤖 Testing Enterprise AI (CLI Mode)...\n")
    
    query = "Check inventory status for material M-9001"
    print(f"User: {query}")
    print("-" * 50)
    
    # Run Agent
    result = handle_request(query)
    
    # Parse Response
    response_text = result['response']
    
    # Use Rich to render Markdown
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        console = Console()
        md = Markdown(response_text)
        console.print(md)
    except ImportError:
        print(response_text)
        
    print("-" * 50)

if __name__ == "__main__":
    test_cli()
