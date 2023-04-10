import pytest

from unittest.mock import AsyncMock

from app.config import ROUND_DURATION_S

from test.mocks.mock_data import ApplicationContextMock

round_duration = ROUND_DURATION_S

@pytest.fixture
def ctx_mock():
    ctx = ApplicationContextMock()
    ctx.respond = AsyncMock()
    ctx.send = AsyncMock()
    return ctx

def test_round_timer_instances(ctx_mock, get_round_timer):
    ctx = ApplicationContextMock()
    rt1 = get_round_timer(ctx_mock)
    rt2 = get_round_timer(ctx_mock)
    assert rt1 is rt2
    assert rt1.index > 0
    get_round_timer.delete_instance()
    rt1 = get_round_timer(ctx_mock)
    assert rt1 is not rt2
