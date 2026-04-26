import typer
from gitbuddy.engine import GitEngine
from gitbuddy.ai import parse_command
from rich.console import Console
import os
app=typer.Typer()
console=Console()
engine=GitEngine()


@app.command()
def setup():
    """Configure your Groq API key."""
    console.print("\n[bold purple]GitBuddy Setup[/]")
    console.print("Get your free API key at: [bold]https://console.groq.com[/]\n")
    key = console.input("[bold cyan]Enter your Groq API key:[/] ").strip()
    env_path = os.path.join(os.getcwd(), ".env")
    with open(env_path, "w") as f:
        f.write(f"GROQ_API_KEY={key}\n")
    console.print("\n[green]Setup complete! You can now use GitBuddy.[/]")


@app.command()
def run(prompt:str = typer.Argument(...,help="Natural language or git command")):
    """Run a git command using natural language or directly."""
    console.print(f"\n[bold purple]GitBuddy[/] processing: [italic]{prompt}[/]")
    command = parse_command(prompt)
    engine.run(command)

@app.command()
def direct(command: str= typer.Argument(...,help="Run a raw git command directly")):
    """Run a raw git command directly, with permission prompt."""
    engine.run(command)

if __name__=="__main__":
    app()