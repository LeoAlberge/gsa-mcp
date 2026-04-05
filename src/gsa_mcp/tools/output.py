"""Output COM function tools."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.tools.common import call_status, call_value, handle_error


def register(mcp: FastMCP, client: GsaComClient) -> None:
    """Register output tools."""

    @mcp.tool()
    def gsa_output_init(
        flags: int,
        axis: str,
        case: str,
        dataref: int,
        num1dpos: int = 0,
    ) -> dict[str, object]:
        """Initialize output API."""
        try:
            return call_status(
                client,
                "Output_Init",
                flags,
                axis,
                case,
                dataref,
                num1dpos,
                status_map={
                    0: "OK",
                    1: "No file open",
                    3: "Invalid axis",
                    4: "Invalid case",
                    5: "Invalid dataref",
                },
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_set_stage(stage: int = 0) -> dict[str, object]:
        """Set output stage."""
        try:
            return call_status(
                client,
                "Output_SetStage",
                stage,
                status_map={0: "OK", 1: "No file open", 2: "Output_Init not called"},
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_data_title(flags: int = 1) -> dict[str, object]:
        """Return title for initialized output data reference."""
        try:
            return call_value(client, "Output_DataTitle", flags)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_is_dataref(flags: int) -> dict[str, object]:
        """Check dataref characteristics from Output_Init."""
        try:
            return call_value(client, "Output_IsDataRef", flags)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_unit_string() -> dict[str, object]:
        """Return units string from Output_Init context."""
        try:
            return call_value(client, "Output_UnitString")
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_unit_factor() -> dict[str, object]:
        """Return SI-to-model unit conversion factor."""
        try:
            return call_value(client, "Output_UnitFactor")
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_data_exist(entity_id: int) -> dict[str, object]:
        """Check if initialized output data exists for id."""
        try:
            return call_value(client, "Output_DataExist", entity_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_num_elem_pos(entity_id: int) -> dict[str, object]:
        """Return number of element/member result positions."""
        try:
            return call_value(client, "Output_NumElemPos", entity_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_1d_elem_pos(pos: int) -> dict[str, object]:
        """Return normalized 1D position for index."""
        try:
            return call_value(client, "Output_1DElemPos", pos)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_extract(entity_id: int, pos: int = 0) -> dict[str, object]:
        """Extract initialized output value for entity and position."""
        try:
            return call_value(client, "Output_Extract", entity_id, pos)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_extract_cur_perm() -> dict[str, object]:
        """Get envelope permutation of last Output_Extract result."""
        try:
            return call_value(client, "Output_Extract_CurPerm")
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_init_arr(
        flags: int,
        axis: str,
        case: str,
        header: int,
        num1dpos: int = 0,
    ) -> dict[str, object]:
        """Initialize array output API."""
        try:
            return call_status(
                client,
                "Output_Init_Arr",
                flags,
                axis,
                case,
                header,
                num1dpos,
                status_map={
                    0: "OK",
                    1: "No file open",
                    3: "Invalid axis",
                    4: "Invalid case",
                    5: "Invalid header",
                },
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_extract_arr(entity_id: int) -> dict[str, object]:
        """Extract array output data for entity."""
        try:
            result: Any = client.call("Output_Extract_Arr", entity_id, [], 0)
            return {"ok": True, "status": 0, "data": result, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_output_extract_cut_assembly(
        assembly_ref: int,
        avg2d_stress: bool,
        disp: bool,
        case: str,
        axis: str,
    ) -> dict[str, object]:
        """Extract cut assembly forces/displacements."""
        try:
            result = client.call(
                "Output_Extract_CutAssembly",
                assembly_ref,
                avg2d_stress,
                disp,
                case,
                axis,
                [],
            )
            return {"ok": True, "status": 0, "data": result, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)
