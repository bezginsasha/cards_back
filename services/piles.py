from db import db
from bson import json_util

cards_collection = db.cards


def get_all_piles_service():
	return cards_collection.distinct('pile_name')


def insert_pile_service(pile_name):
	cards_collection.insert_one({'pile_name': pile_name})
	return {'result': 'ok'}


def delete_pile_service(pile_name):
	cards_collection.delete_one({
		'pile_name': pile_name,
		'original_word': {'$exists': False}
	})
	return {'result': 'ok'}
