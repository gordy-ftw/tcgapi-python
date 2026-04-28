"""Helpers shared by every resource module."""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from ..models import Meta, RateLimit, Response

T = TypeVar("T")


def parse_response(model: type[T], body: dict[str, Any]) -> Response[T]:
    """Coerce a raw response body into a typed Response[T] wrapper."""
    raw_data = body.get("data")
    if isinstance(model, type) and issubclass(model, BaseModel):
        data = model.model_validate(raw_data)
    else:
        # Generic types (list[X], dict[str, list[X]], etc.) handled with TypeAdapter via the caller.
        from pydantic import TypeAdapter

        data = TypeAdapter(model).validate_python(raw_data)

    meta = Meta.model_validate(body["meta"]) if body.get("meta") else None
    rate_limit = RateLimit.model_validate(body["rate_limit"]) if body.get("rate_limit") else None
    return Response[T](data=data, meta=meta, rate_limit=rate_limit)  # type: ignore[valid-type]
