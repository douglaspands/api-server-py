"""Users Models."""
import ormar as orm

from app.core.models import ormar as model


class User(model.BaseModel):
    """User Model."""

    class Meta(model.BaseModelMeta):
        """Metadata."""

        tablename: str = "users"

    email: str = orm.String(max_length=255, unique=True)
    password: str = orm.String(max_length=255)
    username: str = orm.String(max_length=255, unique=True)
    is_active: bool = orm.Boolean()


__all__ = ("User",)
