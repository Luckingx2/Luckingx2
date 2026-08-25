from __future__ import annotations

from pathlib import Path

import yaml


def load_template(name: str, root: Path = Path("templates")) -> dict:
    path = root / f"{name}.yaml"
    if not path.is_file():
        raise ValueError(f"Unknown prompt model: {name}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def render_prompt(name: str, subject: str, root: Path = Path("templates")) -> str:
    template = load_template(name, root)
    sections = template["sections"]
    lines = [f"TOTAL DURATION: {template.get('duration', 'user-defined')}"]
    for section in sections:
        value = subject if section["name"] in {"SUBJECT", "SUBJECT & ACTION"} else section["guidance"]
        lines.extend(("", f"[{section['name']}]", value))
    return "\n".join(lines)

