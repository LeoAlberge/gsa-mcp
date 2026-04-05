"""Shared helpers for tool wrappers."""

from __future__ import annotations

from typing import Any

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.errors import GsaMcpError

StatusMap = dict[int, str]


def payload(ok: bool, status: int | None, data: Any, message: str) -> dict[str, Any]:
    """Standard MCP tool payload."""
    return {"ok": ok, "status": status, "data": data, "message": message}


def call_status(
    client: GsaComClient,
    method_name: str,
    *args: Any,
    success_codes: tuple[int, ...] = (0,),
    status_map: StatusMap | None = None,
    data: Any = None,
) -> dict[str, Any]:
    """Invoke a COM method and interpret integer status return values."""
    result = client.call(method_name, *args)
    if not isinstance(result, int):
        return payload(ok=True, status=None, data=result if data is None else data, message="OK")
    ok = result in success_codes
    message = "OK"
    if status_map and result in status_map:
        message = status_map[result]
    elif not ok:
        message = f"{method_name} returned status {result}."
    return payload(ok=ok, status=result, data=data, message=message)


def call_value(client: GsaComClient, method_name: str, *args: Any) -> dict[str, Any]:
    """Invoke a COM method that returns non-status data."""
    result = client.call(method_name, *args)
    return payload(ok=True, status=None, data=result, message="OK")


def handle_error(exc: Exception) -> dict[str, Any]:
    """Convert exceptions to standard payload."""
    if isinstance(exc, GsaMcpError):
        return payload(ok=False, status=None, data=None, message=str(exc))
    return payload(ok=False, status=None, data=None, message=f"Unexpected error: {exc}")
