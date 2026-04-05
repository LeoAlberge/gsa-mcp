"""View COM function tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.tools.common import call_status, call_value, handle_error


def register(mcp: FastMCP, client: GsaComClient) -> None:
    """Register view tools."""

    @mcp.tool()
    def gsa_update_views() -> dict[str, object]:
        """Refresh all visible GSA views."""
        try:
            client.call("UpdateViews")
            return {"ok": True, "status": 0, "data": None, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_print_view(option: str) -> dict[str, object]:
        """Print graphics/output view(s)."""
        try:
            return call_status(
                client,
                "PrintView",
                option,
                status_map={0: "OK", 1: "No file open", 2: "Invalid argument"},
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_save_view_to_file(option: str, filetype: str) -> dict[str, object]:
        """Save graphics/output view(s) to file."""
        try:
            return call_status(
                client,
                "SaveViewToFile",
                option,
                filetype,
                status_map={0: "OK", 1: "No file open", 2: "Invalid argument"},
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_highest_view(option: str) -> dict[str, object]:
        """Return highest numbered view for option."""
        try:
            return call_value(client, "HighestView", option)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_view_exist(option: str, ref: int) -> dict[str, object]:
        """Return whether view exists."""
        try:
            return call_value(client, "ViewExist", option, ref)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_view_name(option: str, ref: int) -> dict[str, object]:
        """Return view name from option/ref."""
        try:
            return call_value(client, "ViewName", option, ref)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_view_ref_from_name(option: str, name: str) -> dict[str, object]:
        """Return view reference from name."""
        try:
            return call_value(client, "ViewRefFromName", option, name)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_create_new_view(name: str) -> dict[str, object]:
        """Create a new saved graphic view."""
        try:
            return call_value(client, "CreateNewView", name)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_set_view_base_settings(view_id: int, saved_view_gwa: str) -> dict[str, object]:
        """Apply base settings from template GWA record."""
        try:
            return call_status(client, "SetViewBaseSettings", view_id, saved_view_gwa)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_set_view_contour(view_id: int, dataref: int, saved_view_gwa: str) -> dict[str, object]:
        """Apply contour settings and output dataref to view."""
        try:
            return call_status(client, "SetViewContour", view_id, dataref, saved_view_gwa)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_set_view_labels(view_id: int, saved_view_gwa: str) -> dict[str, object]:
        """Apply label settings from template GWA record."""
        try:
            return call_status(client, "SetViewLabels", view_id, saved_view_gwa)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_set_view_diagram(view_id: int, dataref: int, saved_view_gwa: str) -> dict[str, object]:
        """Apply diagram settings and output dataref to view."""
        try:
            return call_status(client, "SetViewDiagram", view_id, dataref, saved_view_gwa)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_rescale_view_to_fit(view_id: int) -> dict[str, object]:
        """Scale view extents to fit."""
        try:
            return call_status(client, "RescaleViewToFit", view_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_rescale_view_data(view_id: int) -> dict[str, object]:
        """Rescale contour/diagram data extents for view."""
        try:
            return call_status(client, "RescaleViewData", view_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)
