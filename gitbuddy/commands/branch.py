def create_branch(name: str):
    from gitbuddy.engine import GitEngine
    engine = GitEngine()
    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return
    existing = engine.run("git branch --list", confirm=False)
    if name in existing:
        print(f"Error: branch '{name}' already exists.")
        return
    engine.run(f"git checkout -b {name}")

def list_branches():
    from gitbuddy.engine import GitEngine
    engine = GitEngine()
    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return
    engine.run("git branch --all")

def switch_branch(name: str):
    from gitbuddy.engine import GitEngine
    engine = GitEngine()
    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return
    existing = engine.run("git branch --list", confirm=False)
    if name not in existing:
        print(f"Error: branch '{name}' does not exist. Use 'gitbuddy branch list' to see all branches.")
        return
    engine.run(f"git checkout {name}")