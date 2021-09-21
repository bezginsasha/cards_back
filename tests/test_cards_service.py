from pathlib import Path

from werkzeug.datastructures import FileStorage

from services.cards import CardsService
from db import test_db
from tests import username, original_word, translated_word, pile_name
from utils.importing import iter_excel
from utils.exceptions import AlreadyExistsError

cards_service = CardsService(test_db)

second_original_word = 'original_word_2'
second_translated_word = 'translated_word_2'


def test_insert_and_delete_card():
    card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    cards_service.delete_card(card_id)


def test_insert_double_card():
    card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    try:
        cards_service.insert_card(
            original_word,
            translated_word,
            username,
        )
    except AlreadyExistsError:
        pass
    cards_service.delete_card(card_id)


def test_find_card_by_original_word_and_test_clear_card_item():
    card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    found_card = cards_service.find_card_by_original_word(original_word, username)
    assert found_card['username'] == username
    assert found_card['original_word'] == original_word
    assert found_card['translated_word'] == translated_word

    assert 'id' in found_card
    assert '_id' not in found_card

    cards_service.delete_card(card_id)


def test_find_card_by_id():
    card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    found_card = cards_service.find_card_by_id(card_id)
    assert found_card['id'] == card_id
    assert found_card['username'] == username
    assert found_card['original_word'] == original_word
    assert found_card['translated_word'] == translated_word

    cards_service.delete_card(card_id)


def test_update_card():
    card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    cards_service.update_card(
        card_id,
        second_original_word,
        second_translated_word,
        username,
    )

    found_card = cards_service.find_card_by_id(card_id)
    assert found_card['original_word'] == second_original_word
    assert found_card['translated_word'] == second_translated_word

    cards_service.delete_card(card_id)


def test_update_card_with_existing_original_word():
    first_card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    second_card_id = cards_service.insert_card(
        second_original_word,
        second_translated_word,
        username,
    )

    try:
        cards_service.update_card(
            second_card_id,
            original_word,
            translated_word,
            username,
        )
    except AlreadyExistsError:
        pass

    cards_service.delete_card(first_card_id)
    cards_service.delete_card(second_card_id)


def test_move_card_to_pile():
    card_id = cards_service.insert_card(
        original_word,
        translated_word,
        username,
    )

    cards_service.move_card_to_pile(card_id, pile_name)

    found_card = cards_service.find_card_by_id(card_id)
    assert found_card['pile_name'] == pile_name

    cards_service.delete_card(card_id)


def test_import_cards():
    file_name = 'for_test_import.xlsx'
    full_path = Path.cwd() / 'tests'
    with open(full_path / file_name, 'rb') as f:
        file = FileStorage(f)
        cards_service.import_card(
            file,
            username,
        )

    for row in iter_excel(full_path, file_name):
        original_word_row = row[0]
        translated_word_row = row[1]

        found_card = cards_service.find_card_by_original_word(
            original_word_row,
            username,
        )

        assert found_card['original_word'] == original_word_row
        assert found_card['translated_word'] == translated_word_row

        cards_service.delete_card(found_card['id'])
