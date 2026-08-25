from __future__ import annotations

import argparse
import os

from ai_content_studio.core.approval import Action, require_approval


def validate_configuration() -> None:
    missing = [key for key in ("IG_USER_ID", "IG_ACCESS_TOKEN", "IMAGE_BASE_URL") if not os.getenv(key)]
    if missing:
        raise RuntimeError("Missing environment variables: " + ", ".join(missing))


def publish(*, confirmed: bool = False) -> None:
    require_approval(Action.EXTERNAL_PUBLISH, approved=confirmed)
    validate_configuration()
    raise NotImplementedError("Meta API adapter will be migrated only after a dry-run test plan is approved.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm-publish", action="store_true")
    args = parser.parse_args()
    publish(confirmed=args.confirm_publish)

