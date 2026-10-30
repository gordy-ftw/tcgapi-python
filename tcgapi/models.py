"""Pydantic models for tcgapi responses. Mirrors openapi/spec.yaml."""

from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

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


class EbayStats(_Base):
    """eBay sold-price figures for one printing (ungraded) or one grade."""

    # Median sold price in the 30 days before as_of. None when nothing sold in the window.
    median_30d: float | None = None
    # Sales the median rests on.
    sales_30d: int | None = None
    # Latest sale, in or out of the window. On a Best Offer sale, the accepted offer.
    last_price: float | None = None
    last_sold: str | None = None


class EbaySale(_Base):
    """One eBay sold listing (only with include="ebay_sales")."""

    sold_date: str | None = None
    # Sold price; on a Best Offer sale, the accepted offer.
    price: float | None = None
    best_offer: bool | None = None
    # Asking price, on Best Offer sales.
    list_price: float | None = None
    # Grade label (e.g. "PSA 10"); None = ungraded.
    grade: str | None = None
    # Ungraded sales only, when the title states one (Near Mint ... Damaged).
    condition: str | None = None
    title: str | None = None
    url: str | None = None


class EbaySlabGrade(EbayStats):
    """identify.photo(include_ebay=True) on a graded slab: eBay figures for the grade on the label."""

    label: str | None = None


class EbaySummary(EbayStats):
    """eBay sold listings for one printing. Top-level figures are ungraded copies of every condition."""

    # How many of the 30 window days the stored ungraded sales cover (30 = complete;
    # lower in the first month of tracking).
    days: int | None = None
    # Every grade that has sold, keyed by label ("PSA 10", "CGC 10 Pristine", "BGS 9.5").
    graded: dict[str, EbayStats] = Field(default_factory=dict)
    # The same as days for graded sales, which start being tracked on their own date.
    graded_days: int | None = None
    # Date the sales were last read. The 30-day window ends here.
    as_of: str | None = None
    # Only with include="ebay_sales": the included sales in the 30-day window, newest first.
    sales: list[EbaySale] | None = None
    # Only from identify.photo(include_ebay=True) on a graded slab.
    slab_grade: EbaySlabGrade | None = None


class EbayHistoryGrade(_Base):
    median_30d: float | None = None
    sales_30d: int | None = None


class EbayHistoryPoint(_Base):
    """eBay sold median for the 30 days up to a history row's date."""

    median_30d: float | None = None
    sales_30d: int | None = None
    # How many of that day's 30 window days the stored ungraded sales cover (30 = complete).
    days: int | None = None
    # Only grades with a sale in that window. None when graded sales were not yet complete that day.
    graded: dict[str, EbayHistoryGrade] | None = Field(default_factory=dict)
    # The same as days for graded sales. Absent (None) when graded is None.
    graded_days: int | None = None
    # Only on days after the card's latest eBay read: those days carry that read's figures,
    # and this is its date (YYYY-MM-DD).
    as_of: str | None = None


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
    # eBay sold prices — only with include="ebay"/"ebay_sales" (Pro+, 2 credits);
    # None when there is no eBay data for the printing (or include was not set).
    ebay: EbaySummary | None = None


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
    # Only with include="ebay" (Pro+): the printing's eBay summary (without sales), or None.
    ebay: EbaySummary | None = None


class BulkCard(Card):
    prices: list[Price] = Field(default_factory=list)


class EbayCoverageRefresh(_Base):
    """Cards with eBay data by how often their sales are re-read."""

    daily: int | None = None
    # "3d" in the JSON
    three_day: int | None = Field(default=None, alias="3d")
    weekly: int | None = None
    monthly: int | None = None


class EbayCoverageGame(_Base):
    """GET /ebay/coverage: eBay sold-price coverage for one game."""

    # Game name
    game: str
    slug: str
    cards: int | None = None
    cards_with_ebay: int | None = None
    coverage_pct: float | None = None
    printings_with_ebay: int | None = None
    # Date of the newest eBay read in this game (YYYY-MM-DD).
    newest_as_of: str | None = None
    refresh: EbayCoverageRefresh | None = None


class EbayCoverageSet(_Base):
    set_id: int
    # Set name
    set: str | None = None
    cards: int | None = None
    cards_with_ebay: int | None = None
    coverage_pct: float | None = None


class EbayCoverageTotals(_Base):
    cards_with_ebay: int | None = None
    printings_with_ebay: int | None = None
    games: int | None = None


class EbayCoverage(_Base):
    """GET /ebay/coverage without game."""

    totals: EbayCoverageTotals
    games: list[EbayCoverageGame] = Field(default_factory=list)
    computed_at: str | None = None


class EbayGameCoverage(EbayCoverageGame):
    """GET /ebay/coverage?game={slug}: the game plus per-set coverage."""

    sets: list[EbayCoverageSet] = Field(default_factory=list)
    computed_at: str | None = None


class CardmarketPrice(_Base):
    """One printing's Cardmarket price (EUR) from Cardmarket's daily price guide.

    Each printing reads one Cardmarket product and one of its two series: regular, or foil (Pokemon:
    reverse holo). Where Cardmarket sells a card's editions as one product (Yu-Gi-Oh! 1st Edition +
    Unlimited) the card has one row with printing "All editions" and editions_blended True.
    """

    card_id: int
    printing: str
    editions_blended: bool = False
    price_trend: float | None = None
    avg_sell_price: float | None = None
    low_price: float | None = None  # lowest listing
    avg_1d: float | None = None
    avg_7d: float | None = None
    avg_30d: float | None = None
    currency: str = "EUR"
    last_updated_at: str | None = None  # date of the price guide the price came from
    cm_product_id: int
    cm_name: str
    cm_url: str | None = None
    cm_series: Literal["regular", "foil"]
    match_method: str | None = None


class CardmarketSetPrice(CardmarketPrice):
    """A row of GET /sets/{id}/prices/cardmarket: the price plus the card's name, number and TCGPlayer id."""

    name: str
    number: str | None = None
    tcgplayer_id: int | None = None


class CardmarketCoverageGame(_Base):
    game_id: int
    game: str | None = None
    game_slug: str | None = None
    cards: int
    printings: int
    priced_printings: int
    updated_at: str | None = None


class CardmarketCoverage(_Base):
    """GET /cardmarket/coverage: cards, printings and priced printings per game (recomputed daily)."""

    total_cards: int
    total_printings: int
    total_priced_printings: int
    price_guide_oldest: str | None = None
    price_guide_newest: str | None = None
    games: list[CardmarketCoverageGame] = Field(default_factory=list)


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
    # Only with include="ebay" on cards.history (Pro+, 2 credits). None before eBay sales
    # for the printing are complete, or when there is no eBay data.
    ebay: EbayHistoryPoint | None = None


class Meta(_Base):
    total: int | None = None
    page: int | None = None
    per_page: int | None = None
    has_more: bool | None = None
    # Credits charged on requests with an eBay include (2 on card prices/history;
    # 1 + cards with eBay data on bulk prices); absent otherwise.
    credits_consumed: int | None = None


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


class SupplyLadderStep(_Base):
    """Listings priced at or under one step of a printing's market price.

    Photo (custom) listings are left out — sellers list opened boxes and lots under
    sealed products.
    """

    # Step as a share of the market price: 0.9, 1.0, 1.1, 1.25 or 1.5.
    max_pct: float
    # Listing price (before shipping) at most this.
    max_price: float | None = None
    listings: int | None = None
    # Copies for sale across those listings.
    units: int | None = None
    sellers: int | None = None
    # False when only the cheapest 50 listings could be itemised, so listings, units and
    # sellers are lower bounds.
    exact: bool | None = None


class SupplyNearMarket(_Base):
    """The 110% ladder step summed over printings (each against its own market price)."""

    listings: int | None = None
    units: int | None = None
    # Summed per printing, so a seller listing two printings counts twice.
    sellers: int | None = None
    # True only when every printing's 110% step is exact.
    exact: bool | None = None


class SupplyLargestListing(_Base):
    """The listing with the most copies and its share (0-1) of all units."""

    quantity: int
    share: float | None = None


class SupplyPrinting(_Base):
    """One price ladder per printing that has a market price."""

    printing: str
    # The market price the ladder was measured against, as of last_updated_at.
    market_price: float | None = None
    ladder: list[SupplyLadderStep] = Field(default_factory=list)


class ListingSupply(_Base):
    """GET /cards/{id}/supply and rows of /bulk/supply (Pro+).

    How much of a product is for sale on TCGPlayer, from how many sellers, and how much
    of it sits near the market price. English listings priced for US shipping, read
    about every 3 days per product. Counts only; no seller identities.
    """

    card_id: int
    name: str | None = None
    tcgplayer_id: int | None = None
    # Active listings, all conditions and printings (photo listings included).
    listings: int | None = None
    # Copies for sale across all listings.
    units: int | None = None
    # Distinct sellers. None when it could not be counted.
    sellers: int | None = None
    # None when units are unknown or 0.
    largest_listing: SupplyLargestListing | None = None
    # Listings with exactly one copy.
    single_unit_listings: int | None = None
    # True when every listing was itemised (not just counted).
    complete: bool | None = None
    # near_market.listings == 0 means nobody is selling near the market price.
    # None when no printing has a market price.
    near_market: SupplyNearMarket | None = None
    # Copies sold over the last 30 days (all printings).
    sales_30d: int | None = None
    # sales_30d divided by the days with recorded sales. None with fewer than 7 recorded days.
    sales_per_day: float | None = None
    # units / sales_per_day. None when sales_per_day is None or 0.
    days_of_supply: float | None = None
    # near_market.units / sales_per_day.
    near_market_days_of_supply: float | None = None
    # Listings per condition, e.g. {"Near Mint": 40}.
    by_condition: dict[str, int] = Field(default_factory=dict)
    # Listings per printing, e.g. {"Normal": 205}.
    by_printing: dict[str, int] = Field(default_factory=dict)
    printings: list[SupplyPrinting] = Field(default_factory=list)
    last_updated_at: str | None = None


class SupplyMeta(Meta):
    """Meta for /cards/{id}/supply."""

    # When the listings were read (same as data.last_updated_at).
    as_of: str | None = None


class SupplyHistoryPoint(_Base):
    """One point of /cards/{id}/supply/history: one per day the listings were read.

    Reads happen about every 3 days per product; history starts 2026-10-27.
    """

    # YYYY-MM-DD (UTC).
    date: str
    listings: int | None = None
    units: int | None = None
    sellers: int | None = None
    # The near-market (110%) step; None when no printing had a market price that day.
    near_market_listings: int | None = None
    near_market_units: int | None = None
    near_market_sellers: int | None = None
    near_market_exact: bool | None = None


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
    # Only with include_ebay=True: the printing's eBay summary (without sales;
    # slab_grade on a slab), or None.
    ebay: EbaySummary | None = None


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
    # Only on the first candidate, with include_prices=True or include_ebay=True
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
