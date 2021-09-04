from services import auth as auth_service
from utils.constants import AUTH_RESULT
from services import piles as piles_service

username = 'test_username'
password = 'test_password'
pile_name = 'test_pile'


class TestAuth:
    def test_register_service(self):
        register_result = auth_service.register(username, password)
        assert register_result in (AUTH_RESULT['ok'], AUTH_RESULT['username_exists'])

    def test_login_service(self):
        login_result = auth_service.login(username, password)
        assert login_result == AUTH_RESULT['ok']


class TestPiles:
    pile_name_for_second_insert = 'test_pile_insert'
    pile_name_for_update = 'test_pile_update'

    def test_insert_pile(self):
        pile_insert_result = piles_service.insert_pile(pile_name, username)
        assert pile_insert_result['result'] == 'ok'

    def test_pile_update(self):
        piles_service.insert_pile(self.pile_name_for_second_insert, username)
        pile_update_result = piles_service.update_pile(
            self.pile_name_for_second_insert,
            self.pile_name_for_update,
            username,
        )
        assert pile_update_result['result'] == 'ok'

    def test_delete_pile(self):
        pile_delete_result = piles_service.delete_pile(self.pile_name_for_update, username)
        assert pile_delete_result['result'] == 'ok'

    def test_get_all_piles(self):
        piles = piles_service.get_all_piles(username)
        assert piles[0] in(pile_name, 'default')
