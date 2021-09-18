from services.piles import PilesService
from db import test_db
from tests import pile_name, username
from utils.constants import DB_OPERATION_RESULT

piles_service = PilesService(test_db)


def test_insert_and_delete_pile():
    pile_insert_result = piles_service.insert_pile(
        pile_name,
        username,
    )
    assert pile_insert_result['result'] == 'ok'

    delete_pile_result = piles_service.delete_pile(
        pile_name,
        username,
    )
    assert delete_pile_result['result'] == 'ok'


def test_double_insert_pile():
    pile_insert_result = piles_service.insert_pile(
        pile_name,
        username,
    )
    assert pile_insert_result['result'] == 'ok'

    pile_insert_result = piles_service.insert_pile(
        pile_name,
        username,
    )
    assert pile_insert_result['result'] == DB_OPERATION_RESULT['already_exists']

    piles_service.delete_pile(
        pile_name,
        username,
    )


def test_update_pile():
    pile_insert_result = piles_service.insert_pile(
        pile_name,
        username,
    )
    assert pile_insert_result['result'] == 'ok'

    pile_name_for_update = 'second_pile_name'
    pile_update_result = piles_service.update_pile(
        pile_name,
        pile_name_for_update,
        username,
    )
    assert pile_update_result['result'] == 'ok'

    updated_pile = piles_service.find_pile_by_name(pile_name_for_update, username)
    assert updated_pile is not None

    old_pile = piles_service.find_pile_by_name(pile_name, username)
    assert old_pile is None

    piles_service.delete_pile(
        pile_name_for_update,
        username,
    )


def test_update_pile_with_existing_pile_name():
    piles_service.insert_pile(
        pile_name,
        username,
    )

    second_pile_name = 'second_pile_name'
    piles_service.insert_pile(
        second_pile_name,
        username,
    )

    pile_name_for_update = 'pile_name_for_update'
    pile_update_result = piles_service.update_pile(
        pile_name,
        pile_name_for_update,
        username,
    )
    assert pile_update_result['result'] == 'ok'

    pile_update_result = piles_service.update_pile(
        pile_name_for_update,
        second_pile_name,
        username,
    )
    assert pile_update_result['result'] == DB_OPERATION_RESULT['already_exists']

    piles_service.delete_pile(
        second_pile_name,
        username,
    )
    piles_service.delete_pile(
        pile_name_for_update,
        username,
    )
