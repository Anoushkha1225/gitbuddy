from rich.console import Console
from rich.panel import Panel

console = Console()

DESTRUCTIVE_COMMANDS = [
    "reset --hard",
    "force push",
    "push --force",
    "clean -fd",
    "rebase",
    "rm",
    "checkout --",
]

def is_destructive(command: str) -> bool:
    return any(d in command for d in DESTRUCTIVE_COMMANDS)

def confirm_command(command: str) -> bool:
    if is_destructive(command):
        console.print(Panel(
            f"[bold red]Warning:[/] This is a destructive command.\n[yellow]{command}[/]",
            title="⚠ Proceed with caution",
            border_style="red"
        ))
    else:
        console.print(f"\n[bold yellow]Command:[/] {command}")

    choice = console.input("[bold cyan]Run this? (y/n):[/] ").strip().lower()
    
    if choice != "y":
        console.print("[red]Cancelled.[/]")
        return False
    return True