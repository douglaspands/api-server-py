import ormar as orm

from apiserver.core.models import ormar as model


class User(model.BaseModel):
    class Meta(model.BaseModelMeta):
        tablename: str = 'users'

    email: str = orm.String(max_length=255, unique=True)
    password: str = orm.String(max_length=255)
    username: str = orm.String(max_length=255, unique=True)
    is_active: bool = orm.Boolean()


__all__ = ('User',)
