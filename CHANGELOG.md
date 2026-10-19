# Changelog

## 0.6.0

- `no_market_price_since` on price rows (`Price`, `CardWithPrice`, `PriceMover`,
  `BulkPriceRow`, `IdentifyPrice`): ISO timestamp since which TCGPlayer has priced
  nothing for the product, `None` while it is priced. Optional: `None` until the API
  serves it.
- `identify.usage()`: scan balance, 30 days of scans by outcome, and the trial/purchase
  ledger (`GET /v1/identify/usage`).

Earlier releases are described in their tagged commits.
