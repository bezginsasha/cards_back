from flask import Flask, Response, request
import json
from services.cards import CardsService
from services.piles import PilesService

app = Flask(__name__)

cardsService = CardsService()
pilesService = PilesService()

@app.route('/api/cards/get_all', methods=['GET', 'POST'])
def get_all_cards():
	cards = cardsService.get_all_cards()
	resp = Response(cards)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/api/cards/add', methods=['GET', 'POST'])
def add_card():
	original_word = request.form['original_word']
	translated_word = request.form['translated_word']
	inserted_id = cardsService.insert_card(original_word, translated_word)

	resp = Response(json.dumps({'id': inserted_id}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/api/cards/delete', methods=['POST'])
def delete_card():
	card_id = request.form['id']
	cardsService.delete_card(card_id)

	resp = Response(json.dumps({'result': 'ok'}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/api/cards/update', methods=['POST'])
def update_card():
	cardsService.update_card(
		request.form['id'],
		request.form['original_word'],
		request.form['translated_word']
	)

	resp = Response(json.dumps({'result': 'ok'}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


	resp = Response(json.dumps({'result': 'ok'}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
