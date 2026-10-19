"""Pydantic models for tcgapi responses. Mirrors openapi/spec.yaml."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class _Base(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class Game(_Base):
    id: int
    name: str
    slug: str
    tcgplayer_id: int
    priority: int | None = None
    set_count: int | None = None
    card_count: int | None = None
    image_url: str | None = None
    logo_url: str | None = None
    last_synced_at: str | None = None


class Set(_Base):
    id: int
    name: str
    slug: str | None = None
    tcgplayer_id: int
    abbreviation: str | None = None
    release_date: str | None = None
    card_count: int | None = None
    image_url: str | None = None
    set_icon_url: str | None = None
    game_name: str | None = None
    game_slug: str | None = None


class Card(_Base):
    id: int
    name: str
    clean_name: str | None = None
    number: str | None = None
    rarity: str | None = None
    image_url: str | None = None
    tcgplayer_id: int
    tcgplayer_url: str | None = None
    product_type: str | None = None
    foil_only: int | None = None
    game_name: str | None = None
    game_slug: str | None = None
    set_name: str | None = None
    set_slug: str | None = None
    custom_attributes: dict[str, Any] | None = None


class Price(_Base):
    card_id: int
    printing: str | None = None
    market_price: float | None = None
    # UTC date (YYYY-MM-DD) TCGPlayer last reported market_price. Older than the other
    # fields when the printing has had no market price recently (the last price is kept).
    market_price_as_of: str | None = None
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    buylist_price: float | None = None
    price_change_24h: float | None = None
    price_change_7d: float | None = None
    price_change_30d: float | None = None
    last_updated_at: str | None = None
    # ISO 8601 UTC time since which TCGPlayer has priced nothing for this product (the
    # row keeps the last prices reported and is not refreshed daily). None while priced.
    no_market_price_since: str | None = None
    # Sales velocity — Pro/Business tiers only; the API omits these below Pro.
    sales_volume: int | None = None
    avg_sales_price: float | None = None
    sales_as_of: str | None = None


class CardWithPrice(_Base):
    id: int
    name: str
    clean_name: str | None = None
    number: str | None = None
    rarity: str | None = None
    tcgplayer_id: int
    product_type: str | None = None
    foil_only: int | None = None
    total_listings: int | None = None
    printing: str | None = None
    market_price: float | None = None
    # UTC date (YYYY-MM-DD) TCGPlayer last reported market_price. Older than the other
    # fields when the printing has had no market price recently (the last price is kept).
    market_price_as_of: str | None = None
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    price_updated_at: str | None = None
    # ISO 8601 UTC time since which TCGPlayer has priced nothing for this product (the
    # row keeps the last prices reported and is not refreshed daily). None while priced.
    no_market_price_since: str | None = None
    image_url: str | None = None
    game_name: str | None = None
    game_slug: str | None = None
    set_name: str | None = None


class PriceMover(_Base):
    card_id: int
    name: str
    tcgplayer_id: int
    product_type: str | None = None
    foil_only: int | None = None
    set_name: str | None = None
    game_name: str | None = None
    game_slug: str | None = None
    printing: str | None = None
    market_price: float
    # UTC date (YYYY-MM-DD) TCGPlayer last reported market_price. Older than the other
    # fields when the printing has had no market price recently (the last price is kept).
    market_price_as_of: str | None = None
    price_change: float
    last_updated_at: str | None = None
    # ISO 8601 UTC time since which TCGPlayer has priced nothing for this product (the
    # row keeps the last prices reported and is not refreshed daily). None while priced.
    no_market_price_since: str | None = None
    image_url: str | None = None


class BulkPriceRow(_Base):
    card_id: int
    name: str | None = None
    tcgplayer_id: int | None = None
    product_type: str | None = None
    foil_only: int | None = None
    printing: str | None = None
    market_price: float | None = None
    # UTC date (YYYY-MM-DD) TCGPlayer last reported market_price. Older than the other
    # fields when the printing has had no market price recently (the last price is kept).
    market_price_as_of: str | None = None
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    buylist_price: float | None = None
    price_change_24h: float | None = None
    price_change_7d: float | None = None
    price_change_30d: float | None = None
    last_updated_at: str | None = None
    # ISO 8601 UTC time since which TCGPlayer has priced nothing for this product (the
    # row keeps the last prices reported and is not refreshed daily). None while priced.
    no_market_price_since: str | None = None
    image_url: str | None = None


class BulkCard(Card):
    prices: list[Price] = Field(default_factory=list)


class ConditionPrice(_Base):
    """Per-condition price floors for one (printing, condition) pair (Pro+)."""

    card_id: int
    printing: str | None = None
    # TCGPlayer condition grade, e.g. "Near Mint", "Lightly Played".
    condition: str
    language: str | None = None
    # Lowest listed item price for this printing + condition.
    low_price: float | None = None
    # Lowest listed price including shipping.
    lowest_with_shipping: float | None = None
    # Median of sampled shipping-inclusive prices. None when sample_count < 3 —
    # prefer this over low_price when pricing inventory (robust to $0.01 junk listings).
    median_with_shipping: float | None = None
    # Listings sampled for this row (not total market depth — see ConditionMeta.condition_counts).
    sample_count: int | None = None
    last_updated_at: str | None = None


class BulkConditionRow(ConditionPrice):
    """Row shape of /bulk/conditions — a ConditionPrice plus card identity."""

    name: str | None = None
    tcgplayer_id: int | None = None


class PriceHistoryPoint(_Base):
    date: str
    printing: str | None = None
    market_price: float | None = None
    low_price: float | None = None
    avg_sales_price: float | None = None
    sales_volume: int | None = None


class Meta(_Base):
    total: int | None = None
    page: int | None = None
    per_page: int | None = None
    has_more: bool | None = None


class ConditionMeta(Meta):
    """Meta for /cards/{id}/prices/conditions — cache/staleness signals."""

    # True when served from cache without a live refresh.
    cached: bool | None = None
    # Present (True) when rows are older than 24h and a live refresh
    # wasn't possible (quota or upstream failure).
    stale: bool | None = None
    as_of: str | None = None
    # Total live listings per condition across ALL printings
    # (only present on live-refreshed responses).
    condition_counts: dict[str, int] | None = None


class RateLimit(_Base):
    daily_limit: int
    daily_remaining: int
    daily_reset: str


class ApiKeySummary(_Base):
    id: str
    key_prefix: str
    name: str
    tier: str
    is_active: int
    total_requests: int
    created_at: str


class ApiKeyCreated(_Base):
    id: str
    key: str
    key_prefix: str
    name: str
    tier: str
    message: str | None = None


class UsageAccount(_Base):
    today_requests: int
    daily_limit: int
    daily_remaining: int


class UsageKey(_Base):
    id: str
    key_prefix: str
    name: str
    tier: str
    total_requests: int


class UsageSubscription(_Base):
    plan: str
    status: str


class UsageScans(_Base):
    """Photo identification scans (POST /v1/identify), billed apart from the daily quota."""

    balance: int
    trial_pending: bool


class UsageResponse(_Base):
    account: UsageAccount
    keys: list[UsageKey] = Field(default_factory=list)
    subscription: UsageSubscription | None = None
    scans: UsageScans | None = None


class IdentifySet(_Base):
    id: int
    name: str
    code: str | None = None


class IdentifyGame(_Base):
    slug: str
    name: str


class IdentifyMatch(_Base):
    # exact | partial (same number, set total on one side only) | unknown
    number: str
    name: float
    set: float
    # False when the card's title names an edition stamp the photo doesn't show, or the reverse
    edition: bool | None = None


class IdentifyPrice(_Base):
    printing: str
    market_price: float | None = None
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    price_change_7d: float | None = None
    price_change_30d: float | None = None
    last_updated_at: str | None = None
    # See Price.no_market_price_since.
    no_market_price_since: str | None = None


class IdentifyCandidate(_Base):
    card_id: int
    tcgplayer_id: int | None = None
    name: str
    number: str | None = None
    rarity: str | None = None
    product_type: str | None = None
    set: IdentifySet
    game: IdentifyGame
    image_url: str | None = None
    match: IdentifyMatch
    printings: list[str] = Field(default_factory=list)
    # The printing the photo points to (finish, 1st Edition stamp), when it decides one
    suggested_printing: str | None = None
    score: float
    # Only on the first candidate, with include_prices=True
    prices: list[IdentifyPrice] | None = None


class IdentifyGrade(_Base):
    company: str | None = None
    grade: str | None = None


class IdentifyReadable(_Base):
    name: bool
    number: bool
    set: bool


class IdentifyRead(_Base):
    """What the photo shows. Empty fields are unreadable, never guessed."""

    game: str
    name: str | None = None
    number: str | None = None
    set: str | None = None
    language: str | None = None
    kind: str
    product_type: str | None = None
    finish: str
    # The edition mark seen; None when clearly none; "unclear" when hidden
    stamp: str | None = None
    grade: IdentifyGrade | None = None
    readable: IdentifyReadable
    notes: str | None = None


class IdentifyResult(_Base):
    id: str
    # matched | ambiguous | retake | not_found | unsupported
    status: str
    message: str | None = None
    read: IdentifyRead | None = None
    candidates: list[IdentifyCandidate] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class IdentifyMeta(Meta):
    # "scan" or "x402"
    charged: str | None = None
    # Scans left after this one (API-key requests)
    scans_remaining: int | None = None


class ScanDay(_Base):
    """One UTC day of scans (GET /identify/usage)."""

    date: str
    # Scans used that day
    scans: int
    # Reads that failed on the reader's side and were refunded
    refunded: int = 0
    matched: int = 0
    ambiguous: int = 0
    retake: int = 0
    not_found: int = 0
    unsupported: int = 0


class ScanLedgerEntry(_Base):
    # "trial" or "purchase"
    reason: str
    scans: int
    amount_cents: int | None = None
    created_at: str


class ScanUsage(_Base):
    """GET /identify/usage: balance, the last 30 days (oldest first) and the trial/purchase ledger."""

    balance: int
    trial_pending: bool
    days: list[ScanDay] = Field(default_factory=list)
    ledger: list[ScanLedgerEntry] = Field(default_factory=list)


class Response(_Base, Generic[T]):
    """Wrapper returned by every method. Reach `.data`, `.meta`, `.rate_limit`."""

    data: T
    meta: Meta | None = None
    rate_limit: RateLimit | None = None
