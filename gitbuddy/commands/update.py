def run_workflow(steps: list, user_input: str = ""):
    from gitbuddy.engine import GitEngine
    from gitbuddy.ai import parse_command
    from rich.console import Console
    console = Console()
    engine = GitEngine()

    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return

    for step in steps:
        if step == "__GENERATE_COMMIT__":
            console.print("[yellow]Generating commit message...[/]")
            diff = engine.run("git diff --staged", confirm=False)
            if not diff:
                diff = engine.run("git diff", confirm=False)
            if not diff:
                console.print("[red]Nothing to commit.[/]")
                return
            message = parse_command(f"generate a short git commit message for this diff:\n{diff}")
            console.print(f"[yellow]Committing: {message}[/]")
            engine.run(f'git commit -m "{message}"', confirm=False)
        else:
            engine.run(step, confirm=False)