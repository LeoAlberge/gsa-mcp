"""Data, list, and case/task tools."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.tools.common import call_status, call_value, handle_error


def _as_int_list(value: Any) -> list[int]:
    if isinstance(value, (list, tuple)):
        return [int(v) for v in value]
    return []


def register(mcp: FastMCP, client: GsaComClient) -> None:
    """Register data/list/case-task tools."""

    @mcp.tool()
    def gsa_node_coor(node_id: int) -> dict[str, object]:
        """Return node coordinates for a node reference."""
        try:
            result = client.call("NodeCoor", node_id, 0.0, 0.0, 0.0)
            if isinstance(result, (list, tuple)) and len(result) >= 4:
                status = int(result[0])
                xyz = {"x": float(result[1]), "y": float(result[2]), "z": float(result[3])}
                return {
                    "ok": status == 0,
                    "status": status,
                    "data": xyz,
                    "message": "OK" if status == 0 else "Node not found",
                }
            return {
                "ok": False,
                "status": None,
                "data": result,
                "message": "Unexpected NodeCoor return format",
            }
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_gen_node_at(x: float, y: float, z: float, tol: float = 1e-6) -> dict[str, object]:
        """Create/find node at coordinate."""
        try:
            return call_value(client, "Gen_NodeAt", x, y, z, tol)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_memb_num_elem(member_id: int) -> dict[str, object]:
        """Return number of elements for member."""
        try:
            return call_value(client, "MembNumElem", member_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_memb_elem_num(member_id: int, index: int) -> dict[str, object]:
        """Return element id for member+index."""
        try:
            return call_value(client, "MembElemNum", member_id, index)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_elem_memb_num(element_id: int) -> dict[str, object]:
        """Return member id associated with element."""
        try:
            return call_value(client, "ElemMembNum", element_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_node_connected_ent(entity_type: int, node_ref: int) -> dict[str, object]:
        """Return connected entity references for a node."""
        try:
            result = client.call("NodeConnectedEnt", entity_type, node_ref, [])
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                return {
                    "ok": int(result[0]) == 0,
                    "status": int(result[0]),
                    "data": {"entity_refs": _as_int_list(result[1])},
                    "message": "OK" if int(result[0]) == 0 else "Failed",
                }
            return {"ok": True, "status": None, "data": result, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_is_item_included(option: str, item_id: int, list_expr: str) -> dict[str, object]:
        """Check if item is in list expression."""
        try:
            return call_value(client, "IsItemIncluded", option, item_id, list_expr)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_entities_in_list(lst: str, list_type: int) -> dict[str, object]:
        """Resolve list expression to entities."""
        try:
            result = client.call("EntitiesInList", lst, list_type, [])
            if isinstance(result, (list, tuple)) and len(result) >= 3:
                status = int(result[0])
                payload = {"list_type": int(result[1]), "entities": _as_int_list(result[2])}
                return {
                    "ok": status == 0,
                    "status": status,
                    "data": payload,
                    "message": "OK" if status == 0 else "Failed",
                }
            return {"ok": True, "status": None, "data": result, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_highest_case(caseop: str) -> dict[str, object]:
        """Return highest case for case type L/A/C."""
        try:
            return call_value(client, "HighestCase", caseop)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_exist(caseop: str, case_id: int) -> dict[str, object]:
        """Check if case exists."""
        try:
            return call_value(client, "CaseExist", caseop, case_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_name(caseop: str, case_id: int) -> dict[str, object]:
        """Get case name."""
        try:
            return call_value(client, "CaseName", caseop, case_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_num_perm(caseop: str, case_id: int) -> dict[str, object]:
        """Get number of permutations for case."""
        try:
            return call_value(client, "CaseNumPerm", caseop, case_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_perm_desc(caseop: str, case_id: int, perm: int) -> dict[str, object]:
        """Get case permutation description."""
        try:
            return call_value(client, "CasePermDesc", caseop, case_id, perm)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_perm_string(caseop: str, case_id: int, perm: int) -> dict[str, object]:
        """Get case permutation string."""
        try:
            return call_value(client, "CasePermString", caseop, case_id, perm)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_perm_anal_factor(
        caseop: str, case_id: int, perm: int, analref: int
    ) -> dict[str, object]:
        """Get analysis factor for a case permutation."""
        try:
            return call_value(client, "CasePermAnalFactor", caseop, case_id, perm, analref)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_results_exist(caseop: str, case_id: int, perm: int = 0) -> dict[str, object]:
        """Check if results exist for case/permutation."""
        try:
            return call_value(client, "CaseResultsExist", caseop, case_id, perm)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_case_task(case_id: int) -> dict[str, object]:
        """Return parent analysis task for analysis case."""
        try:
            return call_value(client, "CaseTask", case_id)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_task_status(task_id: int) -> dict[str, object]:
        """Return analysis task status."""
        try:
            return call_status(
                client,
                "TaskStatus",
                task_id,
                status_map={
                    0: "Analysed",
                    1: "No file open",
                    2: "Task does not exist",
                    3: "Not analysed",
                },
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_design_task_status(task_id: int) -> dict[str, object]:
        """Return design task status."""
        try:
            return call_status(
                client,
                "DesignTaskStatus",
                task_id,
                status_map={
                    0: "OK",
                    1: "No file open",
                    2: "Task does not exist",
                    3: "Has results",
                    4: "Not designed/checked",
                },
            )
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_tool_update_elem_sections() -> dict[str, object]:
        """Sync element sections from members."""
        try:
            return call_value(client, "Tool_UpdateElemSections")
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_tool_reset_member_sections() -> dict[str, object]:
        """Sync member sections from elements."""
        try:
            return call_value(client, "Tool_ResetMemberSections")
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)

    @mcp.tool()
    def gsa_tool_get_ent_length(entity_id: int, entity_type: int) -> dict[str, object]:
        """Return entity length by id and entity enum type."""
        try:
            return call_value(client, "Tool_GetEntLength", entity_id, entity_type)
        except Exception as exc:  # noqa: BLE001
            return handle_error(exc)
