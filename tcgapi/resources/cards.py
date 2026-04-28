"""CardsResource — /cards endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..models import BulkCard, Card, Price, PriceHistoryPoint, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

RangeLiteral = Literal["month", "quarter", "year", "all"]


class CardsResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def get(self, card_id: int) -> Response[Card]:
        body = self._client._request("GET", f"/cards/{card_id}")
        return parse_response(Card, body)

    def prices(self, card_id: int, *, printing: str | None = None) -> Response[list[Price]]:
        body = self._client._request("GET", f"/cards/{card_id}/prices", {"printing": printing})
        return parse_response(list[Price], body)

    def by_tcgplayer_id(self, tcgplayer_id: int) -> Response[BulkCard]:
        body = self._client._request("GET", f"/cards/tcgplayer/{tcgplayer_id}")
        return parse_response(BulkCard, body)

    def history(
        self,
        card_id: int,
        *,
        range: RangeLiteral | None = None,
        printing: str | None = None,
    ) -> Response[list[PriceHistoryPoint]]:
        body = self._client._request(
            "GET", f"/cards/{card_id}/history", {"range": range, "printing": printing}
        )
        return parse_response(list[PriceHistoryPoint], body)

    def history_detailed(
        self, card_id: int, *, printing: str | None = None
    ) -> Response[list[PriceHistoryPoint]]:
        body = self._client._request(
            "GET", f"/cards/{card_id}/history/detailed", {"printing": printing}
        )
        return parse_response(list[PriceHistoryPoint], body)


class AsyncCardsResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def get(self, card_id: int) -> Response[Card]:
        body = await self._client._request("GET", f"/cards/{card_id}")
        return parse_response(Card, body)

    async def prices(self, card_id: int, *, printing: str | None = None) -> Response[list[Price]]:
        body = await self._client._request("GET", f"/cards/{card_id}/prices", {"printing": printing})
        return parse_response(list[Price], body)

    async def by_tcgplayer_id(self, tcgplayer_id: int) -> Response[BulkCard]:
        body = await self._client._request("GET", f"/cards/tcgplayer/{tcgplayer_id}")
        return parse_response(BulkCard, body)

    async def history(
        self,
        card_id: int,
        *,
        range: RangeLiteral | None = None,
        printing: str | None = None,
    ) -> Response[list[PriceHistoryPoint]]:
        body = await self._client._request(
            "GET", f"/cards/{card_id}/history", {"range": range, "printing": printing}
        )
        return parse_response(list[PriceHistoryPoint], body)

    async def history_detailed(
        self, card_id: int, *, printing: str | None = None
    ) -> Response[list[PriceHistoryPoint]]:
        body = await self._client._request(
            "GET", f"/cards/{card_id}/history/detailed", {"printing": printing}
        )
        return parse_response(list[PriceHistoryPoint], body)
