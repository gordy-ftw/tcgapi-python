"""BulkResource — /bulk/* endpoints. Auto-chunks oversized lists."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..models import BulkCard, BulkPriceRow, PriceHistoryPoint, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

BULK_PRICES_MAX = 500
BULK_CARDS_MAX = 100
BULK_HISTORY_MAX = 50

RangeLiteral = Literal["month", "quarter", "year", "all"]


def _ids(ids: list[int]) -> str:
    if not ids:
        raise ValueError("At least one card ID required")
    return ",".join(str(i) for i in ids)


class BulkResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def prices(self, ids: list[int]) -> Response[list[BulkPriceRow]]:
        if len(ids) <= BULK_PRICES_MAX:
            body = self._client._request("GET", "/bulk/prices", {"ids": _ids(ids)})
            return parse_response(list[BulkPriceRow], body)
        rows: list[BulkPriceRow] = []
        last: Response[list[BulkPriceRow]] | None = None
        for i in range(0, len(ids), BULK_PRICES_MAX):
            chunk = ids[i : i + BULK_PRICES_MAX]
            body = self._client._request("GET", "/bulk/prices", {"ids": _ids(chunk)})
            resp: Response[list[BulkPriceRow]] = parse_response(list[BulkPriceRow], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[BulkPriceRow]](data=rows, rate_limit=last.rate_limit if last else None)

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

    async def prices(self, ids: list[int]) -> Response[list[BulkPriceRow]]:
        if len(ids) <= BULK_PRICES_MAX:
            body = await self._client._request("GET", "/bulk/prices", {"ids": _ids(ids)})
            return parse_response(list[BulkPriceRow], body)
        rows: list[BulkPriceRow] = []
        last: Response[list[BulkPriceRow]] | None = None
        for i in range(0, len(ids), BULK_PRICES_MAX):
            chunk = ids[i : i + BULK_PRICES_MAX]
            body = await self._client._request("GET", "/bulk/prices", {"ids": _ids(chunk)})
            resp: Response[list[BulkPriceRow]] = parse_response(list[BulkPriceRow], body)
            rows.extend(resp.data)
            last = resp
        return Response[list[BulkPriceRow]](data=rows, rate_limit=last.rate_limit if last else None)

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
