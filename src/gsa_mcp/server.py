"""MCP server entrypoint for GSA COM."""

from __future__ import annotations

import argparse
from typing import Any

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.errors import GsaMcpError
from gsa_mcp.tools import register_all


def create_server() -> FastMCP:
    """Create FastMCP app and register tools."""
    mcp = FastMCP("gsa-com")
    client = GsaComClient()
    register_all(mcp, client)

    @mcp.tool()
    def gsa_health() -> dict[str, Any]:
        """Health check: validates COM availability and returns version."""
        try:
            version = client.call("VersionString")
            return {"ok": True, "status": 0, "data": {"version": version}, "message": "OK"}
        except Exception as exc:  # noqa: BLE001
            if isinstance(exc, GsaMcpError):
                return {"ok": False, "status": None, "data": None, "message": str(exc)}
            return {
                "ok": False,
                "status": None,
                "data": None,
                "message": f"Unexpected error: {exc}",
            }

    return mcp


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Run GSA MCP server over stdio.")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "sse"],
        help="MCP transport (stdio recommended for local Cursor integration).",
    )
    args = parser.parse_args()
    server = create_server()
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
