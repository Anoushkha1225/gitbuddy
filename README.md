# GitBuddy

An AI-powered Git assistant that runs commands from natural language. Requires Python 3.10+
and a free [Groq API key](https://console.groq.com).

```bash
pip install gitbuddy
gitbuddy setup
```

## Usage

```bash
gitbuddy run "undo my last commit but keep changes"
gitbuddy run "create a branch called feature-login"
gitbuddy run "show me what changed"
```

```bash
gitbuddy clone <url>
gitbuddy commit "your message"
gitbuddy branch create <name>
gitbuddy branch list
gitbuddy branch switch <name>
gitbuddy push <branch>
gitbuddy pull <branch>
```

## How it works

GitBuddy translates natural language into Git commands using Llama 3 via Groq.
Before running anything destructive, it shows you the command and asks for confirmation.

## Windows

After setup, add the alias to your PowerShell profile:

```bash
python -m gitbuddy.install
```

Then restart your terminal.

## Requirements

- Python 3.10+
- Free Groq API key — [console.groq.com](https://console.groq.com)

## License

MIT