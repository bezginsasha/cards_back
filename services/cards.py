from db import db
from bson import json_util

cards_collection = db.cards

def get_clear_card_item(card):
	"""
	mongo has inconvenient format of id:
	'_id': ObjectId("60fbd0c0588d65e6872dc118")
	function get card object taken from mongo
	and returns card object with pretty id:
	'id': '60fbd0c0588d65e6872dc118'
	"""
	card['id'] = str(card['_id'])
	card.pop('_id')
	return card


def get_all_cards():
	cards_cursor = cards_collection.find({})
	all_cards = list(cards_cursor)
	all_cards = [get_clear_card_item(card) for card in all_cards]
	return json_util.dumps(all_cards)
