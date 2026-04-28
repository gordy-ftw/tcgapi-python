# tcgapi

[![PyPI](https://img.shields.io/pypi/v/tcgapi.svg)](https://pypi.org/project/tcgapi/)
[![Python](https://img.shields.io/pypi/pyversions/tcgapi.svg)](https://pypi.org/project/tcgapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for [**tcgapi.dev**](https://tcgapi.dev) — a unified pricing API for **89+ trading card games**, including:

- Pokémon TCG (English + Japanese)
- Magic: The Gathering
- Yu-Gi-Oh!
- Lorcana
- One Piece Card Game
- Flesh and Blood
- Star Wars Unlimited
- Digimon, Dragon Ball Super, Riftbound, Union Arena, Final Fantasy TCG, Weiss Schwarz, Cardfight!! Vanguard, and dozens more.

Real-time market prices, full price history, fuzzy search, bulk lookups, and exports — all from one HTTP API. Sync and async clients, fully typed with Pydantic.

## Install

```bash
pip install tcgapi
```

Requires Python 3.9+.

## Quickstart

Get a free API key at [**tcgapi.dev/dashboard**](https://tcgapi.dev/dashboard) (100 requests/day, no credit card).

```python
from tcgapi import TCGApi

tcg = TCGApi(api_key="tcg_live_...")  # or set TCGAPI_KEY env var

# Look up a single card
card = tcg.cards.get(123456)
print(card.data.name)

# Get every printing's current price
prices = tcg.cards.prices(123456)
for p in prices.data:
    print(f"{p.printing}: ${p.market_price}")
```

If `api_key` is omitted, the client reads from `TCGAPI_KEY`.

## Examples

### Search across every game

```python
results = tcg.search.cards(
    "charizard",
    game="pokemon",
    sort="price_desc",
    per_page=20,
)
for card in results.data:
    print(card.name, card.set_name, card.market_price)
```

### Iterate without pagination boilerplate

```python
for card in tcg.search.iter("lightning", game="magic"):
    # walks meta.has_more automatically — caps at the API's 200/page max
    ...
```

### Browse sets

```python
games = tcg.games.list()
pokemon_sets = tcg.games.sets("pokemon")
surging_sparks = next(
    (s for s in pokemon_sets.data if "Surging Sparks" in s.name), None
)

if surging_sparks:
    cards = tcg.sets.cards(surging_sparks.id, sort="price_desc")
    print(f"{surging_sparks.name}: {cards.meta.total} cards")
```

### Bulk price lookup (Pro+)

```python
# Auto-chunks if you pass more than 500 IDs.
bulk = tcg.bulk.prices([1, 2, 3, ...])  # thousands ok
print(f"Got prices for {len(bulk.data)} card-printings")
```

### Top movers

```python
movers = tcg.prices.top_movers(
    game="pokemon",
    direction="up",
    period="7d",
    limit=10,
)
for m in movers.data:
    print(f"{m.name} ({m.set_name}): +{m.price_change}% — ${m.market_price}")
```

### Price history (Hobby+)

```python
# Window scales with your tier: free=7d, hobby=30d, starter=90d, pro/business=full.
history = tcg.cards.history(123456, range="year")
for point in history.data:
    print(point.date, point.market_price)
```

### Async client

The async API mirrors the sync surface verbatim:

```python
import asyncio
from tcgapi import AsyncTCGApi

async def main():
    async with AsyncTCGApi() as tcg:
        resp = await tcg.search.cards("charizard", game="pokemon")
        async for card in tcg.search.iter("dragon", game="magic"):
            print(card.name)

asyncio.run(main())
```

## Rate limits

Every successful response carries the live rate-limit budget:

```python
resp = tcg.games.list()
print(resp.rate_limit)
# RateLimit(daily_limit=10000, daily_remaining=9871, daily_reset='2026-04-29T00:00:00.000Z')
```

When you exceed the daily limit you'll get a typed `RateLimitError`:

```python
from tcgapi import RateLimitError

try:
    tcg.cards.get(123)
except RateLimitError as err:
    print(f"Hit the limit — retry in {err.retry_after}s")
```

Other error classes: `AuthError` (401), `TierError` (403), `NotFoundError` (404), `TcgApiError` (anything else). All extend `Exception`.

## Tiers

| Plan | Daily requests | History | Bulk endpoints |
|------|---------------|---------|----------------|
| Free | 100 | 7 days | — |
| Hobby ($9.99/mo) | 1,000 | 30 days | — |
| Starter ($19.99/mo) | 2,500 | 90 days | Limited |
| Pro ($49.99/mo) | 10,000 | Full | Yes |
| Business ($99.99/mo) | 50,000 | Full | Yes |

Or pay per request via [x402](https://tcgapi.dev/api/x402) — no signup, USDC on Base or Solana.

## API reference

Full endpoint reference: [**tcgapi.dev/api**](https://tcgapi.dev/api/)
OpenAPI spec: [**tcgapi.dev/openapi.yaml**](https://tcgapi.dev/openapi.yaml)
Quickstart guide: [**tcgapi.dev/quickstart**](https://tcgapi.dev/quickstart/)

## License

MIT
