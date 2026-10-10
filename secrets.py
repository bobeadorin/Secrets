#!/usr/bin/env python3
import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "secrets.json")

# ANSI Color Codes for terminal formatting
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def load_secrets():
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {}

def save_secrets(secrets):
    with open(FILE_PATH, "w") as f:
        json.dump(secrets, f, indent=4)

def parse_value(value_str: str):
    """Parses a string into a native Python type (int, float, dict, list, bool, null).

    If parsing fails, returns the string as-is with preserved lines.
    """
    try:
        return json.loads(value_str)
    except (json.JSONDecodeError, TypeError):
        return value_str.replace("\\n", "\n")

def format_value(value):
    """Formats values nicely for terminal output (handles multiline, dicts, lists)."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2)
    return str(value)

def add_secret(key, raw_value):
    secrets = load_secrets()
    parsed = parse_value(raw_value)
    secrets[key] = parsed
    save_secrets(secrets)
    print(f"{GREEN}✔️ Secret '{BOLD}{key}{RESET}{GREEN}' added/updated successfully.{RESET}")

def remove_secret(key):
    secrets = load_secrets()
    if key in secrets:
        del secrets[key]
        save_secrets(secrets)
        print(f"{GREEN}✔️ Secret '{BOLD}{key}{RESET}{GREEN}' removed.{RESET}")
    else:
        print(f"{RED}✖️ Key '{BOLD}{key}{RESET}{RED}' not found.{RESET}")

def get_secret(key):
    secrets = load_secrets()
    if key in secrets:
        formatted_val = format_value(secrets[key])
        print(f"{CYAN}{BOLD}{key}{RESET}:")
# Indent multiline output nicely
    for line in formatted_val.splitlines():
        print(f" {line}")
    else:
     print(f"{RED}✖️ Key '{BOLD}{key}{RESET}{RED}' not found.{RESET}")

def list_all():
    secrets = load_secrets()
    if not secrets:
        print(f"{YELLOW}No secrets stored yet.{RESET}")     
        return

    print(f"\n{BOLD}{'KEY':<25} VALUE{RESET}")
    print("─" * 60)

    items = list(secrets.items())
    for index, (key, value) in enumerate(items):
        formatted_val = format_value(value)
        lines = formatted_val.splitlines()

        # Print key and first line of value
        print(f"{CYAN}{key:<25}{RESET} {lines[0]}")

    # Print remaining lines of multiline values aligned under VALUE column
    for line in lines[1:]:
     print(f"{'':<26} {line}")

    # Draw a subtle dim separator between items (except after the last item)
    if index < len(items) - 1:
     print(f"{DIM}{'┈' * 60}{RESET}")

    print()

def list_keys():
    secrets = load_secrets()
    if not secrets:
        print(f"{YELLOW}No secrets stored yet.{RESET}")
        return

    print(f"\n{BOLD}Stored Keys ({len(secrets)}):{RESET}")
    print("─" * 30)
    for key in secrets.keys():
        print(f" • {CYAN}{key}{RESET}")
        print()

def main():
    print("Hello, World!")

    parser = argparse.ArgumentParser(
        description="🔑 Manage local secrets safely and cleanly.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-a", "--add", nargs=2, metavar=("KEY", "VALUE"), help="Add or update a secret")
    parser.add_argument("-r", "--remove", nargs=1, metavar=("KEY",), help="Remove a secret")
    parser.add_argument("-g", "--get", nargs=1, metavar=("KEY",), help="Get a secret value")
    parser.add_argument("--all", action="store_true", help="List all secrets with values")
    parser.add_argument("-k", "--keys", action="store_true", help="List all secret keys")

    args = parser.parse_args()

    match args:
        case argparse.Namespace(add=[key, val]):
            if val == "-":
                print(f"{YELLOW}Paste your code below, then press Enter and Ctrl+D:{RESET}")
                val = sys.stdin.read().strip()
            add_secret(key, val)
        case argparse.Namespace(remove=[key]):
            remove_secret(key)
        case argparse.Namespace(get=[key]):
            get_secret(key)
        case argparse.Namespace(all=True):
            list_all()
        case argparse.Namespace(keys=True):
            list_keys()
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()