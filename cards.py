from flask import Flask, Response, request
import json
from services.cards import CardsService
from services.piles import PilesService
from utils.decorators import standard_headers_with_str_response
from auth import bp

app = Flask(__name__)
app.register_blueprint(bp)

cardsService = CardsService()
pilesService = PilesService()


@app.route('/api/cards/get_all', methods=['GET', 'POST'])
@standard_headers_with_str_response
def get_all_cards():
	cards = cardsService.get_all_cards()
	return cards


@app.route('/api/cards/add', methods=['GET', 'POST'])
@standard_headers_with_str_response
def add_card():
	original_word = request.form['original_word']
	translated_word = request.form['translated_word']
	inserted_id = cardsService.insert_card(original_word, translated_word)

	resp = json.dumps({'id': inserted_id})
	return resp


@app.route('/api/cards/delete', methods=['POST'])
@standard_headers_with_str_response
def delete_card():
	card_id = request.form['id']
	cardsService.delete_card(card_id)

	resp = json.dumps({'result': 'ok'})
	return resp


@app.route('/api/cards/update', methods=['POST'])
@standard_headers_with_str_response
def update_card():
	cardsService.update_card(
		request.form['id'],
		request.form['original_word'],
		request.form['translated_word']
	)

	resp = json.dumps({'result': 'ok'})
	return resp


@app.route('/api/piles/get_all', methods=['GET'])
@standard_headers_with_str_response
def get_all():
	piles = pilesService.get_all_piles()
	return piles


@app.route('/api/piles/add', methods=['POST'])
@standard_headers_with_str_response
def insert_pile():
	pilesService.insert_pile(request.form['pile_name'])

	resp = json.dumps({'result': 'ok'})
	return resp


@app.route('/api/piles/delete', methods=['POST'])
@standard_headers_with_str_response
def delete_pile():
	pilesService.delete_pile(request.form['pile_name'])

	resp = json.dumps({'result': 'ok'})
	return resp
