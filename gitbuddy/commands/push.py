def push(branch: str = "main", force: bool = False):
    from gitbuddy.engine import GitEngine
    flag = "--force" if force else ""
    GitEngine().run(f"git push origin {branch} {flag}".strip())

def pull(branch: str = "main"):
    from gitbuddy.engine import GitEngine
    GitEngine().run(f"git pull origin {branch}")