from flask import Blueprint, request
from bson import json_util
from humps import camelize

from services.piles import PilesService
from utils.decorators import standard_headers_with_str_response, require_auth, logger
from utils import responses
from utils.exceptions import AlreadyExistsError, IncorrectPasswordError, UsernameNotFoundError
from db import real_db

piles_bp = Blueprint('piles', __name__, url_prefix='/api/piles')
piles_service = PilesService(real_db)


@piles_bp.route('/get_all', methods=['GET'])
@logger
@require_auth
@standard_headers_with_str_response
def get_all():
    username = request.cookies['username']
    piles = piles_service.get_all_piles(username)
    return json_util.dumps(camelize(piles))


@piles_bp.route('/add', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def insert_pile():
    pile_name = request.form[camelize('pile_name')]
    username = request.cookies['username']
    try:
        piles_service.insert_pile(
            pile_name,
            username,
        )
    except AlreadyExistsError:
        return json_util.dumps(responses.already_exists)
    return json_util.dumps(responses.ok)


@piles_bp.route('/update', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def update_pile():
    old_pile_name = request.form[camelize('old_pile_name')]
    new_pile_name = request.form[camelize('new_pile_name')]
    username = request.cookies['username']
    try:
        piles_service.update_pile(
            old_pile_name,
            new_pile_name,
            username,
        )
    except AlreadyExistsError:
        return json_util.dumps(responses.already_exists)
    return json_util.dumps(responses.ok)


@piles_bp.route('/delete', methods=['POST'])
@logger
@require_auth
@standard_headers_with_str_response
def delete_pile():
    pile_name = request.form[camelize('pile_name')]
    username = request.cookies['username']
    piles_service.delete_pile(
        pile_name,
        username,
    )
    return json_util.dumps(responses.ok)
