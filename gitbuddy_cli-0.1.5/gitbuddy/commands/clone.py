def clone(url: str, path: str = "."):
    from gitbuddy.engine import GitEngine
    engine = GitEngine()
    command = f"git clone {url} {path}".strip()
    engine.run(command)