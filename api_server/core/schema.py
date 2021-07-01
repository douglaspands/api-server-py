from typing import Generic, TypeVar

from pydantic import Field, BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() if n > 0 else word for n, word in enumerate(string.split('_')))


class BaseSchema(BaseModel):

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ResponseOK(GenericModel, Generic[T]):
    data: T = Field(..., title='Envelope', description='Data envelope.')


class ResponseError(BaseSchema):
    error: str = Field(..., title='Error Message', description='Error message.')


__all__ = ('BaseSchema', 'ResponseOK',)
