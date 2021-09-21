from services.piles import PilesService
from db import test_db
from tests import pile_name, username
from utils.exceptions import AlreadyExistsError

piles_service = PilesService(test_db)


def test_insert_and_delete_pile():
    piles_service.insert_pile(
        pile_name,
        username,
    )

    piles_service.delete_pile(
        pile_name,
        username,
    )


def test_double_insert_pile():
    piles_service.insert_pile(
        pile_name,
        username,
    )

    try:
        piles_service.insert_pile(
            pile_name,
            username,
        )
    except AlreadyExistsError:
        pass

    piles_service.delete_pile(
        pile_name,
        username,
    )


def test_update_pile():
    piles_service.insert_pile(
        pile_name,
        username,
    )

    pile_name_for_update = 'second_pile_name'
    piles_service.update_pile(
        pile_name,
        pile_name_for_update,
        username,
    )

    piles_service.find_pile_by_name(pile_name_for_update, username)

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
    piles_service.update_pile(
        pile_name,
        pile_name_for_update,
        username,
    )

    try:
        piles_service.update_pile(
            pile_name_for_update,
            second_pile_name,
            username,
        )
    except AlreadyExistsError:
        pass

    piles_service.delete_pile(
        second_pile_name,
        username,
    )
    piles_service.delete_pile(
        pile_name_for_update,
        username,
    )
