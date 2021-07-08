from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        fields = {
            'access_token': {
                'title': 'Access token',
                'description': 'Access token.',
                'example': ''
            },
            'token_type': {
                'title': 'Token type',
                'description': 'Token type.',
                'example': ''
            },
        }
        schema_extra = {
            'application/json': {
                'examples': {
                    'access_token': '',
                    'token_type': '',
                }
            }
        }


__all__ = ('TokenOut',)
