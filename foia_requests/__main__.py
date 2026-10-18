"""Offline CLI; all outbound sends are forbidden."""
import argparse
import json
import sys
from .config import Config, ConfigurationError

COMMANDS = ("directory", "campaign", "draft", "review", "dispatch", "receipt", "response", "continue", "export")

def main(argv=None):
    parser = argparse.ArgumentParser(prog="foia-requests")
    parser.add_argument("--config", help="JSON configuration path")
    sub = parser.add_subparsers(dest="command")
    for name in COMMANDS:
        sub.add_parser(name)
    args = parser.parse_args(argv)
    try:
        cfg = Config.from_file(args.config) if args.config else Config()
    except ConfigurationError as exc:
        parser.error(str(exc))
    if args.command == "dispatch":
        print("Dispatch disabled; no authorized live transport", file=sys.stderr)
        return 2
    if args.command:
        print(json.dumps({"command": args.command, "mode": cfg.mode, "status": "not_implemented"}))
    else:
        parser.print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
