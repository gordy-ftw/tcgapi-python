"""KeysResource — /keys (session-cookie auth, mostly used from the dashboard)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import ApiKeySummary, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi


class KeysResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def list(self) -> Response[list[ApiKeySummary]]:
        body = self._client._request("GET", "/keys")
        return parse_response(list[ApiKeySummary], body)


class AsyncKeysResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def list(self) -> Response[list[ApiKeySummary]]:
        body = await self._client._request("GET", "/keys")
        return parse_response(list[ApiKeySummary], body)
