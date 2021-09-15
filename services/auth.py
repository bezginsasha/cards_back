from werkzeug.security import generate_password_hash, check_password_hash

from utils.constants import AUTH_RESULT


class AuthService:
    def __init__(self, db_client):
        self.collection = db_client.cards_collection

    def register(self, username, password):
        found_users = self.collection.find({'username': username})
        if not found_users.count():
            self.collection.insert_one({
                'username': username,
                'password': generate_password_hash(password),
            })
            return AUTH_RESULT['ok']
        return AUTH_RESULT['username_exists']

    def login(self, username, password):
        found_user_cursor = self.collection.find({
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
