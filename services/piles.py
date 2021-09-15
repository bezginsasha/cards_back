from utils.constants import DB_OPERATION_RESULT


class PilesService:
    def __init__(self, db_client):
        self.collection = db_client.cards_collection

    def get_all_piles(self, username):
        return self.collection.distinct(
            'pile_name',
            {'username': username},
        )

    def insert_pile(self, pile_name, username):
        found_pile = self.collection.find({
            'pile_name': pile_name,
            'username': username,
        })
        if found_pile.count():
            return {'result': DB_OPERATION_RESULT['already_exists']}

        self.collection.insert_one({
            'pile_name': pile_name,
            'username': username,
        })
        return {'result': 'ok'}

    def update_pile(self, old_pile_name, new_pile_name, username):
        self.collection.update_many(
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

    def delete_pile(self, pile_name, username):
        self.collection.delete_one({
            'pile_name': pile_name,
            'original_word': {'$exists': False},
            'username': username
        })
        self.collection.update_many(
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
