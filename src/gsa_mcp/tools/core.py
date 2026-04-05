"""Core COM function tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.tools.common import call_status, call_value, handle_error
from gsa_mcp.validation import validate_open_path, validate_save_path

_OPEN_STATUS = {0: "OK", 1: "Failed to open"}
_SAVE_STATUS = {
    0: "OK",
    1: "No GSA file is open",
    2: "No default path is available",
    3: "Failed to save",
}
_SAVE_AS_STATUS = {
    0: "OK",
    1: "No GSA file is open",
    2: "Invalid file extension",
    3: "Failed to save",
}
_CLOSE_STATUS = {0: "OK", 1: "No GSA file is open"}
_ANALYSE_STATUS = {
    0: "Analysis attempted",
    1: "No GSA file is open",
    2: "Failed to attempt analysis",
}
_DELETE_STATUS = {0: "OK", 1: "No GSA file is open", 2: "Invalid option", 3: "Data not present"}
_DESIGN_STATUS = {
    0: "OK",
    1: "No GSA file open",
    2: "Design task does not exist",
    3: "Design task has results",
}


def register(mcp: FastMCP, client: GsaComClient) -> None:
    """Register core tools."""

    @mcp.tool()
    def gsa_version_string() -> dict[str, object]:
        """Return GSA version string."""
        try:
            return call_value(client, "VersionString")
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_new_file() -> dict[str, object]:
        """Open a new GSA model."""
        try:
            return call_status(client, "NewFile", status_map={0: "OK", 1: "Failed to open"})
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_open(filename: str) -> dict[str, object]:
        """Open GWB/GWA/CSV file."""
        try:
            normalized = validate_open_path(filename)
            return call_status(client, "Open", normalized, status_map=_OPEN_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_save() -> dict[str, object]:
        """Save current model to default path."""
        try:
            return call_status(client, "Save", status_map=_SAVE_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_save_as(filename: str) -> dict[str, object]:
        """Save current model to the supplied path."""
        try:
            normalized = validate_save_path(filename)
            return call_status(client, "SaveAs", normalized, status_map=_SAVE_AS_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_close() -> dict[str, object]:
        """Close current GSA model."""
        try:
            return call_status(client, "Close", status_map=_CLOSE_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_create_elements_from_members(member_list: str = "all") -> dict[str, object]:
        """Create or recreate elements from members list."""
        try:
            return call_status(
                client,
                "CreateElementsFromMembers",
                member_list,
                success_codes=(0, 4),
                status_map={
                    0: "OK",
                    1: "No GSA file is open",
                    2: "Terminated because model already has results",
                    3: "Invalid member list",
                    4: "Completed with meshing errors",
                },
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_analyse(task: int = -1) -> dict[str, object]:
        """Analyse a task, or all tasks when task <= 0."""
        try:
            return call_status(client, "Analyse", task, status_map=_ANALYSE_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_delete(option: str = "RESULTS") -> dict[str, object]:
        """Delete results based on option string."""
        try:
            return call_status(client, "Delete", option, status_map=_DELETE_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_design(task: int, option: int) -> dict[str, object]:
        """Run design task with design option enum value."""
        try:
            return call_status(client, "Design", task, option, status_map=_DESIGN_STATUS)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_display_window(display: bool) -> dict[str, object]:
        """Show or hide GSA main window."""
        try:
            client.call("DisplayGsaWindow", display)
            return {"ok": True, "status": 0, "data": {"display": display}, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)
