import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.expanduser("~"), ".gitbuddy.env"))

HISTORY_PATH = os.path.join(os.path.expanduser("~"), ".gitbuddy_history.json")
MAX_HISTORY = 10

SYSTEM_PROMPT = """You are a Git command translator with memory of previous commands.
Convert natural language input into a single Git command.
Reply with ONLY the raw git command, nothing else.
No explanations, no markdown, no backticks.
Use previous commands as context to understand what the user wants next.

Examples:
"undo my last commit but keep changes" -> git reset --soft HEAD~1
"create a new branch called feature-login" -> git checkout -b feature-login
"show me what changed" -> git diff
"push to main" -> git push origin main
"now push it" -> git push origin main
"switch to it" -> git checkout feature-login
"""

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

    command = response.choices[0].message.content.strip()

    history.append({"role": "user", "content": text})
    history.append({"role": "assistant", "content": command})
    save_history(history)

    return command