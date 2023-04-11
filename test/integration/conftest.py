import pytest

import sqlite3

from unittest.mock import patch, MagicMock, AsyncMock

import app.data.db as db_module

from test.mocks.mock_data import mock_decorator, mock_tasks_loop_decorator

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    db_temp = sqlite3.connect(":memory:")
    monkeypatch.setattr(db_module, "CONN", db_temp)

@pytest.fixture(autouse=True)
def patch_discord():
    patch('discord.ui.select', mock_decorator).start()
    patch('discord.Bot', MagicMock())
    patch('app.bot.cogs.round_timer.RoundTimer', AsyncMock())
    patch('discord.ext.tasks.loop', mock_tasks_loop_decorator).start()

@pytest.fixture
def get_controller():
    #'controller' module has to be imported after 'discord.ui.select' is mocked
    from app.bot import controller
    return controller
