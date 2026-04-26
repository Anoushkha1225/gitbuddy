from gitbuddy.engine import GitEngine

engine = GitEngine()

def push(branch: str = "main", force: bool = False):
    flag = "--force" if force else ""
    engine.run(f"git push origin {branch} {flag}".strip())

def pull(branch: str = "main"):
    engine.run(f"git pull origin {branch}")