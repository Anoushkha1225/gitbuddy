import subprocess
from pathlib import Path
from rich.console import Console
from gitbuddy.prompts import confirm_command

console = Console()

class GitEngine:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()

    def run(self, command: str, confirm: bool = True) -> str:
        if confirm:
            if not confirm_command(command):
                return ""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.stdout:
                console.print(f"[green]{result.stdout.strip()}[/]")
            if result.stderr:
                console.print(f"[red]{result.stderr.strip()}[/]")
            return result.stdout.strip()
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
            return ""