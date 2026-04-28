"""Smoke tests — hit the live api.tcgapi.dev. Public endpoints only by default.

Set TCGAPI_KEY in the environment to also exercise key-gated endpoints.
"""

from __future__ import annotations

import os

import pytest

from tcgapi import AsyncTCGApi, NotFoundError, TCGApi, TcgApiError

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


async def test_async_games_list() -> None:
    async with AsyncTCGApi() as tcg:
        resp = await tcg.games.list(per_page=3)
        assert len(resp.data) > 0
