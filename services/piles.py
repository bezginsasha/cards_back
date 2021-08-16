from db import db

cards_collection = db.cards


def get_all_piles_service(username):
	return cards_collection.distinct(
		'pile_name',
		{'username': username}
	)


def insert_pile_service(pile_name, username):
	cards_collection.insert_one({
		'pile_name': pile_name,
		'username': username
	})
	return {'result': 'ok'}


def delete_pile_service(pile_name, username):
	cards_collection.delete_one({
		'pile_name': pile_name,
		'original_word': {'$exists': False},
		'username': username
	})
	return {'result': 'ok'}
