from __future__ import annotations

from enum import StrEnum


class Action(StrEnum):
    LOCAL_ANALYSIS = "local_analysis"
    LOCAL_DRAFT = "local_draft"
    FILE_EDIT = "file_edit"
    GIT_COMMIT = "git_commit"
    GIT_PUSH = "git_push"
    PULL_REQUEST = "pull_request"
    EXTERNAL_PUBLISH = "external_publish"


EXPLICIT_APPROVAL = {
    Action.GIT_COMMIT,
    Action.GIT_PUSH,
    Action.PULL_REQUEST,
    Action.EXTERNAL_PUBLISH,
}


def require_approval(action: Action, approved: bool = False) -> None:
    if action in EXPLICIT_APPROVAL and not approved:
        raise PermissionError(f"Explicit approval required: {action.value}")

