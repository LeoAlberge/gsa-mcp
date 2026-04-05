"""Minimal Windows smoke-test for GSA COM connectivity."""

from __future__ import annotations

import json
import platform
import sys

from gsa_mcp.com_client import GsaComClient


def main() -> int:
    if platform.system() != "Windows":
        print("This smoke test must run on Windows.", file=sys.stderr)
        return 2

    client = GsaComClient()
    output: dict[str, object] = {"ok": False}
    try:
        version = client.call("VersionString")
        new_status = client.call("NewFile")
        close_status = client.call("Close")
        output = {
            "ok": True,
            "version": version,
            "new_file_status": int(new_status) if isinstance(new_status, int) else new_status,
            "close_status": int(close_status) if isinstance(close_status, int) else close_status,
        }
        print(json.dumps(output, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001
        output["error"] = str(exc)
        print(json.dumps(output, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
