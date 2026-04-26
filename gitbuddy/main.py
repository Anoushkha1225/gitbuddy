import os
import typer
from gitbuddy.engine import GitEngine
from gitbuddy.ai import parse_command
from gitbuddy.commands.clone import clone as git_clone
from gitbuddy.commands.commit import commit as git_commit
from gitbuddy.commands.branch import create_branch, list_branches, switch_branch
from gitbuddy.commands.push import push as git_push, pull as git_pull
from rich.console import Console

app = typer.Typer()
console = Console()
engine = GitEngine()

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
def run(prompt: str = typer.Argument(..., help="Natural language git command")):
    """Run any git command using natural language."""
    console.print(f"\n[bold purple]GitBuddy[/] processing: [italic]{prompt}[/]")
    command = parse_command(prompt)
    engine.run(command)

@app.command()
def direct(command: str = typer.Argument(..., help="Run a raw git command")):
    """Run a raw git command directly."""
    engine.run(command)

@app.command()
def clone(url: str = typer.Argument(..., help="Repo URL to clone"),
          path: str = typer.Argument(".", help="Destination path")):
    """Clone a repository."""
    git_clone(url, path)

@app.command()
def commit(message: str = typer.Argument(None, help="Commit message")):
    """Stage all changes and commit."""
    git_commit(message)

@app.command()
def branch(
    action: str = typer.Argument(..., help="create / list / switch"),
    name: str = typer.Argument(None, help="Branch name")
):
    """Manage branches."""
    if action == "create" and name:
        create_branch(name)
    elif action == "list":
        list_branches()
    elif action == "switch" and name:
        switch_branch(name)
    else:
        console.print("[red]Usage: branch create <name> | branch list | branch switch <name>[/]")

@app.command()
def push(branch: str = typer.Argument("main"),
         force: bool = typer.Option(False, "--force")):
    """Push to remote."""
    git_push(branch, force)

@app.command()
def pull(branch: str = typer.Argument("main")):
    """Pull from remote."""
    git_pull(branch)

if __name__ == "__main__":
    app()