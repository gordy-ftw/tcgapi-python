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
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    buylist_price: float | None = None
    price_change_24h: float | None = None
    price_change_7d: float | None = None
    price_change_30d: float | None = None
    last_updated_at: str | None = None
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
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    price_updated_at: str | None = None
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
    price_change: float
    last_updated_at: str | None = None
    image_url: str | None = None


class BulkPriceRow(_Base):
    card_id: int
    name: str | None = None
    tcgplayer_id: int | None = None
    product_type: str | None = None
    foil_only: int | None = None
    printing: str | None = None
    market_price: float | None = None
    low_price: float | None = None
    median_price: float | None = None
    lowest_with_shipping: float | None = None
    buylist_price: float | None = None
    price_change_24h: float | None = None
    price_change_7d: float | None = None
    price_change_30d: float | None = None
    last_updated_at: str | None = None
    image_url: str | None = None


class BulkCard(Card):
    prices: list[Price] = Field(default_factory=list)


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


class UsageResponse(_Base):
    account: UsageAccount
    keys: list[UsageKey] = Field(default_factory=list)
    subscription: UsageSubscription | None = None


class Response(_Base, Generic[T]):
    """Wrapper returned by every method. Reach `.data`, `.meta`, `.rate_limit`."""

    data: T
    meta: Meta | None = None
    rate_limit: RateLimit | None = None
