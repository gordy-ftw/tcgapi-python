"""Shared HTTP transport for sync + async clients."""

from __future__ import annotations

import os
from typing import Any

import httpx

from .errors import make_error

DEFAULT_BASE_URL = "https://api.tcgapi.dev/v1"
DEFAULT_TIMEOUT = 30.0


class _BaseTransport:
    """Common transport plumbing — header construction, error handling."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        user_agent: str | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("TCGAPI_KEY")
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout if timeout is not None else DEFAULT_TIMEOUT
        self.user_agent = user_agent

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        if self.user_agent:
            headers["User-Agent"] = self.user_agent
        return headers

    @staticmethod
    def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
        if not params:
            return None
        return {k: v for k, v in params.items() if v is not None}

    @staticmethod
    def _handle_response(resp: httpx.Response) -> dict[str, Any]:
        try:
            body: dict[str, Any] | None = resp.json() if resp.content else None
        except ValueError:
            body = None

        if resp.is_error:
            err = (body or {}).get("error") if body else None
            # Standard tcgapi: error = {message, code}. x402 402: error = "string message".
            if isinstance(err, dict):
                message = err.get("message") or f"Request failed with status {resp.status_code}"
                code = err.get("code")
            elif isinstance(err, str):
                message = err
                code = None
            else:
                message = f"Request failed with status {resp.status_code}"
                code = None
            raise make_error(resp.status_code, message, code, body, resp.headers.get("Retry-After"))

        return body or {}
