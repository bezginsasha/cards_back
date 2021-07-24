from flask import Flask, Response, request
from db import db
import json
from bson import json_util

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    cards_collection = db.cards

    words_cursor = cards_collection.find({})

    words_list = list(words_cursor)

    words_json = json_util.dumps(words_list)


    resp = Response(words_json)
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