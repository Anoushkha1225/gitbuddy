def create_branch(name: str):
    from gitbuddy.engine import GitEngine
    GitEngine().run(f"git checkout -b {name}")

def list_branches():
    from gitbuddy.engine import GitEngine
    GitEngine().run("git branch --all")

def switch_branch(name: str):
    from gitbuddy.engine import GitEngine
    GitEngine().run(f"git checkout {name}")