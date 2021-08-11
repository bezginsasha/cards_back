from db import db
from bson import json_util
from bson.objectid import ObjectId

cards_collection = db.cards


class PilesService:
	def get_all_piles(self):
		piles = cards_collection.distinct('pile_name')
		return json_util.dumps(piles)

	def insert_pile(self, pile_name):
		cards_collection.insert_one({'pile_name': pile_name})

	def delete_pile(self, pile_name):
		cards_collection.delete_one({
			'pile_name': pile_name,
			'original_word': {'$exists': False}
		})
