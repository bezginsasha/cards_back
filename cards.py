from flask import Flask, Response, request
import json
from services.cards import get_all_cards, insert_card, delete_card

app = Flask(__name__)

@app.route('/api/get_all', methods=['GET', 'POST'])
def index():
	cards = get_all_cards()
	resp = Response(cards)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/api/add', methods=['GET', 'POST'])
def add():
	original_word = request.form['original_word']
	translated_word = request.form['translated_word']
	inserted_id = insert_card(original_word, translated_word)

	resp = Response(json.dumps({'id': inserted_id}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/api/delete', methods=['POST'])
def delete():
	card_id = request.form['id']
	delete_card(card_id)

	resp = Response(json.dumps({'result': 'ok'}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
