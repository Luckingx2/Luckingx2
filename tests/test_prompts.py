from pathlib import Path

from ai_content_studio.core.prompts import render_prompt


ROOT = Path(__file__).parents[1] / "templates"


def test_kling_has_required_motion_controls():
    prompt = render_prompt("kling_3", "Hero sprints forward", ROOT)
    assert "[CHARACTER LOCK]" in prompt
    assert "[MOTION CONTROL]" in prompt
    assert "0.0 seconds" in prompt
    assert "[NEGATIVE RULES]" in prompt


def test_nanobanana_uses_four_section_format():
    prompt = render_prompt("nanobanana_pro", "A cinematic portrait", ROOT)
    assert "[SUBJECT & ACTION]" in prompt
    assert "[SCREEN CONTENT]" in prompt
    assert "[ENVIRONMENT]" in prompt
    assert "[STYLE]" in prompt

