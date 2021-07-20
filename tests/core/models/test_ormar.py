import asyncio
from datetime import datetime
from importlib import reload
from unittest.mock import patch

import ormar as orm
import pytest


def test_basemodel_ok():

    class MockSetting:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:docker@localhost:5432/apiserver'

    with patch('apiserver.core.config.settings', MockSetting) as mock_settings:

        from apiserver.core.models import ormar as model
        reload(model)

        class Team(model.BaseModel):
            class Meta(model.BaseModelMeta):
                tablename: str = 'teams'

            name: str = orm.String(max_length=50)

        team = Team(name='SuperTeam')

        assert team.id == None
        assert team.name == 'SuperTeam'
        assert isinstance(team.created_at, datetime)
        assert isinstance(team.updated_at, datetime)


@pytest.mark.asyncio
async def test_basemodel_update_ok():

    class MockSetting:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:docker@localhost:5432/apiserver'

    async def mock_update(*args, **kwargs):
        pass

    with patch('apiserver.core.config.settings', MockSetting) as mock_settings:

        import ormar
        reload(ormar)

        with patch('ormar.Model.update', mock_update) as mock_orm:

            from apiserver.core.models import ormar as model
            reload(model)

            class Player(model.BaseModel):
                class Meta(model.BaseModelMeta):
                    tablename: str = 'players'

                name: str = orm.String(max_length=50)

            player = Player(name='Richard')
            assert player.id == None
            assert player.name == 'Richard'
            assert isinstance(player.created_at, datetime)
            assert isinstance(player.updated_at, datetime)

            update_at = player.updated_at
            await asyncio.sleep(1)
            await player.update()
            assert update_at != player.updated_at
