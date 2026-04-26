def connect(url: str):
    from gitbuddy.engine import GitEngine
    from rich.console import Console
    console = Console()
    engine = GitEngine()

    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return

    existing = engine.run("git remote -v", confirm=False)
    if "origin" in existing:
        engine.run(f"git remote set-url origin {url}", confirm=False)
        console.print("[green]Remote URL updated.[/]")
    else:
        engine.run(f"git remote add origin {url}", confirm=False)
        console.print("[green]Remote added.[/]")

    if not engine.has_commits():
        console.print("[yellow]No commits found. Staging and creating initial commit...[/]")
        engine.run("git add .", confirm=False)
        engine.run('git commit -m "initial commit"', confirm=False)

    engine.run("git push -u origin main", confirm=False)
    console.print("[green]Connected and pushed successfully.[/]")