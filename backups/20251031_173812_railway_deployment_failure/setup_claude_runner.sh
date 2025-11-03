#!/usr/bin/env bash
set -euo pipefail

if ! command -v conda >/dev/null 2>&1; then
  echo "Conda is not available. Open a new terminal that has 'conda' on the PATH."
  exit 1
fi

echo "Creating Conda env 'claude-run' with Python 3.12..."
conda env remove -n claude-run -y >/dev/null 2>&1 || true
conda create -n claude-run python=3.12 pip -y

echo "Installing Anthropic SDK..."
conda run -n claude-run pip install anthropic

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
            return f"(command succeeded with stderr only)\\n{result.stderr.strip()}"
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
        max_tokens=8_000,
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

            print(f\"Claude requested tool '{tool_name}' with command: {command}\")

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

echo
echo "Setup complete."
echo "Run me with:"
echo "conda run -n claude-run python scripts/claude_tool_runner.py"
