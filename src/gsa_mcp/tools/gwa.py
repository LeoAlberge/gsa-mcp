"""GwaCommand and utility function tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.tools.common import call_status, call_value, handle_error
from gsa_mcp.validation import require_non_empty, validate_gwa_command, validate_save_path


def register(mcp: FastMCP, client: GsaComClient) -> None:
    """Register GWA and utility tools."""

    @mcp.to ol()
    def gsa_gwa_command(command: str) -> dict[str, object]:
        """Execute raw GWA command string."""
        try:
            normalized = validate_gwa_command(command)
            return call_value(client, "GwaCommand", normalized)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_set_locale(locale: int) -> dict[str, object]:
        """Set locale for GwaCommand parsing."""
        try:
            return call_status(
                client, "SetLocale", locale, status_map={0: "OK", 1: "Invalid locale"}
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_num_arg(line: str) -> dict[str, object]:
        """Return number of arguments in a comma-separated line."""
        try:
            normalized = require_non_empty(line, "line")
            return call_value(client, "NumArg", normalized)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_arg(index: int, line: str) -> dict[str, object]:
        """Return argument string at zero-based index."""
        try:
            normalized = require_non_empty(line, "line")
            return call_value(client, "Arg", index, normalized)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_write_sid_tag_value(key: str, record: int, tag: str, value: str) -> dict[str, object]:
        """Write sid tag/value for a module record."""
        try:
            return call_status(
                client,
                "WriteSidTagValue",
                key,
                record,
                tag,
                value,
                status_map={0: "OK", 1: "Failed"},
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_get_sid_tag_value(key: str, record: int, tag: str) -> dict[str, object]:
        """Read sid value for module record+tag."""
        try:
            return call_value(client, "GetSidTagValue", key, record, tag)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_export_to_csv(
        pathname: str,
        num_point: int = 2,
        interesting_points: bool = False,
        combinations: bool = False,
        delimiter: str = ",",
    ) -> dict[str, object]:
        """Export model and results tables as CSV files."""
        try:
            normalized = validate_save_path(pathname)
            return call_status(
                client,
                "ExportToCsv",
                normalized,
                num_point,
                interesting_points,
                combinations,
                delimiter,
                status_map={0: "OK", 1: "No GSA file", 2: "Failure to export"},
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)
