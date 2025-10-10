#!/usr/bin/env python3
"""
scripts/claude_tool_runner.py
Runs any tool Claude asks for and immediately returns the tool_result block.
"""
import os
import shlex
import subprocess
from pathlib import Path
from getpass import getpass
from anthropic import Anthropic

KEY_FILE = Path.home() / ".claude_tool_runner_key"


def _persist_api_key(key: str) -> None:
    """Store the API key so future runs don't require re-entry."""
    try:
        KEY_FILE.write_text(key.strip() + "\n")
        KEY_FILE.chmod(0o600)
    except Exception as exc:
        print(f"Warning: unable to store API key for reuse ({exc}).")


def resolve_api_key() -> str:
    """Return the Claude API key from env, stored file, or interactive prompt."""
    env_key = os.environ.get("CLAUDE_API_KEY", "").strip()
    if env_key:
        _persist_api_key(env_key)
        return env_key

    if KEY_FILE.exists():
        try:
            stored = KEY_FILE.read_text().strip()
            if stored:
                return stored
        except Exception as exc:
            print(f"Warning: could not read stored API key ({exc}).")

    entered = getpass("Enter Claude API key (input hidden): ").strip()
    if not entered:
        return ""
    _persist_api_key(entered)
    return entered

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

def dispatch_to_claude(history, client):
    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=8000,
        messages=history,
    )
    for block in response.content:
        block_type = getattr(block, "type", None)

        if block_type == "text":
            text = getattr(block, "text", "")
            print(f"Claude: {text}\\n")
        elif block_type == "tool_use":
            tool_id = getattr(block, "id", "")
            tool_name = getattr(block, "name", "")
            tool_args = getattr(block, "input", {}) or {}
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
            return dispatch_to_claude(history, client)
    return response

if __name__ == "__main__":
    api_key = resolve_api_key()
    if not api_key:
        raise SystemExit("Claude API key required. Export CLAUDE_API_KEY or enter it when prompted.")

    client = Anthropic(api_key=api_key)
    conversation = [
        {
            "role": "user",
            "content": [{"type": "text", "text": "Hi Claude, let's test the tool runner."}],
        }
    ]
    dispatch_to_claude(conversation, client)
