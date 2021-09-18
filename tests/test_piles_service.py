from services.piles import PilesService
from db import test_db
from tests import pile_name, username

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
