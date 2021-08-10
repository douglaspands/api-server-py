"""Core Base Model For ORMAR."""
from __future__ import annotations

from typing import Any, TypeVar
from datetime import datetime

import ormar

from app.core.databases.sqlalchemy import database, metadata


class BaseModelMeta(ormar.ModelMeta):
    """Base ModelMeta for ORMAR Model."""

    metadata = metadata
    database = database


T = TypeVar("T", bound="BaseModel")


class BaseModel(ormar.Model):
    """Base Model for ORMAR Model."""

    class Meta(BaseModelMeta):
        """Metadata from BaseModel."""

        abstract = True

    id: int = ormar.Integer(primary_key=True)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow)

    async def update(self: T, *args: Any, **kwargs: Any) -> T:
        """Set updated_at fields before update run.

        Returns:
            T: Domain Model.
        """
        self.updated_at = datetime.utcnow()
        return await super().update(*args, **kwargs)


__all__ = (
    "BaseModelMeta",
    "BaseModel",
)
