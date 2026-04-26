def push(branch: str = "main", force: bool = False):
    from gitbuddy.engine import GitEngine
    engine = GitEngine()
    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return
    if not engine.has_remote():
        print("Error: no remote configured. Run 'gitbuddy connect <url>' first.")
        return
    if not engine.has_commits():
        print("Error: no commits yet. Make a commit before pushing.")
        return
    flag = "--force" if force else ""
    engine.run(f"git push origin {branch} {flag}".strip())

def pull(branch: str = "main"):
    from gitbuddy.engine import GitEngine
    engine = GitEngine()
    if not engine.is_git_repo():
        print("Error: not inside a git repo. Run 'git init' first.")
        return
    if not engine.has_remote():
        print("Error: no remote configured. Run 'gitbuddy connect <url>' first.")
        return
    if engine.has_uncommitted_changes():
        print("Warning: you have uncommitted changes. Commit or stash them before pulling.")
        return
    engine.run(f"git pull origin {branch}")