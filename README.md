# gsa-mcp

Python MCP server for [Oasys GSA COM API](https://docs.oasys-software.com/structural/gsa/references/comautomation/), designed for Windows machines with GSA installed.

## Requirements

- Windows (GSA COM automation is Windows-only)
- Oasys GSA installed locally
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Setup (uv)

```bash
uv sync
```

Run lint, type-check, and tests:

```bash
uv run ruff check .
uv run mypy src
uv run pytest
```

## Run MCP server

Stdio (recommended for local Cursor integration):

```bash
uv run gsa-mcp
```

or:

```bash
uv run python -m gsa_mcp.server --transport stdio
```

## Cursor MCP configuration

Add an MCP server entry in your Cursor MCP config:

```json
{
  "mcpServers": {
    "gsa-com": {
      "command": "uv",
      "args": ["run", "gsa-mcp"],
      "cwd": "C:\\path\\to\\gsa-mcp"
    }
  }
}
```

## Tool coverage (v1)

The server exposes a broad surface of GSA COM families:

- Core model lifecycle and analysis (`Open`, `SaveAs`, `Analyse`, `Delete`, ...)
- Data/list and case/task helpers
- Output extraction (`Output_Init`, `Output_Extract`, array variants)
- View operations (print/save views, create/rescale views, template-based setters)
- Raw `GwaCommand` and utility helpers (`SetLocale`, `Arg`, `ExportToCsv`, sID helpers)

All tools return a normalized payload:

```json
{
  "ok": true,
  "status": 0,
  "data": {},
  "message": "OK"
}
```

## Important behavior notes

- COM function names are case-sensitive.
- `GwaCommand` is powerful and can modify model data directly; validate commands before use.
- If GSA is already open interactively, COM automation may be unstable (as documented by Oasys).

## Windows smoke test

Run a basic real-COM connectivity test:

```bash
uv run python scripts/smoke_windows.py
```

## Project layout

- `src/gsa_mcp/server.py`: MCP entrypoint and health tool
- `src/gsa_mcp/com_client.py`: COM connection/invocation wrapper
- `src/gsa_mcp/tools/`: grouped MCP tool registrations
- `tests/`: mocked unit tests (no GSA install required)
- `scripts/smoke_windows.py`: Windows-only runtime smoke test
