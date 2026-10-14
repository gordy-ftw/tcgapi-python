"""IdentifyResource — POST /identify (card identification from a photo)."""

from __future__ import annotations

import os
from typing import IO, TYPE_CHECKING, Union

from ..models import IdentifyMeta, IdentifyResult, Response, ScanUsage
from ._base import parse_response

if TYPE_CHECKING:
    from ..async_client import AsyncTCGApi
    from ..client import TCGApi

# Raw bytes, a path to the photo, or an open binary file. JPEG, PNG or WebP, up to 8 MB.
Image = Union[bytes, "os.PathLike[str]", str, IO[bytes]]

# A read can take up to ~45s (one retry on a busy model host).
IDENTIFY_TIMEOUT = 60.0


def _files(image: Image) -> dict[str, tuple[str, bytes]]:
    if isinstance(image, bytes):
        data = image
    elif isinstance(image, (str, os.PathLike)):
        with open(image, "rb") as f:
            data = f.read()
    else:
        data = image.read()
    return {"image": ("photo", data)}


def _params(game: str | None, include_prices: bool) -> dict[str, object | None]:
    return {"game": game, "include": "prices" if include_prices else None}


class IdentifyResource:
    def __init__(self, client: "TCGApi") -> None:
        self._client = client

    def photo(self, image: Image, *, game: str | None = None, include_prices: bool = False) -> Response[IdentifyResult]:
        """Identify a card or sealed product from one photo.

        Uses one scan from the account's balance (25 free, then prepaid packs),
        apart from the daily request quota. A 402 with code SCAN_BALANCE_EMPTY
        means no scans are left. `meta` is an IdentifyMeta (scans_remaining).
        """
        body = self._client._request(
            "POST", "/identify", _params(game, include_prices), files=_files(image), timeout=IDENTIFY_TIMEOUT
        )
        return parse_response(IdentifyResult, body, meta_model=IdentifyMeta)

    def usage(self) -> Response[ScanUsage]:
        """Scan balance, scans per day for the last 30 days by outcome, and the
        trial/purchase ledger. Free: uses no scan and no daily quota."""
        return parse_response(ScanUsage, self._client._request("GET", "/identify/usage"))


class AsyncIdentifyResource:
    def __init__(self, client: "AsyncTCGApi") -> None:
        self._client = client

    async def photo(
        self, image: Image, *, game: str | None = None, include_prices: bool = False
    ) -> Response[IdentifyResult]:
        """Async variant of IdentifyResource.photo."""
        body = await self._client._request(
            "POST", "/identify", _params(game, include_prices), files=_files(image), timeout=IDENTIFY_TIMEOUT
        )
        return parse_response(IdentifyResult, body, meta_model=IdentifyMeta)

    async def usage(self) -> Response[ScanUsage]:
        """Async variant of IdentifyResource.usage."""
        return parse_response(ScanUsage, await self._client._request("GET", "/identify/usage"))
