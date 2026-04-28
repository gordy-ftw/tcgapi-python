"""Async TCGApi client. Mirror of the sync client surface."""

from __future__ import annotations

from typing import Any

import httpx

from ._transport import _BaseTransport
from .resources.bulk import AsyncBulkResource
from .resources.cards import AsyncCardsResource
from .resources.export import AsyncExportResource
from .resources.games import AsyncGamesResource
from .resources.keys import AsyncKeysResource
from .resources.prices import AsyncPricesResource
from .resources.search import AsyncSearchResource
from .resources.sets import AsyncSetsResource
from .resources.usage import AsyncUsageResource


class AsyncTCGApi(_BaseTransport):
    """Asynchronous client. Backed by httpx.AsyncClient."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        user_agent: str | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, user_agent=user_agent)
        self._client = client or httpx.AsyncClient(timeout=self.timeout)
        self._owns_client = client is None

        self.games = AsyncGamesResource(self)
        self.sets = AsyncSetsResource(self)
        self.cards = AsyncCardsResource(self)
        self.search = AsyncSearchResource(self)
        self.prices = AsyncPricesResource(self)
        self.bulk = AsyncBulkResource(self)
        self.export = AsyncExportResource(self)
        self.keys = AsyncKeysResource(self)
        self.usage = AsyncUsageResource(self)

    async def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = await self._client.request(
            method,
            self.base_url + path,
            params=self._clean_params(params),
            headers=self._headers(),
        )
        return self._handle_response(resp)

    async def _request_raw(self, method: str, path: str, params: dict[str, Any] | None = None) -> str:
        resp = await self._client.request(
            method,
            self.base_url + path,
            params=self._clean_params(params),
            headers=self._headers(),
        )
        if resp.is_error:
            self._handle_response(resp)  # raises
        return resp.text

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncTCGApi":
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()
