from flask import Flask, Response, request
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    client = MongoClient()
    db = client.test
    cards_collection = db.cards

    words_cursor = cards_collection.find({})

    words_list = list(words_cursor)

    words_json = json_util.dumps(words_list)


    resp = Response(words_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
