import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.expanduser("~"), ".gitbuddy.env"))

HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".gitbuddy_history.json")
MAX_HISTORY = 10

SYSTEM_PROMPT = """You are a Git assistant that converts natural language into git commands or workflow names.

If the input requires a single git command, reply with ONLY that raw git command.
If the input requires multiple steps, reply with ONLY one of these workflow names:
- WORKFLOW:update
- WORKFLOW:sync
- WORKFLOW:start_feature
- WORKFLOW:finish_feature
- WORKFLOW:undo_everything
- WORKFLOW:fresh_start

No explanations, no markdown, no backticks.
Use previous commands as context to understand what the user wants next.

Examples:
"show status" -> git status
"create branch login" -> git checkout -b login
"undo my last commit but keep changes" -> git reset --soft HEAD~1
"push my changes" -> WORKFLOW:update
"save and upload" -> WORKFLOW:update
"update my repo" -> WORKFLOW:update
"get latest and push mine" -> WORKFLOW:sync
"new feature called login" -> WORKFLOW:start_feature
"im done with this feature" -> WORKFLOW:finish_feature
"throw away everything" -> WORKFLOW:undo_everything
"save work temporarily" -> WORKFLOW:fresh_start
"now push it" -> WORKFLOW:update
"switch to it" -> git checkout feature-login
"""

CHAIN_WORKFLOWS = {
    "update": [
        "git add .",
        "GENERATE_COMMIT",
        "git push"
    ],
    "sync": [
        "git pull",
        "git add .",
        "GENERATE_COMMIT",
        "git push"
    ],
    "start_feature": [
        "git pull",
        "CREATE_BRANCH"
    ],
    "finish_feature": [
        "git add .",
        "GENERATE_COMMIT",
        "git push"
    ],
    "undo_everything": [
        "git reset --hard HEAD",
        "git clean -fd"
    ],
    "fresh_start": [
        "git add .",
        "GENERATE_COMMIT",
        "git stash"
    ],
}

def resolve_steps(steps: list, user_input: str) -> list:
    resolved = []
    for step in steps:
        if step == "GENERATE_COMMIT":
            resolved.append("__GENERATE_COMMIT__")
        elif step == "CREATE_BRANCH":
            match = re.search(r"called (.+)|named (.+)|branch (.+)", user_input.lower())
            name = (match.group(1) or match.group(2) or match.group(3)).strip() if match else "new-feature"
            resolved.append(f"git checkout -b {name}")
        else:
            resolved.append(step)
    return resolved

def load_history() -> list:
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history: list):
    try:
        with open(HISTORY_PATH, "w") as f:
            json.dump(history[-MAX_HISTORY:], f)
    except:
        pass

def clear_history():
    try:
        os.remove(HISTORY_PATH)
    except:
        pass

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("No API key found. Run 'gitbuddy setup' first.")
    return Groq(api_key=api_key)

def parse_command(user_input: str) -> str:
    text = user_input.strip()
    if text.lower().startswith("git "):
        return text

    history = load_history()
    client = get_client()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": text})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.1
    )

    result = response.choices[0].message.content.strip()

    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": result})
    save_history(history)

    return result