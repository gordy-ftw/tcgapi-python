"""GamesResource — /games endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import Game, Response, Set
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi


class GamesResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def list(self, *, page: int | None = None, per_page: int | None = None) -> Response[list[Game]]:
        body = self._client._request("GET", "/games", {"page": page, "per_page": per_page})
        return parse_response(list[Game], body)

    def get(self, slug: str | int) -> Response[Game]:
        body = self._client._request("GET", f"/games/{slug}")
        return parse_response(Game, body)

    def sets(self, slug: str | int, *, page: int | None = None, per_page: int | None = None) -> Response[list[Set]]:
        body = self._client._request("GET", f"/games/{slug}/sets", {"page": page, "per_page": per_page})
        return parse_response(list[Set], body)


class AsyncGamesResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def list(self, *, page: int | None = None, per_page: int | None = None) -> Response[list[Game]]:
        body = await self._client._request("GET", "/games", {"page": page, "per_page": per_page})
        return parse_response(list[Game], body)

    async def get(self, slug: str | int) -> Response[Game]:
        body = await self._client._request("GET", f"/games/{slug}")
        return parse_response(Game, body)

    async def sets(
        self, slug: str | int, *, page: int | None = None, per_page: int | None = None
    ) -> Response[list[Set]]:
        body = await self._client._request("GET", f"/games/{slug}/sets", {"page": page, "per_page": per_page})
        return parse_response(list[Set], body)
