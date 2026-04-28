"""Official Python SDK for tcgapi.dev.

>>> from tcgapi import TCGApi
>>> tcg = TCGApi(api_key="tcg_live_...")
>>> tcg.games.get("pokemon").data.name
'Pokemon'

Async variant:

>>> from tcgapi import AsyncTCGApi
>>> async with AsyncTCGApi() as tcg:
...     resp = await tcg.search.cards("charizard")
"""

from .async_client import AsyncTCGApi
from .client import TCGApi
from .errors import (
    AuthError,
    NotFoundError,
    RateLimitError,
    TcgApiError,
    TierError,
)
from .models import (
    ApiKeyCreated,
    ApiKeySummary,
    BulkCard,
    BulkPriceRow,
    Card,
    CardWithPrice,
    Game,
    Meta,
    Price,
    PriceHistoryPoint,
    PriceMover,
    RateLimit,
    Response,
    Set,
    UsageResponse,
)

__version__ = "0.1.0"
__all__ = [
    "TCGApi",
    "AsyncTCGApi",
    # errors
    "TcgApiError",
    "AuthError",
    "TierError",
    "NotFoundError",
    "RateLimitError",
    # models
    "Game",
    "Set",
    "Card",
    "CardWithPrice",
    "Price",
    "PriceMover",
    "PriceHistoryPoint",
    "BulkCard",
    "BulkPriceRow",
    "ApiKeySummary",
    "ApiKeyCreated",
    "UsageResponse",
    "Meta",
    "RateLimit",
    "Response",
]
