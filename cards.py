from flask import Flask, Response, request
from db import db
import json
from bson import json_util
from services.cards import get_all_cards

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	cards = get_all_cards()
	resp = Response(cards)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/add', methods=['GET', 'POST'])
def add():

	cards_collection = db.cards

	word = {
		"original_word": request.form['original_word'],
		"translated_word": request.form['translated_word']
	}

	inserted_word = cards_collection.insert_one(word)

	resp = Response(json.dumps({'id': str(inserted_word.inserted_id)}))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
