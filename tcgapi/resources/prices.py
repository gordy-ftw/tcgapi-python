"""PricesResource — /prices/top-movers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from ..models import PriceMover, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

DirectionLiteral = Literal["up", "down"]
PeriodLiteral = Literal["24h", "7d", "30d"]
TypeLiteral = Literal["Cards", "Sealed Products"]


class PricesResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def top_movers(
        self,
        *,
        game: str | None = None,
        direction: DirectionLiteral | None = None,
        period: PeriodLiteral | None = None,
        printing: str | None = None,
        type: TypeLiteral | None = None,
        limit: int | None = None,
    ) -> Response[list[PriceMover]]:
        body = self._client._request(
            "GET",
            "/prices/top-movers",
            {
                "game": game,
                "direction": direction,
                "period": period,
                "printing": printing,
                "type": type,
                "limit": limit,
            },
        )
        return parse_response(list[PriceMover], body)


class AsyncPricesResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def top_movers(
        self,
        *,
        game: str | None = None,
        direction: DirectionLiteral | None = None,
        period: PeriodLiteral | None = None,
        printing: str | None = None,
        type: TypeLiteral | None = None,
        limit: int | None = None,
    ) -> Response[list[PriceMover]]:
        body = await self._client._request(
            "GET",
            "/prices/top-movers",
            {
                "game": game,
                "direction": direction,
                "period": period,
                "printing": printing,
                "type": type,
                "limit": limit,
            },
        )
        return parse_response(list[PriceMover], body)
