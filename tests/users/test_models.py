from datetime import datetime
from app.users import models


def test_user_instance():
    user = models.User(
        email="jonh.roberts@email.com",
        password="123456",
        username="jonh.roberts",
        is_active=True
    )
    assert user.email == "jonh.roberts@email.com"
    assert user.password == "123456"
    assert user.username == "jonh.roberts"
    assert user.is_active
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
