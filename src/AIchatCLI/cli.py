#!/usr/bin/env python
"""
AIChat CLI - Fast Groq-powered terminal chatbot.
"""
import sys
from typing import NoReturn

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
except ImportError:
    print("❌ Install: pip install rich 'prompt-toolkit>=3.0.0'")
    sys.exit(1)

from .client import ChatClient
from .config import get_provider

# Global UI
console = Console()
session = PromptSession()
style = Style.from_dict({'prompt': '#00ff88 bold'})

def print_welcome():
    """Welcome screen."""
    console.print(Panel(
        "[bold green]🚀 AIChat CLI - Fast Multi-Provider Chatbot[/bold green]\n\n"
        "[dim]Type /help for commands. Ctrl+C to exit.[/dim]",
        title=f"[cyan]{get_provider().upper()} Active[/cyan]",
        border_style="cyan",  # ✅ STRING, not box.ROUNDED
        padding=(1, 2)
    ))

def print_help():
    """Help screen."""
    console.print(Panel(
        "**Commands:**\n"
        "• `/clear` - Clear chat history\n"
        "• `/provider` - Show AI provider\n"
        "• `/help` - Show help\n"
        "• `exit` - Quit",
        title="📋 Help", 
        border_style="yellow"
    ))

def main() -> NoReturn:
    """Main CLI loop."""
    print_welcome()
    console.print()
    
    try:
        client = ChatClient()
        print_help()
        console.print()
        
        while True:
            user_input = session.prompt("💬 You: ", style=style).strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye', '']:
                console.print("[bold green]👋 Goodbye![/bold green]")
                break
            
            if user_input.lower() == '/clear':
                client.clear_history()
                console.print("[bold yellow]🧹 Chat cleared![/bold yellow]")
                continue
            
            if user_input.lower() == '/help':
                print_help()
                continue
            
            console.print("[dim]🤔 AI thinking...[/dim]")
            response = client.send(user_input)
            
            console.print(Panel(
                Markdown(response),
                title="🤖 AI", 
                border_style="blue",  # ✅ STRING
                padding=(1, 2)
            ))
            console.print()
            
    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 Interrupted![/bold yellow]")
    except Exception as e:
        console.print(f"[red bold]❌ Error: {str(e)}[/red bold]")
        console.print("[yellow]💡 Check .env has GROQ_API_KEY[/yellow]")

if __name__ == "__main__":
    main()
