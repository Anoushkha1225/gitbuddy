import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.expanduser("~"), ".gitbuddy.env"))

SYSTEM_PROMPT = """You are a Git command translator.
Convert natural language input into a single Git command.
Reply with ONLY the raw git command, nothing else.
No explanations, no markdown, no backticks.

Examples:
"undo my last commit but keep changes" -> git reset --soft HEAD~1
"create a new branch called feature-login" -> git checkout -b feature-login
"show me what changed" -> git diff
"push to main" -> git push origin main

Make sure to ask everytime before running any commands.
"""

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("No API key found. Run 'gitbuddy setup' first.")
    return Groq(api_key=api_key)

def parse_command(user_input: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content.strip()