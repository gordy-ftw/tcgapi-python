"""CardsResource — /cards endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..models import (
    BulkCard,
    Card,
    ConditionMeta,
    ConditionPrice,
    ListingSupply,
    Price,
    PriceHistoryPoint,
    Response,
    SupplyHistoryPoint,
    SupplyMeta,
)
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

RangeLiteral = Literal["month", "quarter", "year", "all"]
# Pro+; adds eBay sold prices (2 credits). "ebay_sales" also returns the sold listings.
PricesIncludeLiteral = Literal["ebay", "ebay_sales"]
HistoryIncludeLiteral = Literal["ebay"]


class CardsResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def get(self, card_id: int) -> Response[Card]:
        body = self._client._request("GET", f"/cards/{card_id}")
        return parse_response(Card, body)

    def prices(
        self,
        card_id: int,
        *,
        printing: str | None = None,
        include: PricesIncludeLiteral | None = None,
    ) -> Response[list[Price]]:
        body = self._client._request(
            "GET", f"/cards/{card_id}/prices", {"printing": printing, "include": include}
        )
        return parse_response(list[Price], body)

    def conditions(
        self, card_id: int, *, printing: str | None = None
    ) -> Response[list[ConditionPrice]]:
        # Pro+ only. `meta` is a ConditionMeta (cached/stale/as_of/condition_counts).
        body = self._client._request(
            "GET", f"/cards/{card_id}/prices/conditions", {"printing": printing}
        )
        return parse_response(list[ConditionPrice], body, meta_model=ConditionMeta)

    def supply(self, card_id: int) -> Response[ListingSupply]:
        # Pro+ only. Listing supply: listings, copies, sellers, a price ladder per printing
        # and days of supply. `meta` is a SupplyMeta (as_of). NotFoundError when the card
        # is unknown or has no supply recorded yet.
        body = self._client._request("GET", f"/cards/{card_id}/supply")
        return parse_response(ListingSupply, body, meta_model=SupplyMeta)

    def supply_history(self, card_id: int, *, days: int | None = None) -> Response[list[SupplyHistoryPoint]]:
        # Pro+ only. One point per day the listings were read, oldest first.
        # `days`: how far back, 1-3650 (API default 90). History starts 2026-10-27.
        body = self._client._request("GET", f"/cards/{card_id}/supply/history", {"days": days})
        return parse_response(list[SupplyHistoryPoint], body)

    def by_tcgplayer_id(self, tcgplayer_id: int) -> Response[BulkCard]:
        body = self._client._request("GET", f"/cards/tcgplayer/{tcgplayer_id}")
        return parse_response(BulkCard, body)

    def history(
        self,
        card_id: int,
        *,
        range: RangeLiteral | None = None,
        printing: str | None = None,
        include: HistoryIncludeLiteral | None = None,
    ) -> Response[list[PriceHistoryPoint]]:
        body = self._client._request(
            "GET",
            f"/cards/{card_id}/history",
            {"range": range, "printing": printing, "include": include},
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

    async def prices(
        self,
        card_id: int,
        *,
        printing: str | None = None,
        include: PricesIncludeLiteral | None = None,
    ) -> Response[list[Price]]:
        body = await self._client._request(
            "GET", f"/cards/{card_id}/prices", {"printing": printing, "include": include}
        )
        return parse_response(list[Price], body)

    async def conditions(
        self, card_id: int, *, printing: str | None = None
    ) -> Response[list[ConditionPrice]]:
        # Pro+ only. `meta` is a ConditionMeta (cached/stale/as_of/condition_counts).
        body = await self._client._request(
            "GET", f"/cards/{card_id}/prices/conditions", {"printing": printing}
        )
        return parse_response(list[ConditionPrice], body, meta_model=ConditionMeta)

    async def supply(self, card_id: int) -> Response[ListingSupply]:
        # Pro+ only. Listing supply: listings, copies, sellers, a price ladder per printing
        # and days of supply. `meta` is a SupplyMeta (as_of). NotFoundError when the card
        # is unknown or has no supply recorded yet.
        body = await self._client._request("GET", f"/cards/{card_id}/supply")
        return parse_response(ListingSupply, body, meta_model=SupplyMeta)

    async def supply_history(
        self, card_id: int, *, days: int | None = None
    ) -> Response[list[SupplyHistoryPoint]]:
        # Pro+ only. One point per day the listings were read, oldest first.
        # `days`: how far back, 1-3650 (API default 90). History starts 2026-10-27.
        body = await self._client._request("GET", f"/cards/{card_id}/supply/history", {"days": days})
        return parse_response(list[SupplyHistoryPoint], body)

    async def by_tcgplayer_id(self, tcgplayer_id: int) -> Response[BulkCard]:
        body = await self._client._request("GET", f"/cards/tcgplayer/{tcgplayer_id}")
        return parse_response(BulkCard, body)

    async def history(
        self,
        card_id: int,
        *,
        range: RangeLiteral | None = None,
        printing: str | None = None,
        include: HistoryIncludeLiteral | None = None,
    ) -> Response[list[PriceHistoryPoint]]:
        body = await self._client._request(
            "GET",
            f"/cards/{card_id}/history",
            {"range": range, "printing": printing, "include": include},
        )
        return parse_response(list[PriceHistoryPoint], body)

    async def history_detailed(
        self, card_id: int, *, printing: str | None = None
    ) -> Response[list[PriceHistoryPoint]]:
        body = await self._client._request(
            "GET", f"/cards/{card_id}/history/detailed", {"printing": printing}
        )
        return parse_response(list[PriceHistoryPoint], body)
