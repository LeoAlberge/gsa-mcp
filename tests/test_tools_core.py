from __future__ import annotations

from pathlib import Path

import pytest

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.errors import PlatformUnsupportedError, ValidationError
from gsa_mcp.tools.common import call_status
from gsa_mcp.validation import validate_save_path


class StubClient:
    def __init__(self, result):
        self._result = result

    def call(self, method_name, *args):  # noqa: ANN001
        return self._result


def test_call_status_success_payload() -> None:
    payload = call_status(StubClient(0), "Save", status_map={0: "OK", 1: "No file"})
    assert payload["ok"] is True
    assert payload["status"] == 0
    assert payload["message"] == "OK"


def test_call_status_failure_payload() -> None:
    payload = call_status(StubClient(1), "Save", status_map={0: "OK", 1: "No file"})
    assert payload["ok"] is False
    assert payload["status"] == 1
    assert payload["message"] == "No file"


def test_validate_save_path_requires_supported_extension(tmp_path: Path) -> None:
    invalid = tmp_path / "model.txt"
    with pytest.raises(ValidationError):
        validate_save_path(str(invalid))


def test_connect_non_windows_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    client = GsaComClient(dispatcher=lambda _: object())
    with pytest.raises(PlatformUnsupportedError):
        client.connect()
