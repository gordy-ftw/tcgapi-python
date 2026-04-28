"""UsageResource — /usage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import Response, UsageResponse
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi


class UsageResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def get(self) -> Response[UsageResponse]:
        body = self._client._request("GET", "/usage")
        return parse_response(UsageResponse, body)


class AsyncUsageResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def get(self) -> Response[UsageResponse]:
        body = await self._client._request("GET", "/usage")
        return parse_response(UsageResponse, body)
