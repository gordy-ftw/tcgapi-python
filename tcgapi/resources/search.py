"""SearchResource — /search."""

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator, Iterator, Literal

from ..models import CardWithPrice, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

SortLiteral = Literal["relevance", "price_asc", "price_desc", "name"]
TypeLiteral = Literal["Cards", "Sealed Products"]


def _params(
    q: str,
    game: str | None,
    set_id: int | None,
    rarity: str | None,
    type: TypeLiteral | None,
    printing: str | None,
    min_price: float | None,
    max_price: float | None,
    sort: SortLiteral | None,
    page: int | None,
    per_page: int | None,
) -> dict[str, object | None]:
    return {
        "q": q,
        "game": game,
        "set_id": set_id,
        "rarity": rarity,
        "type": type,
        "printing": printing,
        "min_price": min_price,
        "max_price": max_price,
        "sort": sort,
        "page": page,
        "per_page": per_page,
    }


class SearchResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def cards(
        self,
        q: str,
        *,
        game: str | None = None,
        set_id: int | None = None,
        rarity: str | None = None,
        type: TypeLiteral | None = None,
        printing: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort: SortLiteral | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response[list[CardWithPrice]]:
        body = self._client._request(
            "GET",
            "/search",
            _params(q, game, set_id, rarity, type, printing, min_price, max_price, sort, page, per_page),
        )
        return parse_response(list[CardWithPrice], body)

    def iter(self, q: str, **kwargs: object) -> Iterator[CardWithPrice]:
        page = int(kwargs.pop("page", 1) or 1)  # type: ignore[arg-type]
        per_page = min(200, int(kwargs.pop("per_page", 200) or 200))  # type: ignore[arg-type]
        while True:
            resp = self.cards(q, page=page, per_page=per_page, **kwargs)  # type: ignore[arg-type]
            yield from resp.data
            if not resp.meta or not resp.meta.has_more:
                return
            page += 1


class AsyncSearchResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def cards(
        self,
        q: str,
        *,
        game: str | None = None,
        set_id: int | None = None,
        rarity: str | None = None,
        type: TypeLiteral | None = None,
        printing: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort: SortLiteral | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Response[list[CardWithPrice]]:
        body = await self._client._request(
            "GET",
            "/search",
            _params(q, game, set_id, rarity, type, printing, min_price, max_price, sort, page, per_page),
        )
        return parse_response(list[CardWithPrice], body)

    async def iter(self, q: str, **kwargs: object) -> AsyncIterator[CardWithPrice]:
        page = int(kwargs.pop("page", 1) or 1)  # type: ignore[arg-type]
        per_page = min(200, int(kwargs.pop("per_page", 200) or 200))  # type: ignore[arg-type]
        while True:
            resp = await self.cards(q, page=page, per_page=per_page, **kwargs)  # type: ignore[arg-type]
            for card in resp.data:
                yield card
            if not resp.meta or not resp.meta.has_more:
                return
            page += 1
