"""CardmarketResource — /cardmarket/coverage."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import CardmarketCoverage, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi


class CardmarketResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def coverage(self) -> Response[CardmarketCoverage]:
        """Cards, printings and priced printings with a Cardmarket price, per game (recomputed daily)."""
        body = self._client._request("GET", "/cardmarket/coverage")
        return parse_response(CardmarketCoverage, body)


class AsyncCardmarketResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def coverage(self) -> Response[CardmarketCoverage]:
        """Async variant of CardmarketResource.coverage."""
        body = await self._client._request("GET", "/cardmarket/coverage")
        return parse_response(CardmarketCoverage, body)
