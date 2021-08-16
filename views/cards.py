from flask import Blueprint, request
from bson import json_util
from services.cards import get_all_cards_service, insert_card_service, update_card_service, delete_card_service
from utils.decorators import standard_headers_with_str_response
from humps import camelize

cards_bp = Blueprint('cards', __name__, url_prefix='/api/cards')


@cards_bp.route('/get_all', methods=['GET', 'POST'])
@standard_headers_with_str_response
def get_all_cards():
	cards = get_all_cards_service()
	return json_util.dumps(camelize(cards))


@cards_bp.route('/add', methods=['GET', 'POST'])
@standard_headers_with_str_response
def add_card():
	original_word = request.form[camelize('original_word')]
	translated_word = request.form[camelize('translated_word')]
	username = request.cookies['username']
	inserted_id = insert_card_service(original_word, translated_word, username)
	return json_util.dumps({'id': inserted_id})


@cards_bp.route('/delete', methods=['POST'])
@standard_headers_with_str_response
def delete_card():
	card_id = request.form['id']
	delete_card_service(card_id)
	return json_util.dumps({'result': 'ok'})


@cards_bp.route('/update', methods=['POST'])
@standard_headers_with_str_response
def update_card():
	update_card_service(
		request.form['id'],
		request.form[camelize('original_word')],
		request.form[camelize('translated_word')]
	)
	return json_util.dumps({'result': 'ok'})
