"""BulkResource — /bulk/* endpoints. Auto-chunks oversized lists."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..models import (
    BulkCard,
    BulkConditionRow,
    BulkPriceRow,
    ListingSupply,
    Meta,
    PriceHistoryPoint,
    Response,
)
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

BULK_PRICES_MAX = 500
BULK_CARDS_MAX = 100
BULK_HISTORY_MAX = 50
BULK_CONDITIONS_MAX = 500
BULK_SUPPLY_MAX = 500

RangeLiteral = Literal["month", "quarter", "year", "all"]
# Pro+; adds each row's eBay summary (1 credit plus 1 per card with eBay data).
BulkPricesIncludeLiteral = Literal["ebay"]


def _ids(ids: list[int]) -> str:
    if not ids:
        raise ValueError("At least one card ID required")
    return ",".join(str(i) for i in ids)


class BulkResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def prices(
        self, ids: list[int], *, include: BulkPricesIncludeLiteral | None = None
    ) -> Response[list[BulkPriceRow]]:
        if len(ids) <= BULK_PRICES_MAX:
            body = self._client._request("GET", "/bulk/prices", {"ids": _ids(ids), "include": include})
            return parse_response(list[BulkPriceRow], body)
        rows: list[BulkPriceRow] = []
        last: Response[list[BulkPriceRow]] | None = None
        credits: int | None = None
        for i in range(0, len(ids), BULK_PRICES_MAX):
            chunk = ids[i : i + BULK_PRICES_MAX]
            body = self._client._request("GET", "/bulk/prices", {"ids": _ids(chunk), "include": include})
            resp: Response[list[BulkPriceRow]] = parse_response(list[BulkPriceRow], body)
            rows.extend(resp.data)
            last = resp
            if resp.meta and resp.meta.credits_consumed is not None:
                credits = (credits or 0) + resp.meta.credits_consumed
        # With include, meta.credits_consumed is the total across chunks.
        meta = Meta(total=len(rows), credits_consumed=credits) if credits is not None else None
        return Response[list[BulkPriceRow]](
            data=rows, meta=meta, rate_limit=last.rate_limit if last else None
        )

    def cards(self, ids: list[int]) -> Response[list[BulkCard]]:
        if len(ids) <= BULK_CARDS_MAX:
            body = self._client._request("GET", "/bulk/cards", {"ids": _ids(ids)})
            return parse_response(list[BulkCard], body)
        rows: list[BulkCard] = []
        last: Response[list[BulkCard]] | None = None
        for i in range(0, len(ids), BULK_CARDS_MAX):
            chunk = ids[i : i + BULK_CARDS_MAX]
            body = self._client._request("GET", "/bulk/cards", {"ids": _ids(chunk)})
            resp: Response[list[BulkCard]] = parse_response(list[BulkCard], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[BulkCard]](data=rows, rate_limit=last.rate_limit if last else None)

    def conditions(self, ids: list[int]) -> Response[list[BulkConditionRow]]:
        # Pro+ only. Cache-only: cards without condition data yet are absent —
        # request them once via cards.conditions() to warm them.
        if len(ids) <= BULK_CONDITIONS_MAX:
            body = self._client._request("GET", "/bulk/conditions", {"ids": _ids(ids)})
            return parse_response(list[BulkConditionRow], body)
        rows: list[BulkConditionRow] = []
        last: Response[list[BulkConditionRow]] | None = None
        for i in range(0, len(ids), BULK_CONDITIONS_MAX):
            chunk = ids[i : i + BULK_CONDITIONS_MAX]
            body = self._client._request("GET", "/bulk/conditions", {"ids": _ids(chunk)})
            resp: Response[list[BulkConditionRow]] = parse_response(list[BulkConditionRow], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[BulkConditionRow]](
            data=rows, rate_limit=last.rate_limit if last else None
        )

    def supply(self, ids: list[int]) -> Response[list[ListingSupply]]:
        # Pro+ only. Listing supply (see cards.supply()) for up to 500 products per call,
        # ordered by card_id within each call. Products with no supply recorded yet are absent.
        if len(ids) <= BULK_SUPPLY_MAX:
            body = self._client._request("GET", "/bulk/supply", {"ids": _ids(ids)})
            return parse_response(list[ListingSupply], body)
        rows: list[ListingSupply] = []
        last: Response[list[ListingSupply]] | None = None
        for i in range(0, len(ids), BULK_SUPPLY_MAX):
            chunk = ids[i : i + BULK_SUPPLY_MAX]
            body = self._client._request("GET", "/bulk/supply", {"ids": _ids(chunk)})
            resp: Response[list[ListingSupply]] = parse_response(list[ListingSupply], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[ListingSupply]](data=rows, rate_limit=last.rate_limit if last else None)

    def history(
        self,
        ids: list[int],
        *,
        range: RangeLiteral | None = None,
        printing: str | None = None,
    ) -> Response[dict[str, list[PriceHistoryPoint]]]:
        params: dict[str, object | None] = {"range": range, "printing": printing}
        if len(ids) <= BULK_HISTORY_MAX:
            body = self._client._request("GET", "/bulk/history", {**params, "ids": _ids(ids)})
            return parse_response(dict[str, list[PriceHistoryPoint]], body)
        merged: dict[str, list[PriceHistoryPoint]] = {}
        last: Response[dict[str, list[PriceHistoryPoint]]] | None = None
        for i in range(0, len(ids), BULK_HISTORY_MAX):
            chunk = ids[i : i + BULK_HISTORY_MAX]
            body = self._client._request("GET", "/bulk/history", {**params, "ids": _ids(chunk)})
            resp: Response[dict[str, list[PriceHistoryPoint]]] = parse_response(
                dict[str, list[PriceHistoryPoint]], body
            )
            merged.update(resp.data)
            last = resp
        return Response[dict[str, list[PriceHistoryPoint]]](
            data=merged, rate_limit=last.rate_limit if last else None
        )


class AsyncBulkResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def prices(
        self, ids: list[int], *, include: BulkPricesIncludeLiteral | None = None
    ) -> Response[list[BulkPriceRow]]:
        if len(ids) <= BULK_PRICES_MAX:
            body = await self._client._request("GET", "/bulk/prices", {"ids": _ids(ids), "include": include})
            return parse_response(list[BulkPriceRow], body)
        rows: list[BulkPriceRow] = []
        last: Response[list[BulkPriceRow]] | None = None
        credits: int | None = None
        for i in range(0, len(ids), BULK_PRICES_MAX):
            chunk = ids[i : i + BULK_PRICES_MAX]
            body = await self._client._request(
                "GET", "/bulk/prices", {"ids": _ids(chunk), "include": include}
            )
            resp: Response[list[BulkPriceRow]] = parse_response(list[BulkPriceRow], body)
            rows.extend(resp.data)
            last = resp
            if resp.meta and resp.meta.credits_consumed is not None:
                credits = (credits or 0) + resp.meta.credits_consumed
        # With include, meta.credits_consumed is the total across chunks.
        meta = Meta(total=len(rows), credits_consumed=credits) if credits is not None else None
        return Response[list[BulkPriceRow]](
            data=rows, meta=meta, rate_limit=last.rate_limit if last else None
        )

    async def cards(self, ids: list[int]) -> Response[list[BulkCard]]:
        if len(ids) <= BULK_CARDS_MAX:
            body = await self._client._request("GET", "/bulk/cards", {"ids": _ids(ids)})
            return parse_response(list[BulkCard], body)
        rows: list[BulkCard] = []
        last: Response[list[BulkCard]] | None = None
        for i in range(0, len(ids), BULK_CARDS_MAX):
            chunk = ids[i : i + BULK_CARDS_MAX]
            body = await self._client._request("GET", "/bulk/cards", {"ids": _ids(chunk)})
            resp: Response[list[BulkCard]] = parse_response(list[BulkCard], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[BulkCard]](data=rows, rate_limit=last.rate_limit if last else None)

    async def conditions(self, ids: list[int]) -> Response[list[BulkConditionRow]]:
        # Pro+ only. Cache-only: cards without condition data yet are absent —
        # request them once via cards.conditions() to warm them.
        if len(ids) <= BULK_CONDITIONS_MAX:
            body = await self._client._request("GET", "/bulk/conditions", {"ids": _ids(ids)})
            return parse_response(list[BulkConditionRow], body)
        rows: list[BulkConditionRow] = []
        last: Response[list[BulkConditionRow]] | None = None
        for i in range(0, len(ids), BULK_CONDITIONS_MAX):
            chunk = ids[i : i + BULK_CONDITIONS_MAX]
            body = await self._client._request("GET", "/bulk/conditions", {"ids": _ids(chunk)})
            resp: Response[list[BulkConditionRow]] = parse_response(list[BulkConditionRow], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[BulkConditionRow]](
            data=rows, rate_limit=last.rate_limit if last else None
        )

    async def supply(self, ids: list[int]) -> Response[list[ListingSupply]]:
        # Pro+ only. Listing supply (see cards.supply()) for up to 500 products per call,
        # ordered by card_id within each call. Products with no supply recorded yet are absent.
        if len(ids) <= BULK_SUPPLY_MAX:
            body = await self._client._request("GET", "/bulk/supply", {"ids": _ids(ids)})
            return parse_response(list[ListingSupply], body)
        rows: list[ListingSupply] = []
        last: Response[list[ListingSupply]] | None = None
        for i in range(0, len(ids), BULK_SUPPLY_MAX):
            chunk = ids[i : i + BULK_SUPPLY_MAX]
            body = await self._client._request("GET", "/bulk/supply", {"ids": _ids(chunk)})
            resp: Response[list[ListingSupply]] = parse_response(list[ListingSupply], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[ListingSupply]](data=rows, rate_limit=last.rate_limit if last else None)

    async def history(
        self,
        ids: list[int],
        *,
        range: RangeLiteral | None = None,
        printing: str | None = None,
    ) -> Response[dict[str, list[PriceHistoryPoint]]]:
        params: dict[str, object | None] = {"range": range, "printing": printing}
        if len(ids) <= BULK_HISTORY_MAX:
            body = await self._client._request("GET", "/bulk/history", {**params, "ids": _ids(ids)})
            return parse_response(dict[str, list[PriceHistoryPoint]], body)
        merged: dict[str, list[PriceHistoryPoint]] = {}
        last: Response[dict[str, list[PriceHistoryPoint]]] | None = None
        for i in range(0, len(ids), BULK_HISTORY_MAX):
            chunk = ids[i : i + BULK_HISTORY_MAX]
            body = await self._client._request("GET", "/bulk/history", {**params, "ids": _ids(chunk)})
            resp: Response[dict[str, list[PriceHistoryPoint]]] = parse_response(
                dict[str, list[PriceHistoryPoint]], body
            )
            merged.update(resp.data)
            last = resp
        return Response[dict[str, list[PriceHistoryPoint]]](
            data=merged, rate_limit=last.rate_limit if last else None
        )
