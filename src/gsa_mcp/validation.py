"""Input validation helpers."""

from __future__ import annotations

from pathlib import Path

from gsa_mcp.errors import ValidationError

_ALLOWED_SAVE_SUFFIXES = {".gwb", ".gwa", ".csv"}


def require_non_empty(value: str, field_name: str) -> str:
    """Ensure string value is not empty."""
    normalized = value.strip()
    if not normalized:
        raise ValidationError(f"{field_name} must not be empty.")
    return normalized


def validate_open_path(path: str) -> str:
    """Validate Open input path."""
    normalized = require_non_empty(path, "filename")
    p = Path(normalized)
    if not p.exists():
        raise ValidationError(f"File does not exist: {normalized}")
    return str(p)


def validate_save_path(path: str) -> str:
    """Validate SaveAs/Export path and extension."""
    normalized = require_non_empty(path, "filename")
    p = Path(normalized)
    if p.suffix.lower() not in _ALLOWED_SAVE_SUFFIXES:
        suffixes = ", ".join(sorted(_ALLOWED_SAVE_SUFFIXES))
        raise ValidationError(f"Invalid file extension '{p.suffix}'. Expected one of: {suffixes}.")
    return str(p)


def validate_gwa_command(command: str) -> str:
    """Basic guardrails for raw GWA commands."""
    normalized = require_non_empty(command, "command")
    if len(normalized) > 20000:
        raise ValidationError("command is too long.")
    if "\x00" in normalized:
        raise ValidationError("command contains invalid NULL character.")
    return normalized
