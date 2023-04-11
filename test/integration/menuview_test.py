import pytest

from unittest.mock import AsyncMock

from app.bot.constants import choices
import app.bot.constants.strings as strings
from app.bot.service import db

from test.mocks.mock_data import SelectMock, UserMock
from test.integration.conftest import get_controller


@pytest.fixture
def prep_args():
    select = SelectMock(choices.REGISTER)
    interaction = AsyncMock()
    interaction.user = UserMock()
    interaction.response.send_message = AsyncMock()
    return select, interaction

@pytest.fixture
def prep_coins(user_id="12345", balance=0):
    db.update_user_coins(user_id, balance)

@pytest.mark.asyncio
async def test_select_callback_register_success(prep_args, get_controller):
    menu_view = get_controller.MenuView()
    user_id = "12345"
    select, interaction = prep_args
    await menu_view.select_callback(select, interaction)
    interaction.response.send_message.assert_called_once_with(
        strings.REGISTER_SUCCESS_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_select_callback_register_already_registered(prep_args, get_controller):
    select, interaction = prep_args
    menu_view = get_controller.MenuView()
    user_id = "12345"
    await menu_view.select_callback(select, interaction)
    interaction.response.send_message.assert_called_once_with(
        strings.REGISTER_FAIL_MSG.format(user_id=user_id)
    )

@pytest.mark.asyncio
async def test_select_callback_register_refill_coins(prep_args, prep_coins, get_controller):
    select, interaction = prep_args
    menu_view = get_controller.MenuView()
    user_id = "12345"
    await menu_view.select_callback(select, interaction)
    interaction.response.send_message.assert_called_once_with(
        strings.REGISTER_SUCCESS_MSG.format(user_id=user_id)
    )
    current_coins = db.fetch_user_by_id(user_id)[1]
    assert current_coins == 100

@pytest.mark.asyncio
async def test_select_callback_rules(prep_args, get_controller):
    select, interaction = prep_args
    select.values[0] = choices.RULES
    menu_view = get_controller.MenuView()
    await menu_view.select_callback(select, interaction)
    interaction.response.send_message.assert_called_once_with(strings.RESP_RULES)

@pytest.mark.asyncio
async def test_select_callback_commands(prep_args, get_controller):
    select, interaction = prep_args
    select.values[0] = choices.COMMANDS
    menu_view = get_controller.MenuView()
    await menu_view.select_callback(select, interaction)
    interaction.response.send_message.assert_called_once_with(strings.LIST_COMMANDS)

