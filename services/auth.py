from werkzeug.security import generate_password_hash
from db import db

cards_collection = db.cards


def register_service(username, password):
	"""
	function returns True if register was successful
	and False if username already exists
	"""
	found_users = cards_collection.find({'username': username})
	if found_users.count() == 0:
		cards_collection.insert_one({
			'username': username,
			'password': generate_password_hash(password)
		})
		return True
	return False
