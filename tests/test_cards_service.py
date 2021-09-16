from services.cards import CardsService
from db import test_db
from tests import username, original_word, translated_word
from utils.constants import DB_OPERATION_RESULT

cards_service = CardsService(test_db)


def test_insert_and_delete_card():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    assert insert_card_result['result'] == 'ok'

    delete_card_result = cards_service.delete_card(insert_card_result['id'])
    assert delete_card_result['result'] == 'ok'


def test_insert_double_card():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    assert insert_card_result['result'] == 'ok'
    card_id = insert_card_result['id']

    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    assert insert_card_result['result'] == DB_OPERATION_RESULT['already_exists']
    cards_service.delete_card(card_id)


def test_find_card_by_original_word_and_test_clear_card_item():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    assert insert_card_result['result'] == 'ok'

    found_card = cards_service.find_card_by_original_word(original_word, username)
    assert found_card['username'] == username
    assert found_card['original_word'] == original_word
    assert found_card['translated_word'] == translated_word

    assert 'id' in found_card
    assert '_id' not in found_card

    cards_service.delete_card(insert_card_result['id'])
