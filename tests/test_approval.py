import pytest

from ai_content_studio.core.approval import Action, require_approval


def test_push_requires_explicit_approval():
    with pytest.raises(PermissionError):
        require_approval(Action.GIT_PUSH)


def test_local_draft_is_allowed():
    require_approval(Action.LOCAL_DRAFT)

