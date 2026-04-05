"""Tool group registration."""

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.tools import core, data, gwa, output, view

__all__ = ["register_all"]


def register_all(mcp: FastMCP, client: GsaComClient) -> None:
    """Register all tool groups."""
    core.register(mcp, client)
    data.register(mcp, client)
    output.register(mcp, client)
    view.register(mcp, client)
    gwa.register(mcp, client)
