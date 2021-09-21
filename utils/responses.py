ok = {'result': 'ok'}
already_exists = {'result': 'already exists'}
username_not_found = {'result': 'username not found'}
incorrect_password = {'result': 'incorrect password'}


def ok_with_inserted_id(inserted_id):
    return {
        'result': 'ok',
        'id': inserted_id
    }
