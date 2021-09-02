from db import db

cards_collection = db.cards


def get_all_piles(username):
    return cards_collection.distinct(
        'pile_name',
        {'username': username}
    )


def insert_pile(pile_name, username):
    cards_collection.insert_one({
        'pile_name': pile_name,
        'username': username
    })
    return {'result': 'ok'}


def update_pile(old_pile_name, new_pile_name, username):
    cards_collection.update_many(
        {
            'pile_name': old_pile_name,
            'username': username
        },
        {
            '$set': {
                'pile_name': new_pile_name
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
            'username': username
        },
        {
            '$set': {
                'pile_name': 'default'
            }
        }
    )
    return {'result': 'ok'}
