"""EbayResource — /ebay/coverage (public)."""

from __future__ import annotations

from typing import TYPE_CHECKING, overload

from ..models import EbayCoverage, EbayGameCoverage, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi


class EbayResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    @overload
    def coverage(self, game: None = None) -> Response[EbayCoverage]: ...
    @overload
    def coverage(self, game: str) -> Response[EbayGameCoverage]: ...
    def coverage(self, game: str | None = None) -> Response[EbayCoverage] | Response[EbayGameCoverage]:
        """How many cards have eBay sold prices, per game and how often they refresh.

        With `game` (a slug): that game plus per-set coverage; NotFoundError when the game
        has no eBay data. Public: no key needed, not counted against quota.
        """
        body = self._client._request("GET", "/ebay/coverage", {"game": game})
        if game is None:
            return parse_response(EbayCoverage, body)
        return parse_response(EbayGameCoverage, body)


class AsyncEbayResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    @overload
    async def coverage(self, game: None = None) -> Response[EbayCoverage]: ...
    @overload
    async def coverage(self, game: str) -> Response[EbayGameCoverage]: ...
    async def coverage(self, game: str | None = None) -> Response[EbayCoverage] | Response[EbayGameCoverage]:
        """Async variant of EbayResource.coverage."""
        body = await self._client._request("GET", "/ebay/coverage", {"game": game})
        if game is None:
            return parse_response(EbayCoverage, body)
        return parse_response(EbayGameCoverage, body)
