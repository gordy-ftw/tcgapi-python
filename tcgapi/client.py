"""Sync TCGApi client."""

from __future__ import annotations

from typing import Any

import httpx

from ._transport import _BaseTransport
from .resources.bulk import BulkResource
from .resources.cards import CardsResource
from .resources.export import ExportResource
from .resources.games import GamesResource
from .resources.keys import KeysResource
from .resources.prices import PricesResource
from .resources.search import SearchResource
from .resources.sets import SetsResource
from .resources.usage import UsageResource


class TCGApi(_BaseTransport):
    """Synchronous client. Backed by httpx.Client.

    Get a key at https://tcgapi.dev/dashboard. If `api_key` is omitted,
    the client reads from the `TCGAPI_KEY` environment variable.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = None,
        user_agent: str | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout, user_agent=user_agent)
        self._client = client or httpx.Client(timeout=self.timeout)
        self._owns_client = client is None

        self.games = GamesResource(self)
        self.sets = SetsResource(self)
        self.cards = CardsResource(self)
        self.search = SearchResource(self)
        self.prices = PricesResource(self)
        self.bulk = BulkResource(self)
        self.export = ExportResource(self)
        self.keys = KeysResource(self)
        self.usage = UsageResource(self)

    def _request(self, method: str, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        resp = self._client.request(
            method,
            self.base_url + path,
            params=self._clean_params(params),
            headers=self._headers(),
        )
        return self._handle_response(resp)

    def _request_raw(self, method: str, path: str, params: dict[str, Any] | None = None) -> str:
        resp = self._client.request(
            method,
            self.base_url + path,
            params=self._clean_params(params),
            headers=self._headers(),
        )
        if resp.is_error:
            self._handle_response(resp)  # raises
        return resp.text

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "TCGApi":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
