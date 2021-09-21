import json

from flask import Response, Blueprint, request

from utils.decorators import standard_headers_with_response_object, logger
from utils import responses
from utils.exceptions import UsernameNotFoundError, IncorrectPasswordError, AlreadyExistsError
from services.auth import AuthService
from db import real_db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService(real_db)


@auth_bp.route('/register', methods=('POST',))
@logger
@standard_headers_with_response_object
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        auth_service.register(username, password)
    except AlreadyExistsError:
        return Response(json.dumps(responses.already_exists))

    resp = Response(json.dumps(responses.ok))
    set_username_cookie(resp, username)
    return resp


@auth_bp.route('/login', methods=('POST',))
@logger
@standard_headers_with_response_object
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        auth_service.login(username, password)
    except UsernameNotFoundError:
        return Response(json.dumps(responses.username_not_found))
    except IncorrectPasswordError:
        return Response(json.dumps(responses.incorrect_password))

    resp = Response(json.dumps(responses.ok))
    set_username_cookie(resp, username)
    return resp


def set_username_cookie(resp, username):
    resp.set_cookie(
        key='username',
        value=username,
        samesite='Strict'
    )
