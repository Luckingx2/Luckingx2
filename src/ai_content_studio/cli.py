from __future__ import annotations

import argparse

from .core.prompts import render_prompt


def main() -> None:
    parser = argparse.ArgumentParser(prog="ai-content")
    sub = parser.add_subparsers(dest="command", required=True)
    prompt = sub.add_parser("prompt")
    prompt.add_argument("--model", choices=("kling_3", "seedance", "higgsfield", "nanobanana_pro"), required=True)
    prompt.add_argument("--subject", required=True)
    args = parser.parse_args()
    if args.command == "prompt":
        print(render_prompt(args.model, args.subject))


if __name__ == "__main__":
    main()

