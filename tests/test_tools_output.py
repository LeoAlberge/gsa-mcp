from __future__ import annotations

from gsa_mcp.tools.common import call_status, call_value


class StubClient:
    def __init__(self, result):
        self._result = result

    def call(self, method_name, *args):  # noqa: ANN001
        return self._result


def test_output_init_status_mapping_success() -> None:
    payload = call_status(StubClient(0), "Output_Init", status_map={0: "OK", 5: "Invalid dataref"})
    assert payload["ok"] is True
    assert payload["message"] == "OK"


def test_output_init_status_mapping_failure() -> None:
    payload = call_status(StubClient(5), "Output_Init", status_map={0: "OK", 5: "Invalid dataref"})
    assert payload["ok"] is False
    assert payload["status"] == 5
    assert payload["message"] == "Invalid dataref"


def test_output_extract_returns_variant_value() -> None:
    payload = call_value(StubClient([1.0, 2.0, 3.0]), "Output_Extract", 1, 0)
    assert payload["ok"] is True
    assert payload["status"] is None
    assert payload["data"] == [1.0, 2.0, 3.0]
