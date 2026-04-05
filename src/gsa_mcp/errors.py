"""Domain errors used by GSA MCP."""

from __future__ import annotations


class GsaMcpError(Exception):
    """Base class for user-facing MCP errors."""


class PlatformUnsupportedError(GsaMcpError):
    """Raised when running on a non-Windows platform."""


class ComInitializationError(GsaMcpError):
    """Raised when GSA COM cannot be instantiated."""


class ComInvocationError(GsaMcpError):
    """Raised when invoking a COM method fails."""


class ValidationError(GsaMcpError):
    """Raised when user input is invalid."""
