# Changelog

## 0.11.0

- `ebay.coverage()` (`GET /v1/ebay/coverage`, sync and async): how many cards and printings
  have eBay sold prices, per game, with coverage percentage, newest read and refresh
  cadence (`EbayCoverage`). `ebay.coverage(game)` returns that game with per-set coverage
  (`EbayGameCoverage`); `NotFoundError` when the game has no eBay data. Public: no key
  needed, not counted against quota. The refresh count keyed `"3d"` in the JSON is
  `refresh.three_day`. New models `EbayCoverage`, `EbayGameCoverage`, `EbayCoverageGame`,
  `EbayCoverageSet`, `EbayCoverageTotals`, `EbayCoverageRefresh`.

## 0.10.0

- `as_of` on `EbayHistoryPoint` (`cards.history()` with `include="ebay"`): present only on
  days after the card's latest eBay read, which carry that read's figures; `as_of` is its
  date (YYYY-MM-DD). Optional: `None` on other days.

## 0.9.0

- `days` and `graded_days` on `EbaySummary` (card prices, bulk prices, identify prices)
  and `EbayHistoryPoint`: how many of the 30 window days the stored ungraded / graded
  eBay sales cover (30 = complete; lower in the first month after a card's eBay
  tracking starts). Optional: `None` on older responses; on history points
  `graded_days` is `None` when `graded` is.
- `EbayHistoryPoint.graded` can now be `None` (graded sales not yet complete that day).

## 0.8.0

- `include="ebay"` on `bulk.prices()` (sync and async), Pro and up: adds `ebay`
  (`EbaySummary` without `sales`, or `None`) to each `BulkPriceRow`. Costs 1 credit plus
  1 per card with eBay data (`meta.credits_consumed`, summed across auto-chunked calls).
  Below Pro the API answers 403 `TIER_REQUIRED` (`TierError`).
- `include_ebay=True` on `identify.photo()` (implies `include_prices`; every plan, no
  extra charge): adds `ebay` to each of the top candidate's `prices`, and on a graded slab
  `ebay.slab_grade` (`EbaySlabGrade`: `EbayStats` plus the grade `label`) for the grade on
  the label. New model `EbaySlabGrade`.

## 0.7.0

- `include` keyword on `cards.prices()` (`"ebay"` | `"ebay_sales"`) and `cards.history()`
  (`"ebay"`), sync and async, Pro and up, 2 credits (`meta.credits_consumed`): adds `ebay`
  to each row, `None` when there is no eBay data for the printing. Price rows get an
  `EbaySummary` (30-day median sold price for ungraded copies, sales count, last sale,
  `graded` per grade label, `as_of`; `sales: list[EbaySale]` only with `"ebay_sales"`);
  history rows get an `EbayHistoryPoint` (30-day median and sales count, ungraded and per
  grade via `EbayHistoryGrade`). Below Pro the API answers 403 `TIER_REQUIRED`
  (`TierError`). New models `EbayStats`, `EbaySummary`, `EbaySale`, `EbayHistoryPoint`,
  `EbayHistoryGrade`.

## 0.6.0

- `no_market_price_since` on price rows (`Price`, `CardWithPrice`, `PriceMover`,
  `BulkPriceRow`, `IdentifyPrice`): ISO timestamp since which TCGPlayer has priced
  nothing for the product, `None` while it is priced. Optional: `None` until the API
  serves it.
- `identify.usage()`: scan balance, 30 days of scans by outcome, and the trial/purchase
  ledger (`GET /v1/identify/usage`).

Earlier releases are described in their tagged commits.
