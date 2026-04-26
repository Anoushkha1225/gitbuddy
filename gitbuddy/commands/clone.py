from gitbuddy.engine import GitEngine

engine = GitEngine()

def clone(url: str, path: str = "."):
    command = f"git clone {url} {path}".strip()
    engine.run(command)