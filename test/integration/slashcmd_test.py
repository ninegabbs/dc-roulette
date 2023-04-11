import pytest

import sqlite3
from unittest.mock import AsyncMock

# from app.bot import controller
import app.bot.constants.strings as strings
from app.bot.service import db
from app.data import db as db_module
from app.data.queries import WIPE_USERS, WIPE_BETS
from test.integration.conftest import get_controller
# from test.helpers.test_db import custom_query
from test.mocks.mock_data import (ApplicationContextMock, UserMock, mock_decorator)

user_id = "12345"

@pytest.fixture
def ctx_mock():
    ctx = ApplicationContextMock()
    ctx.respond = AsyncMock()
    ctx.send = AsyncMock()
    return ctx

@pytest.fixture
def mock_timer():
    pass

@pytest.fixture
def prep_user():
    db.add_user(user_id)

@pytest.fixture
def prep_coins(request):
    balance = request.param if hasattr(request, "param") else 0
    db.update_user_coins(user_id, balance)

@pytest.fixture
def wipe_tables():
    db.custom_query(WIPE_USERS, {})
    db.custom_query(WIPE_BETS, {})

@pytest.mark.asyncio
async def test_roulette(get_controller, ctx_mock, wipe_tables):
    await get_controller.roulette(ctx_mock)
    ctx_mock.respond.assert_called_once_with(strings.INTRO_MSG)
    ctx_mock.send.assert_called_once()

@pytest.mark.asyncio
async def test_bet_color_no_user(get_controller, ctx_mock):
    await get_controller.color(ctx_mock, "red", 10)
    ctx_mock.respond.assert_called_once_with(strings.USER_NOT_REGISTERED_MSG.format(user_id=user_id))

@pytest.mark.asyncio
async def test_bet_color_0_balance(get_controller, ctx_mock, prep_user, prep_coins):
    await get_controller.color(ctx_mock, "red", 10)
    ctx_mock.respond.assert_called_once_with(strings.BET_FAIL_0_BALANCE_MSG.format(user_id=user_id))

@pytest.mark.asyncio
@pytest.mark.parametrize('prep_coins', [7], indirect=True)
async def test_bet_color_insufficient_balance(get_controller, ctx_mock, prep_coins):
    await get_controller.color(ctx_mock, "red", 10)
    ctx_mock.respond.assert_called_once_with(strings.BET_FAIL_INSUFFICIENT_BALANCE_MSG.format(
        user_id=user_id,
        user_coins=7,
        bet_amount=10
    ))

@pytest.mark.asyncio
async def test_bet_color_invalid_color(get_controller, ctx_mock):
    await get_controller.color(ctx_mock, "magenta", 5)
    ctx_mock.respond.assert_called_once_with(
        strings.BET_FAIL_INVALID_COLOR_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_bet_color_invalid_amount(get_controller, ctx_mock):
    await get_controller.color(ctx_mock, "red", 0)
    ctx_mock.respond.assert_called_once_with(
        strings.BET_FAIL_INVALID_AMOUNT_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_bet_color_success(get_controller, ctx_mock):
    await get_controller.color(ctx_mock, "red", 5)
    ctx_mock.respond.assert_called_once_with(
        strings.BET_SUCCESS_COLOR_MSG.format(value="red", bet_amount=5)
    )
    assert db.fetch_active_bets_by_user(user_id)[0][3] == "red"
    from app.bot.cogs.round_timer import RoundTimer

@pytest.mark.asyncio
async def test_bet_number_invalid_value(get_controller, ctx_mock):
    await get_controller.number(ctx_mock, "55", 2)
    ctx_mock.respond.assert_called_once_with(
        strings.BET_FAIL_INVALID_NUMBER_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_bet_number_success(get_controller, ctx_mock):
    await get_controller.number(ctx_mock, "24", 2)
    ctx_mock.respond.assert_called_once_with(
        strings.BET_SUCCESS_NUMBER_MSG.format(value="24", bet_amount=2)
    )
    assert db.fetch_active_bets_by_user(user_id)[1][2] == 24

@pytest.mark.asyncio
async def test_my_bets_success(get_controller, ctx_mock):
    await get_controller.my_bets(ctx_mock)
    expected_bets = "5 coins on red\n2 coins on 24"
    ctx_mock.respond.assert_called_once_with(
        strings.MY_BETS_SUCCESS_MSG.format(user_id=user_id, bets=expected_bets)
    )

# TODO: check timer??

@pytest.mark.asyncio
async def test_my_bets_no_user(get_controller, ctx_mock, wipe_tables, prep_user):
    await get_controller.my_bets(ctx_mock)
    ctx_mock.respond.assert_called_once_with(
        strings.MY_BETS_FAIL_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_my_coins_no_user(get_controller, ctx_mock, wipe_tables):
    await get_controller.my_coins(ctx_mock)
    ctx_mock.respond.assert_called_once_with(
        strings.USER_NOT_REGISTERED_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_my_coins_success(get_controller, ctx_mock, prep_user):
    await get_controller.my_coins(ctx_mock)
    ctx_mock.respond.assert_called_once_with(
        strings.MY_COINS_SUCCESS_MSG.format(user_id=user_id, coins=100)
    )
