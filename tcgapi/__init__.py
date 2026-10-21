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
    BulkConditionRow,
    BulkPriceRow,
    Card,
    CardWithPrice,
    ConditionMeta,
    ConditionPrice,
    EbayHistoryGrade,
    EbayHistoryPoint,
    EbaySale,
    EbaySlabGrade,
    EbayStats,
    EbaySummary,
    Game,
    IdentifyCandidate,
    IdentifyMeta,
    IdentifyRead,
    IdentifyResult,
    Meta,
    Price,
    PriceHistoryPoint,
    PriceMover,
    RateLimit,
    Response,
    ScanDay,
    ScanLedgerEntry,
    ScanUsage,
    Set,
    UsageResponse,
    UsageScans,
)

__version__ = "0.10.0"
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
    "IdentifyResult",
    "IdentifyCandidate",
    "IdentifyRead",
    "IdentifyMeta",
    "UsageScans",
    "ScanUsage",
    "ScanDay",
    "ScanLedgerEntry",
    "Set",
    "Card",
    "CardWithPrice",
    "Price",
    "PriceMover",
    "PriceHistoryPoint",
    "EbayStats",
    "EbaySummary",
    "EbaySale",
    "EbayHistoryPoint",
    "EbayHistoryGrade",
    "EbaySlabGrade",
    "BulkCard",
    "BulkPriceRow",
    "ConditionPrice",
    "BulkConditionRow",
    "ConditionMeta",
    "ApiKeySummary",
    "ApiKeyCreated",
    "UsageResponse",
    "Meta",
    "RateLimit",
    "Response",
]
