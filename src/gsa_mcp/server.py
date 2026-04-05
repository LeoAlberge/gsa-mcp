"""MCP server entrypoint for GSA COM."""

from __future__ import annotations

import argparse
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from gsa_mcp.com_client import GsaComClient
from gsa_mcp.errors import GsaMcpError
from gsa_mcp.tools import register_all

LOGGER = logging.getLogger("gsa_mcp.server")


def _configure_logging() -> None:
    """Configure stderr logging so stdio JSON-RPC remains clean on stdout."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


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
    _configure_logging()
    parser = argparse.ArgumentParser(description="Run GSA MCP server over stdio.")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "sse"],
        help="MCP transport (stdio recommended for local Cursor integration).",
    )
    args = parser.parse_args()
    LOGGER.info("Starting GSA MCP server (transport=%s)...", args.transport)
    server = create_server()
    LOGGER.info("GSA MCP server ready; awaiting client messages.")
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
