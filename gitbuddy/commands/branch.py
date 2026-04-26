from gitbuddy.engine import GitEngine

engine = GitEngine()

def create_branch(name: str):
    engine.run(f"git checkout -b {name}")

def list_branches():
    engine.run("git branch --all")

def switch_branch(name: str):
    engine.run(f"git checkout {name}")