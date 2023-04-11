import pytest

import sqlite3
from unittest.mock import patch, AsyncMock, MagicMock

import app.data.db as db_module

from test.mocks.mock_data import mock_tasks_loop_decorator, TimerMock

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    db_temp = sqlite3.connect(":memory:")
    monkeypatch.setattr(db_module, "CONN", db_temp)

@pytest.fixture(autouse=True)
def patch_timer():
    patch('discord.ext.tasks', mock_tasks_loop_decorator)

@pytest.fixture
def get_round_timer():
    from app.bot.cogs.round_timer import RoundTimer
    return RoundTimer
