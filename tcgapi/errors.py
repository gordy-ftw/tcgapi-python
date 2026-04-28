"""Typed exceptions for tcgapi responses."""

from __future__ import annotations

from typing import Any


class TcgApiError(Exception):
    """Base exception for all tcgapi errors."""

    def __init__(
        self,
        message: str,
        status: int,
        code: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code or f"HTTP_{status}"
        self.body = body


class AuthError(TcgApiError):
    """401 — invalid or missing API key."""

    def __init__(self, message: str = "Invalid or missing API key", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, 401, "UNAUTHORIZED", body)


class TierError(TcgApiError):
    """403 — endpoint requires a higher tier than the current key has."""

    def __init__(self, message: str = "Tier upgrade required", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, 403, "TIER_REQUIRED", body)


class NotFoundError(TcgApiError):
    """404 — resource not found."""

    def __init__(self, message: str = "Resource not found", body: dict[str, Any] | None = None) -> None:
        super().__init__(message, 404, "NOT_FOUND", body)


class RateLimitError(TcgApiError):
    """429 — daily request limit reached."""

    def __init__(
        self,
        message: str = "Daily request limit reached",
        retry_after: int | None = None,
        body: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, 429, "RATE_LIMITED", body)
        self.retry_after = retry_after


def make_error(
    status: int,
    message: str,
    code: str | None,
    body: dict[str, Any] | None,
    retry_after: str | None,
) -> TcgApiError:
    if status == 401:
        return AuthError(message, body)
    if status == 403:
        return TierError(message, body)
    if status == 404:
        return NotFoundError(message, body)
    if status == 429:
        ra: int | None
        try:
            ra = int(retry_after) if retry_after else None
        except (TypeError, ValueError):
            ra = None
        return RateLimitError(message, ra, body)
    return TcgApiError(message, status, code, body)
