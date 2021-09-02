import json
from flask import Response, Blueprint, request
from services.auth import register_service, login_service
from utils.constants import AUTH_RESULT
from utils.decorators import standard_headers_with_response_object

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=('POST',))
@standard_headers_with_response_object
def register():
    username = request.form['username']
    password = request.form['password']
    register_result = register_service(username, password)

    resp = Response(json.dumps({'result': register_result}))
    if register_result == AUTH_RESULT['ok']:
        set_username_cookie(resp, username)
    return resp


@auth_bp.route('/login', methods=('POST',))
@standard_headers_with_response_object
def login():
    username = request.form['username']
    password = request.form['password']
    login_result = login_service(username, password)

    resp = Response(json.dumps({'result': login_result}))
    if login_result == AUTH_RESULT['ok']:
        set_username_cookie(resp, username)
    return resp


def set_username_cookie(resp, username):
    resp.set_cookie(
        key='username',
        value=username,
        samesite='Strict'
    )
