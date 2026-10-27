"""Smoke tests — hit the live api.tcgapi.dev. Public endpoints only by default.

Set TCGAPI_KEY in the environment to also exercise key-gated endpoints.
"""

from __future__ import annotations

import os

import pytest

from tcgapi import AsyncTCGApi, NotFoundError, TCGApi, TcgApiError, TierError

HAS_KEY = bool(os.environ.get("TCGAPI_KEY"))


def test_games_list() -> None:
    with TCGApi() as tcg:
        resp = tcg.games.list(per_page=5)
        assert len(resp.data) > 0
        assert resp.data[0].slug


def test_games_get_pokemon() -> None:
    with TCGApi() as tcg:
        resp = tcg.games.get("pokemon")
        assert resp.data.slug == "pokemon"
        assert resp.data.name == "Pokemon"


def test_games_get_unknown_raises_not_found() -> None:
    with TCGApi() as tcg:
        with pytest.raises(NotFoundError):
            tcg.games.get("definitely-not-a-real-game-xyz")


def test_ebay_coverage_public() -> None:
    with TCGApi() as tcg:
        resp = tcg.ebay.coverage()
        assert resp.data.totals.cards_with_ebay
        assert len(resp.data.games) > 0
        assert resp.data.games[0].refresh is not None
        assert resp.data.games[0].refresh.three_day is not None


def test_ebay_coverage_pokemon_sets() -> None:
    with TCGApi() as tcg:
        resp = tcg.ebay.coverage("pokemon")
        assert resp.data.slug == "pokemon"
        assert len(resp.data.sets) > 0


def test_ebay_coverage_unknown_game_raises_not_found() -> None:
    with TCGApi() as tcg:
        with pytest.raises(NotFoundError):
            tcg.ebay.coverage("definitely-not-a-real-game-xyz")


def test_games_sets_for_pokemon() -> None:
    with TCGApi() as tcg:
        resp = tcg.games.sets("pokemon", per_page=3)
        assert len(resp.data) > 0
        assert resp.data[0].name


@pytest.mark.skipif(not HAS_KEY, reason="search.cards is x402-priced; needs API key")
def test_search_cards() -> None:
    with TCGApi() as tcg:
        resp = tcg.search.cards("charizard", per_page=5)
        assert len(resp.data) > 0
        assert (resp.meta.total if resp.meta else 0) > 0


@pytest.mark.skipif(HAS_KEY, reason="without a key we expect a 402")
def test_search_cards_without_key_raises_402() -> None:
    with TCGApi() as tcg:
        with pytest.raises(TcgApiError) as exc_info:
            tcg.search.cards("charizard")
        assert exc_info.value.status == 402


@pytest.mark.skipif(HAS_KEY, reason="without a key we expect a 402")
def test_card_conditions_without_key_raises_402() -> None:
    with TCGApi() as tcg:
        with pytest.raises(TcgApiError) as exc_info:
            tcg.cards.conditions(13217)
        assert exc_info.value.status == 402


@pytest.mark.skipif(not HAS_KEY, reason="cards.conditions is Pro-gated; needs API key")
def test_card_conditions() -> None:
    with TCGApi() as tcg:
        try:
            resp = tcg.cards.conditions(13217)
            assert isinstance(resp.data, list)
        except TierError:
            pass  # sub-Pro keys get the tier gate — that shape is also correct


@pytest.mark.skipif(HAS_KEY, reason="without a key we expect a 402")
def test_bulk_conditions_without_key_raises_402() -> None:
    with TCGApi() as tcg:
        with pytest.raises(TcgApiError) as exc_info:
            tcg.bulk.conditions([13217])
        assert exc_info.value.status == 402


@pytest.mark.skipif(not HAS_KEY, reason="bulk.conditions is Pro-gated; needs API key")
def test_bulk_conditions() -> None:
    with TCGApi() as tcg:
        try:
            resp = tcg.bulk.conditions([13217])
            assert isinstance(resp.data, list)
        except TierError:
            pass  # sub-Pro keys get the tier gate — that shape is also correct


@pytest.mark.skipif(HAS_KEY, reason="without a key we expect a 402")
def test_supply_without_key_raises_402() -> None:
    with TCGApi() as tcg:
        for call in (lambda: tcg.cards.supply(13118), lambda: tcg.cards.supply_history(13118), lambda: tcg.bulk.supply([13118])):
            with pytest.raises(TcgApiError) as exc_info:
                call()
            assert exc_info.value.status == 402


@pytest.mark.skipif(not HAS_KEY, reason="cards.supply is Pro-gated; needs API key")
def test_supply() -> None:
    with TCGApi() as tcg:
        try:
            resp = tcg.cards.supply(13118)
            assert resp.data.card_id == 13118
            assert isinstance(resp.data.printings, list)
            history = tcg.cards.supply_history(13118, days=30)
            assert len(history.data) > 0
            bulk = tcg.bulk.supply([13118])
            assert [s.card_id for s in bulk.data] == [13118]
        except TierError:
            pass  # sub-Pro keys get the tier gate — that shape is also correct


@pytest.mark.skipif(not HAS_KEY, reason="cards.supply is Pro-gated; needs API key")
async def test_async_supply() -> None:
    async with AsyncTCGApi() as tcg:
        try:
            resp = await tcg.cards.supply(13118)
            assert resp.data.card_id == 13118
        except TierError:
            pass


async def test_async_games_list() -> None:
    async with AsyncTCGApi() as tcg:
        resp = await tcg.games.list(per_page=3)
        assert len(resp.data) > 0


async def test_async_ebay_coverage() -> None:
    async with AsyncTCGApi() as tcg:
        resp = await tcg.ebay.coverage("pokemon")
        assert resp.data.slug == "pokemon"


def _charizard_photo() -> bytes:
    # Base Set Charizard (TCGPlayer 42382), TCGPlayer's own product photo.
    import httpx

    return httpx.get("https://product-images.tcgplayer.com/fit-in/1000x1000/42382.jpg").content


@pytest.mark.skipif(HAS_KEY, reason="checks the keyless path")
def test_identify_without_key_reaches_x402() -> None:
    # A malformed upload would be a 400 INVALID_IMAGE; reaching the 402 offer proves the multipart body is right.
    with TCGApi() as tcg:
        with pytest.raises(TcgApiError) as exc:
            tcg.identify.photo(_charizard_photo())
        assert exc.value.status == 402


@pytest.mark.skipif(not HAS_KEY, reason="uses one scan; needs TCGAPI_KEY")
def test_identify_reads_a_card() -> None:
    with TCGApi() as tcg:
        resp = tcg.identify.photo(_charizard_photo(), game="pokemon", include_prices=True)
        assert resp.data.candidates[0].tcgplayer_id == 42382
        assert resp.data.candidates[0].prices
        assert resp.meta is not None and resp.meta.charged == "scan"


@pytest.mark.skipif(HAS_KEY, reason="checks the keyless path")
async def test_async_identify_without_key_reaches_x402() -> None:
    async with AsyncTCGApi() as tcg:
        with pytest.raises(TcgApiError) as exc:
            await tcg.identify.photo(_charizard_photo())
        assert exc.value.status == 402


@pytest.mark.skipif(not HAS_KEY, reason="needs TCGAPI_KEY")
def test_identify_usage_is_free() -> None:
    with TCGApi() as tcg:
        a = tcg.identify.usage()
        b = tcg.identify.usage()
        assert len(a.data.days) == 30
        assert b.data.balance == a.data.balance  # reading usage takes no scan


@pytest.mark.skipif(not HAS_KEY, reason="needs TCGAPI_KEY")
async def test_async_identify_usage() -> None:
    async with AsyncTCGApi() as tcg:
        resp = await tcg.identify.usage()
        assert len(resp.data.days) == 30
