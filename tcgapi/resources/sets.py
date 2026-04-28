"""SetsResource — /sets endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator, Literal

from ..models import BulkPriceRow, CardWithPrice, Response, Set
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

SortLiteral = Literal["number", "price_asc", "price_desc", "name"]
TypeLiteral = Literal["Cards", "Sealed Products"]


class SetsResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def list(
        self,
        *,
        game: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response[list[Set]]:
        body = self._client._request("GET", "/sets", {"game": game, "page": page, "per_page": per_page})
        return parse_response(list[Set], body)

    def get(self, set_id: int) -> Response[Set]:
        body = self._client._request("GET", f"/sets/{set_id}")
        return parse_response(Set, body)

    def cards(
        self,
        set_id: int,
        *,
        type: TypeLiteral | None = None,
        sort: SortLiteral | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response[list[CardWithPrice]]:
        body = self._client._request(
            "GET",
            f"/sets/{set_id}/cards",
            {"type": type, "sort": sort, "page": page, "per_page": per_page},
        )
        return parse_response(list[CardWithPrice], body)

    def prices(self, set_id: int) -> Response[list[BulkPriceRow]]:
        body = self._client._request("GET", f"/sets/{set_id}/prices")
        return parse_response(list[BulkPriceRow], body)

    def iter_cards(self, set_id: int, **params: object) -> Iterator[CardWithPrice]:
        """Paginate through every card in a set, yielding one at a time."""
        page = int(params.pop("page", 1) or 1)  # type: ignore[arg-type]
        per_page = min(200, int(params.pop("per_page", 200) or 200))  # type: ignore[arg-type]
        while True:
            resp = self.cards(set_id, page=page, per_page=per_page, **params)  # type: ignore[arg-type]
            yield from resp.data
            if not resp.meta or not resp.meta.has_more:
                return
            page += 1


class AsyncSetsResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def list(
        self,
        *,
        game: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response[list[Set]]:
        body = await self._client._request("GET", "/sets", {"game": game, "page": page, "per_page": per_page})
        return parse_response(list[Set], body)

    async def get(self, set_id: int) -> Response[Set]:
        body = await self._client._request("GET", f"/sets/{set_id}")
        return parse_response(Set, body)

    async def cards(
        self,
        set_id: int,
        *,
        type: TypeLiteral | None = None,
        sort: SortLiteral | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response[list[CardWithPrice]]:
        body = await self._client._request(
            "GET",
            f"/sets/{set_id}/cards",
            {"type": type, "sort": sort, "page": page, "per_page": per_page},
        )
        return parse_response(list[CardWithPrice], body)

    async def prices(self, set_id: int) -> Response[list[BulkPriceRow]]:
        body = await self._client._request("GET", f"/sets/{set_id}/prices")
        return parse_response(list[BulkPriceRow], body)

    async def iter_cards(self, set_id: int, **params: object) -> AsyncIterator[CardWithPrice]:
        page = int(params.pop("page", 1) or 1)  # type: ignore[arg-type]
        per_page = min(200, int(params.pop("per_page", 200) or 200))  # type: ignore[arg-type]
        while True:
            resp = await self.cards(set_id, page=page, per_page=per_page, **params)  # type: ignore[arg-type]
            for card in resp.data:
                yield card
            if not resp.meta or not resp.meta.has_more:
                return
            page += 1
