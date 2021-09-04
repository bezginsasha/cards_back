from services import auth as auth_service
from utils.constants import AUTH_RESULT, DB_OPERATION_RESULT
from services import piles as piles_service
from services import cards as cards_service

username = 'test_username'
password = 'test_password'
pile_name = 'test_pile'
original_word = 'test_original_word'
translated_word = 'test_translated_word'


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
        piles_service.delete_pile(pile_name, username)


class TestCards:
    original_word_for_second_insert = 'test_original_word_insert'
    translated_word_for_second_insert = 'test_translated_word_insert'
    original_word_for_update = 'test_original_word_update'
    id_of_second_inserted_card = None

    def test_insert_card(self):
        """ Now i don't use assert there because
        this method tests only is there exceptions while inserting or no
        """
        cards_service.insert_card(
            original_word,
            translated_word,
            username,
        )

    def test_double_insert_the_same_card(self):
        double_insert_card_result = cards_service.insert_card(
            original_word,
            translated_word,
            username,
        )
        assert double_insert_card_result['result'] == DB_OPERATION_RESULT['already_exists']

    def test_update_card(self):
        self.id_of_second_inserted_card = cards_service.insert_card(
            self.original_word_for_second_insert,
            self.translated_word_for_second_insert,
            username,
        )
        card_update_result = update_card_result = cards_service.update_card(
            self.id_of_second_inserted_card,
            self.original_word_for_update,
            self.translated_word_for_second_insert,
        )
        assert card_update_result['result'] == 'ok'

    def test_delete_card(self):
        card_delete_result = cards_service.delete_card(self.id_of_second_inserted_card)
        assert card_delete_result['result'] == 'ok'

    def test_get_all_cards(self):
        cards = cards_service.get_all_cards(username)
        original_words = [card['original_word'] for card in cards]
        translated_words = [card['translated_word'] for card in cards]

        assert original_word in original_words
        assert translated_word in translated_words

    def test_move_card_to_pile(self):
        card_id = cards_service.insert_card(
            self.original_word_for_second_insert,
            self.translated_word_for_second_insert,
            username,
        )
        move_card_result = cards_service.move_card_to_pile(card_id, pile_name)
        assert move_card_result['result'] == 'ok'
        cards_service.delete_card(card_id)
