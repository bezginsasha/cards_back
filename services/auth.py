from werkzeug.security import generate_password_hash, check_password_hash

from utils.constants import AUTH_RESULT
from db import db

cards_collection = db.cards


def register(username, password):
    found_users = cards_collection.find({'username': username})
    if not found_users.count():
        cards_collection.insert_one({
            'username': username,
            'password': generate_password_hash(password),
        })
        return AUTH_RESULT['ok']
    return AUTH_RESULT['username_exists']


def login(username, password):
    found_user_cursor = cards_collection.find({
        'username': username,
        'password': {'$exists': True},
    })
    if not found_user_cursor.count():
        return AUTH_RESULT['username_not_found']

    found_user = list(found_user_cursor)[0]
    if check_password_hash(found_user['password'], password):
        return AUTH_RESULT['ok']
    else:
        return AUTH_RESULT['password_incorrect']
