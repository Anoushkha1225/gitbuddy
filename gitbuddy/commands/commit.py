def commit(message: str = None):
    from gitbuddy.engine import GitEngine
    from gitbuddy.ai import parse_command
    engine = GitEngine()
    if not message:
        diff = engine.run("git diff --staged", confirm=False)
        if not diff:
            diff = engine.run("git diff", confirm=False)
        if not diff:
            print("Nothing to commit.")
            return
        message = parse_command(f"generate a short git commit message for this diff:\n{diff}")
    engine.run("git add .")
    engine.run(f'git commit -m "{message}"', confirm=False)