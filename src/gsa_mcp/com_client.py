"""Thin wrapper around GSA COM automation."""

from __future__ import annotations

import platform
import time
from collections.abc import Callable
from typing import Any

from gsa_mcp.errors import ComInitializationError, ComInvocationError, PlatformUnsupportedError

ComDispatchFactory = Callable[[str], Any]


class GsaComClient:
    """Connects to and invokes methods on GSA COM automation."""

    def __init__(
        self,
        prog_id: str = "Gsa.ComAuto",
        dispatcher: ComDispatchFactory | None = None,
        retries: int = 1,
        retry_delay_seconds: float = 0.25,
    ) -> None:
        self._prog_id = prog_id
        self._dispatcher = dispatcher
        self._retries = max(retries, 0)
        self._retry_delay_seconds = max(retry_delay_seconds, 0.0)
        self._com_obj: Any | None = None

    @property
    def is_connected(self) -> bool:
        """Return whether COM object is initialized."""
        return self._com_obj is not None

    def connect(self) -> None:
        """Create COM object if needed."""
        if self._com_obj is not None:
            return
        if platform.system() != "Windows":
            raise PlatformUnsupportedError("GSA COM is only supported on Windows.")
        dispatch = self._dispatcher or self._default_dispatch
        try:
            self._com_obj = dispatch(self._prog_id)
        except Exception as exc:  # noqa: BLE001 - COM exceptions are opaque.
            raise ComInitializationError(
                f"Unable to create COM object '{self._prog_id}'. Is GSA installed?"
            ) from exc

    def disconnect(self) -> None:
        """Release COM object."""
        self._com_obj = None

    def call(self, method_name: str, *args: Any) -> Any:
        """Call a COM method with a small retry loop for transient failures."""
        self.connect()
        assert self._com_obj is not None
        attempts = self._retries + 1
        last_exc: Exception | None = None
        for attempt in range(attempts):
            try:
                method = getattr(self._com_obj, method_name)
                return method(*args)
            except Exception as exc:  # noqa: BLE001 - COM exceptions are opaque.
                last_exc = exc
                if attempt + 1 < attempts:
                    time.sleep(self._retry_delay_seconds)
                    continue
                break
        raise ComInvocationError(
            f"COM call failed for method '{method_name}' after {attempts} attempts."
        ) from last_exc

    @staticmethod
    def _default_dispatch(prog_id: str) -> Any:
        """Lazily import pywin32 on Windows only."""
        import win32com.client  # type: ignore[import-untyped]

        return win32com.client.Dispatch(prog_id)
