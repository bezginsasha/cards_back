from db import db
from utils.constants import DB_OPERATION_RESULT

cards_collection = db.cards


def get_all_piles(username):
    return cards_collection.distinct(
        'pile_name',
        {'username': username},
    )


def insert_pile(pile_name, username):
    found_pile = cards_collection.find({
        'pile_name': pile_name,
        'username': username,
    })
    if found_pile.count():
        return {'result': DB_OPERATION_RESULT['already_exists']}

    cards_collection.insert_one({
        'pile_name': pile_name,
        'username': username,
    })
    return {'result': 'ok'}


def update_pile(old_pile_name, new_pile_name, username):
    cards_collection.update_many(
        {
            'pile_name': old_pile_name,
            'username': username,
        },
        {
            '$set': {
                'pile_name': new_pile_name,
            }
        }
    )
    return {'result': 'ok'}


def delete_pile(pile_name, username):
    cards_collection.delete_one({
        'pile_name': pile_name,
        'original_word': {'$exists': False},
        'username': username
    })
    cards_collection.update_many(
        {
            'pile_name': pile_name,
            'username': username,
        },
        {
            '$set': {
                'pile_name': 'default',
            }
        }
    )
    return {'result': 'ok'}
