#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3.12 >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "Installing Python 3.12 with Homebrew..."
    brew install python@3.12
  else
    echo "Homebrew is not installed. Install it from https://brew.sh, then run this script again."
    exit 1
  fi
fi

PY312="$(command -v python3.12)"

echo "Creating virtual environment .claude-run ..."
$PY312 -m venv .claude-run

echo "Installing Anthropic SDK ..."
./.claude-run/bin/python -m pip install --upgrade pip
./.claude-run/bin/python -m pip install anthropic

echo "Writing scripts/claude_tool_runner.py ..."
mkdir -p scripts
cat <<'PY' > scripts/claude_tool_runner.py
#!/usr/bin/env python3
"""
scripts/claude_tool_runner.py
Runs any tool Claude asks for and immediately returns the tool_result block.
"""
import os
import shlex
import subprocess
from anthropic import Anthropic

def run_command(command_str: str) -> str:
    if not command_str:
        return "(no command provided)"
    try:
        result = subprocess.run(
            shlex.split(command_str),
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout.strip():
            return result.stdout.strip()
        if result.stderr.strip():
            return "(command succeeded with stderr only)\\n" + result.stderr.strip()
        return "(command succeeded with no output)"
    except subprocess.CalledProcessError as exc:
        return (
            f"(command failed with exit {exc.returncode})\\n"
            f"STDOUT:\\n{exc.stdout.strip() or '(empty)'}\\n"
            f"STDERR:\\n{exc.stderr.strip() or '(empty)'}"
        )

def dispatch_to_claude(history):
    client = Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        messages=history,
    )
    for block in response.content:
        if block["type"] == "text":
            print(f"Claude: {block['text']}\\n")
        elif block["type"] == "tool_use":
            tool_id = block["id"]
            tool_name = block["name"]
            tool_args = block.get("input", {})
            command = tool_args.get("command")
            print(f"Claude requested tool '{tool_name}' with command: {command}")
            output = run_command(command)
            tool_result = {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": [{"type": "text", "text": output}],
                    }
                ],
            }
            history.extend(
                [
                    {"role": "assistant", "content": [block]},
                    tool_result,
                ]
            )
            return dispatch_to_claude(history)
    return response

if __name__ == "__main__":
    if "CLAUDE_API_KEY" not in os.environ:
        raise SystemExit("Set CLAUDE_API_KEY before running this script.")
    conversation = [
        {
            "role": "user",
            "content": [{"type": "text", "text": "Hi Claude, let's test the tool runner."}],
        }
    ]
    dispatch_to_claude(conversation)
PY

chmod +x scripts/claude_tool_runner.py

cat <<MSG

=== Setup complete ===
Start the runner anytime with:
  ./.claude-run/bin/python scripts/claude_tool_runner.py

(If you prefer, you can 'source .claude-run/bin/activate' first, then run 'python scripts/claude_tool_runner.py'.)
MSG
