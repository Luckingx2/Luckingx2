from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Settings:
    model: str
    max_tokens: int
    log_dir: Path


def load_settings(path: Path | None = None) -> Settings:
    config_path = path or Path("config/models.yaml")
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return Settings(
        model=os.getenv("AI_CONTENT_MODEL", "claude-opus-4-1"),
        max_tokens=int(raw.get("max_tokens", 8000)),
        log_dir=Path(os.getenv("AI_CONTENT_LOG_DIR", "logs")),
    )

