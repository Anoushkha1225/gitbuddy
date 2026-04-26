import subprocess
import sys
import os

def setup_alias():
    profile_path = subprocess.run(
        ["powershell", "-Command", "echo $PROFILE"],
        capture_output=True, text=True
    ).stdout.strip()

    alias = '\nfunction gitbuddy { python -m gitbuddy.main @args }'

    with open(profile_path, 'a+') as f:
        f.seek(0)
        if 'function gitbuddy' not in f.read():
            f.write(alias)
            print("GitBuddy alias added. Restart your terminal.")
        else:
            print("GitBuddy already set up.")

if __name__ == "__main__":
    setup_alias()