"""Core Schemas."""
from typing import Generic, TypeVar

from pydantic import Field, BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


def to_camel(string: str) -> str:
    """Convert text to camel case.

    Args:
        string (str): text.

    Returns:
        str: Text camel case.
    """
    return ''.join(word.capitalize() if n > 0 else word for n, word in enumerate(string.split('_')))


class BaseConfig:
    """Base metadata for schema."""

    alias_generator = to_camel
    allow_population_by_field_name = True


class BaseSchema(BaseModel):
    """Base schema for domains schemas."""

    class Config(BaseConfig):
        """Base metadata."""

        pass


class ResponseOK(GenericModel, Generic[T]):
    """Response schema for result ok."""

    data: T = Field(..., title='Envelope', description='Data envelope.')


__all__ = ('ResponseOK', 'BaseSchema', 'BaseConfig', 'to_camel')
