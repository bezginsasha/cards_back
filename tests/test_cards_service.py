from services.cards import CardsService
from db import test_db
from tests import username, original_word, translated_word, pile_name
from utils.constants import DB_OPERATION_RESULT

cards_service = CardsService(test_db)

second_original_word = 'original_word_2'
second_translated_word = 'translated_word_2'


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


def test_find_card_by_id():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    assert insert_card_result['result'] == 'ok'

    card_id = insert_card_result['id']
    found_card = cards_service.find_card_by_id(card_id)
    assert found_card['id'] == card_id
    assert found_card['username'] == username
    assert found_card['original_word'] == original_word
    assert found_card['translated_word'] == translated_word

    cards_service.delete_card(card_id)


def test_update_card():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    assert insert_card_result['result'] == 'ok'

    card_id = insert_card_result['id']
    update_card_result = cards_service.update_card(
        card_id,
        second_original_word,
        second_translated_word,
        username
    )
    assert update_card_result['result'] == 'ok'

    found_card = cards_service.find_card_by_id(card_id)
    assert found_card['original_word'] == second_original_word
    assert found_card['translated_word'] == second_translated_word

    cards_service.delete_card(card_id)


def test_update_card_with_existing_original_word():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    first_card_id = insert_card_result['id']

    insert_card_result = cards_service.insert_card(
        second_original_word,
        second_translated_word,
        username
    )
    second_card_id = insert_card_result['id']

    update_card_result = cards_service.update_card(
        second_card_id,
        original_word,
        translated_word,
        username
    )
    assert update_card_result['result'] == DB_OPERATION_RESULT['already_exists']

    cards_service.delete_card(first_card_id)
    cards_service.delete_card(second_card_id)


def test_move_card_to_pile():
    insert_card_result = cards_service.insert_card(
        original_word,
        translated_word,
        username
    )
    card_id = insert_card_result['id']

    move_card_to_pile_result = cards_service.move_card_to_pile(card_id, pile_name)
    assert move_card_to_pile_result['result'] == 'ok'

    found_card = cards_service.find_card_by_id(card_id)
    assert found_card['pile_name'] == pile_name

    cards_service.delete_card(card_id)
