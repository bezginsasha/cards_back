from flask import Blueprint, request
from bson import json_util
from humps import camelize

from services import cards as cards_service
from utils.decorators import standard_headers_with_str_response, require_auth

cards_bp = Blueprint('cards', __name__, url_prefix='/api/cards')


@cards_bp.route('/get_all', methods=['GET', 'POST'])
@require_auth
@standard_headers_with_str_response
def get_all_cards():
    username = request.cookies['username']
    cards = cards_service.get_all_cards(username)
    return json_util.dumps(camelize(cards))


@cards_bp.route('/add', methods=['GET', 'POST'])
@require_auth
@standard_headers_with_str_response
def add_card():
    original_word = request.form[camelize('original_word')]
    translated_word = request.form[camelize('translated_word')]
    username = request.cookies['username']
    inserted_id = cards_service.insert_card(original_word, translated_word, username)
    return json_util.dumps({'id': inserted_id})


@cards_bp.route('/delete', methods=['POST'])
@require_auth
@standard_headers_with_str_response
def delete_card():
    card_id = request.form['id']
    cards_service.delete_card(card_id)
    return json_util.dumps({'result': 'ok'})


@cards_bp.route('/update', methods=['POST'])
@require_auth
@standard_headers_with_str_response
def update_card():
    cards_service.update_card(
        request.form['id'],
        request.form[camelize('original_word')],
        request.form[camelize('translated_word')],
    )
    return json_util.dumps({'result': 'ok'})


@cards_bp.route('/move', methods=['POST'])
@require_auth
@standard_headers_with_str_response
def move_card_to_pile():
    card_id = request.form[camelize('card_id')]
    pile_name = request.form[camelize('pile_name')]
    cards_service.move_card_to_pile(card_id, pile_name)
    return json_util.dumps({'result': 'ok'})
