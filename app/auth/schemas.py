from pydantic import BaseModel


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        fields = {
            'access_token': {
                'title': 'Access token',
                'description': 'Access token.',
                'example': 'sahdlkhahsldjhajshldhakhsdhkahsjdhahshdljashdashdjhajlhsdjahkhsdkhalkdhskshdajhjshdk4'
            },
            'token_type': {
                'title': 'Token type',
                'description': 'Token type.',
                'example': 'bearer'
            },
        }


__all__ = ('TokenOut',)
