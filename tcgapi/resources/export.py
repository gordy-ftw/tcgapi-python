"""ExportResource — /export/set/{id}."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import BulkPriceRow, Response
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi


class ExportResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def set_json(self, set_id: int) -> Response[list[BulkPriceRow]]:
        body = self._client._request("GET", f"/export/set/{set_id}", {"format": "json"})
        return parse_response(list[BulkPriceRow], body)

    def set_csv(self, set_id: int) -> str:
        return self._client._request_raw("GET", f"/export/set/{set_id}", {"format": "csv"})


class AsyncExportResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def set_json(self, set_id: int) -> Response[list[BulkPriceRow]]:
        body = await self._client._request("GET", f"/export/set/{set_id}", {"format": "json"})
        return parse_response(list[BulkPriceRow], body)

    async def set_csv(self, set_id: int) -> str:
        return await self._client._request_raw("GET", f"/export/set/{set_id}", {"format": "csv"})
