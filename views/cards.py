from flask import Blueprint, request
from bson import json_util
from humps import camelize

from services.cards import CardsService
from utils.decorators import standard_headers_with_str_response, require_auth, logger
from utils.exceptions import AlreadyExistsError
from utils import responses
from db import real_db

cards_bp = Blueprint('cards', __name__, url_prefix='/api/cards')
cards_service = CardsService(real_db)


@cards_bp.route('/get_all', methods=['GET', 'POST'])
@logger
@require_auth
@standard_headers_with_str_response
def get_all_cards():
    username = request.cookies['username']
    cards = cards_service.get_all_cards(username)
    return json_util.dumps(camelize(cards))


@cards_bp.route('/add', methods=['GET', 'POST'])
@logger
@require_auth
@standard_headers_with_str_response
def add_card():
    original_word = request.form[camelize('original_word')]
    translated_word = request.form[camelize('translated_word')]
    username = request.cookies['username']
    try:
        inserted_id = cards_service.insert_card(original_word, translated_word, username)
    except AlreadyExistsError:
        return json_util.dumps(responses.already_exists)
    return json_util.dumps(responses.ok_with_inserted_id(inserted_id))


@cards_bp.route('/delete', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def delete_card():
    card_id = request.form['id']
    cards_service.delete_card(card_id)
    return json_util.dumps(responses.ok)


@cards_bp.route('/update', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def update_card():
    try:
        cards_service.update_card(
            request.form['id'],
            request.form[camelize('original_word')],
            request.form[camelize('translated_word')],
            request.cookies['username'],
        )
    except AlreadyExistsError:
        return json_util.dumps(responses.already_exists)
    return json_util.dumps(responses.ok)


@cards_bp.route('/move', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def move_card_to_pile():
    card_id = request.form[camelize('card_id')]
    pile_name = request.form[camelize('pile_name')]
    cards_service.move_card_to_pile(card_id, pile_name)
    return json_util.dumps(responses.ok)


@cards_bp.route('/import', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def import_cards():
    file = request.files['file']
    username = request.cookies['username']
    cards_service.import_card(file, username)
    return json_util.dumps(responses.ok)
